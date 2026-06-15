import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional, Any
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import text

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm

# Загружаем переменные окружения
load_dotenv()

# ----- Конфигурация базы данных (используем Transaction pooler с портом 6543) -----
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL не задан в .env")

# Приводим к формату для psycopg2 (если нужно)
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ----- Модели для заявок -----
class QuotationRequest(Base):
    __tablename__ = "quotation_requests"
    id = Column(Integer, primary_key=True, index=True)
    request_number = Column(String(50), unique=True, nullable=False)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(50))
    contact_name = Column(String(200))
    company_name = Column(String(200))
    project_name = Column(String(500))
    project_description = Column(Text)
    status = Column(String(50), default="new")
    created_at = Column(DateTime, default=datetime.utcnow)

class RequestItem(Base):
    __tablename__ = "request_items"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("quotation_requests.id"), nullable=False)
    product_id = Column(Integer, nullable=False)
    product_name = Column(String(200))
    quantity = Column(Integer, default=1)
    notes = Column(Text)

# Создаём таблицы (если их нет)
Base.metadata.create_all(bind=engine)

# ----- Pydantic схемы -----
class QuoteRequestItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int = 1
    notes: Optional[str] = None

class QuoteRequestCreate(BaseModel):
    contact_email: str
    contact_phone: Optional[str] = None
    contact_name: Optional[str] = None
    company_name: Optional[str] = None
    project_name: Optional[str] = None
    project_description: Optional[str] = None
    items: List[QuoteRequestItem]

class QuoteResponse(BaseModel):
    id: int
    request_number: str
    status: str
    created_at: datetime
    pdf_url: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    product_code: str
    name: str
    power_kw: Optional[float]
    speed_rpm: Optional[int]
    voltage: Optional[str]
    price: Optional[float]
    manufacturer_name: str

# ----- Вспомогательные функции -----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_request_number():
    now = datetime.utcnow()
    return f"RQ-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}"

# ----- Отправка email (без вложений, только текст) -----
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
if not EMAIL_PASSWORD:
    print("⚠️ EMAIL_PASSWORD не задан – уведомления не будут отправляться")

def send_email_notification(manager_email: str, subject: str, body_html: str):
    if not EMAIL_PASSWORD:
        return
    sender_email = "Ser.orchilob@gmail.com"
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = manager_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body_html, "html"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, EMAIL_PASSWORD)
            server.sendmail(sender_email, manager_email, msg.as_string())
        print("✅ Email отправлен")
    except Exception as e:
        print(f"❌ Ошибка email: {e}")

# ----- Генерация PDF (без внешних шрифтов) -----
def generate_quote_pdf(request_id: int, request_data: dict, items: list, db: Session) -> str:
    pdf_dir = "pdf_quotes"
    os.makedirs(pdf_dir, exist_ok=True)
    filename = f"quote_{request_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(pdf_dir, filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,
        spaceAfter=12
    )

    story = []
    story.append(Paragraph("КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>№ заявки:</b> {request_data['request_number']}", styles['Normal']))
    story.append(Paragraph(f"<b>Дата:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}", styles['Normal']))
    story.append(Paragraph(f"<b>Клиент:</b> {request_data.get('company_name', 'Не указано')}", styles['Normal']))
    story.append(Paragraph(f"<b>Контакт:</b> {request_data.get('contact_name', '')} ({request_data.get('contact_email', '')})", styles['Normal']))
    story.append(Spacer(1, 10))

    data = [["№", "Наименование", "Кол-во", "Цена", "Сумма"]]
    total_sum = 0.0
    for idx, item in enumerate(items, 1):
        price_row = db.execute(text("SELECT price FROM products WHERE id = :pid"), {"pid": item.product_id}).fetchone()
        price = float(price_row[0]) if price_row and price_row[0] else 0.0
        amount = price * item.quantity
        total_sum += amount
        data.append([
            str(idx),
            item.product_name,
            str(item.quantity),
            f"{price:,.2f} руб.",
            f"{amount:,.2f} руб."
        ])
    data.append(["", "", "", "<b>Итого:</b>", f"<b>{total_sum:,.2f} руб.</b>"])

    table = Table(data, colWidths=[30, 250, 50, 80, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    story.append(table)
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Условия поставки:</b>", styles['Normal']))
    story.append(Paragraph("Срок изготовления: 2-4 недели. Доставка по согласованию. Цены указаны без НДС.", styles['Normal']))

    doc.build(story)
    return filepath

# ----- FastAPI приложение -----
app = FastAPI(title="Конфигуратор приводной техники", version="2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Эндпоинты -----
@app.get("/")
def root():
    return {"message": "API конфигуратора работает"}

@app.get("/api/v1/products")
def get_products(
    limit: int = 20,
    offset: int = 0,
    power_min: Optional[float] = None,
    power_max: Optional[float] = None,
    speed_min: Optional[int] = None,
    speed_max: Optional[int] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    manufacturer: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = """
        SELECT p.id, p.product_code, p.name, p.power_kw, p.speed_rpm, p.voltage, p.price,
               m.name as manufacturer_name
        FROM products p
        JOIN manufacturers m ON p.manufacturer_id = m.id
        WHERE p.is_active = true
    """
    params = {}
    conditions = []
    if power_min is not None:
        conditions.append("p.power_kw >= :power_min")
        params["power_min"] = power_min
    if power_max is not None:
        conditions.append("p.power_kw <= :power_max")
        params["power_max"] = power_max
    if speed_min is not None:
        conditions.append("p.speed_rpm >= :speed_min")
        params["speed_min"] = speed_min
    if speed_max is not None:
        conditions.append("p.speed_rpm <= :speed_max")
        params["speed_max"] = speed_max
    if price_min is not None:
        conditions.append("p.price >= :price_min")
        params["price_min"] = price_min
    if price_max is not None:
        conditions.append("p.price <= :price_max")
        params["price_max"] = price_max
    if manufacturer:
        conditions.append("m.name ILIKE :manufacturer")
        params["manufacturer"] = f"%{manufacturer}%"
    if search:
        conditions.append("(p.name ILIKE :search OR p.product_code ILIKE :search)")
        params["search"] = f"%{search}%"
    if conditions:
        query += " AND " + " AND ".join(conditions)
    query += " ORDER BY p.id LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    result = db.execute(text(query), params)
    products = []
    for row in result:
        products.append({
            "id": row[0],
            "product_code": row[1],
            "name": row[2],
            "power_kw": float(row[3]) if row[3] else None,
            "speed_rpm": row[4],
            "voltage": row[5],
            "price": float(row[6]) if row[6] else None,
            "manufacturer_name": row[7]
        })
    return products

@app.get("/api/v1/manufacturers")
def get_manufacturers(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT id, name FROM manufacturers ORDER BY name"))
    return [{"id": row[0], "name": row[1]} for row in result]

@app.get("/api/v1/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    row = db.execute(text("""
        SELECT p.id, p.product_code, p.name, p.power_kw, p.speed_rpm, p.voltage, p.price,
               m.name as manufacturer_name
        FROM products p
        JOIN manufacturers m ON p.manufacturer_id = m.id
        WHERE p.id = :id
    """), {"id": product_id}).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(
        id=row[0], product_code=row[1], name=row[2],
        power_kw=float(row[3]) if row[3] else None,
        speed_rpm=row[4], voltage=row[5],
        price=float(row[6]) if row[6] else None,
        manufacturer_name=row[7]
    )

@app.post("/api/v1/quote-requests", response_model=QuoteResponse)
def create_quote_request(request: QuoteRequestCreate, db: Session = Depends(get_db)):
    req_number = generate_request_number()
    db_request = QuotationRequest(
        request_number=req_number,
        contact_email=request.contact_email,
        contact_phone=request.contact_phone,
        contact_name=request.contact_name,
        company_name=request.company_name,
        project_name=request.project_name,
        project_description=request.project_description,
        status="new"
    )
    db.add(db_request)
    db.flush()

    for item in request.items:
        db_item = RequestItem(
            request_id=db_request.id,
            product_id=item.product_id,
            product_name=item.product_name,
            quantity=item.quantity,
            notes=item.notes
        )
        db.add(db_item)
    db.commit()
    db.refresh(db_request)

    pdf_url = None
    try:
        request_dict = {
            "request_number": db_request.request_number,
            "company_name": db_request.company_name,
            "contact_name": db_request.contact_name,
            "contact_email": db_request.contact_email,
        }
        items_list = db.query(RequestItem).filter(RequestItem.request_id == db_request.id).all()
        pdf_path = generate_quote_pdf(db_request.id, request_dict, items_list, db)
        pdf_url = f"/api/v1/quote-requests/{db_request.id}/download"
    except Exception as e:
        print(f"Ошибка PDF: {e}")

    try:
        items_list = db.query(RequestItem).filter(RequestItem.request_id == db_request.id).all()
        body = f"""
<h2>Новая заявка #{db_request.request_number}</h2>
<p><b>Клиент:</b> {db_request.contact_name}</p>
<p><b>Email:</b> {db_request.contact_email}</p>
<p><b>Телефон:</b> {db_request.contact_phone or '—'}</p>
<p><b>Компания:</b> {db_request.company_name or '—'}</p>
<p><b>Проект:</b> {db_request.project_name or '—'}</p>
<p><b>Описание:</b> {db_request.project_description or '—'}</p>
<hr>
<p><b>Позиции:</b></p>
<ul>
"""
        for item in items_list:
            body += f"<li>{item.product_name} x {item.quantity}</li>"
        body += f"""
</ul>
<p><b>Дата:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
"""
        send_email_notification("manager@example.com", f"Заявка #{db_request.request_number}", body)
    except Exception as e:
        print(f"Ошибка email: {e}")

    return QuoteResponse(
        id=db_request.id,
        request_number=db_request.request_number,
        status=db_request.status,
        created_at=db_request.created_at,
        pdf_url=pdf_url
    )

@app.get("/api/v1/quote-requests/{request_id}/download")
def download_quote_pdf(request_id: int):
    pdf_dir = "pdf_quotes"
    if not os.path.exists(pdf_dir):
        raise HTTPException(status_code=404, detail="PDF not found")
    for fname in os.listdir(pdf_dir):
        if fname.startswith(f"quote_{request_id}_"):
            filepath = os.path.join(pdf_dir, fname)
            return FileResponse(filepath, media_type='application/pdf', filename=fname)
    raise HTTPException(status_code=404, detail="PDF not found")

@app.get("/api/v1/quote-requests")
def list_quote_requests(db: Session = Depends(get_db)):
    requests = db.query(QuotationRequest).order_by(QuotationRequest.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "request_number": r.request_number,
            "contact_email": r.contact_email,
            "contact_name": r.contact_name,
            "company_name": r.company_name,
            "status": r.status,
            "created_at": r.created_at.isoformat()
        }
        for r in requests
    ]

# ----- Мастер подбора (упрощённый) -----
selection_sessions = {}
MOTOR_QUESTIONS = [
    {"id": "power", "question": "Мощность (кВт)?", "type": "number"},
    {"id": "speed", "question": "Обороты (об/мин)?", "type": "number"},
    {"id": "manufacturer", "question": "Производитель?", "type": "select", "options": ["Siemens", "ABB", "SEW-Eurodrive", "Любой"]},
    {"id": "price_max", "question": "Макс. цена (руб)?", "type": "number"},
]

class AnswerSubmit(BaseModel):
    session_id: str
    answer_id: str
    value: Any

@app.post("/api/selection/start")
def start_selection():
    session_id = str(uuid4())
    selection_sessions[session_id] = {"answers": {}, "current_index": 0}
    return {"session_id": session_id, "questions": MOTOR_QUESTIONS, "total": len(MOTOR_QUESTIONS)}

@app.post("/api/selection/answer")
def submit_answer(data: AnswerSubmit):
    if data.session_id not in selection_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    selection_sessions[data.session_id]["answers"][data.answer_id] = data.value
    current = selection_sessions[data.session_id].get("current_index", 0)
    nxt = current + 1
    if nxt < len(MOTOR_QUESTIONS):
        selection_sessions[data.session_id]["current_index"] = nxt
        return {"next_question": MOTOR_QUESTIONS[nxt], "progress": nxt + 1, "total": len(MOTOR_QUESTIONS), "finished": False}
    else:
        return {"finished": True, "progress": len(MOTOR_QUESTIONS), "total": len(MOTOR_QUESTIONS)}

@app.post("/api/selection/result")
def get_selection_result(session_id: str, db: Session = Depends(get_db)):
    if session_id not in selection_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    answers = selection_sessions[session_id]["answers"]
    query = """
        SELECT p.id, p.product_code, p.name, p.power_kw, p.speed_rpm, p.price, m.name as manufacturer_name
        FROM products p
        JOIN manufacturers m ON p.manufacturer_id = m.id
        WHERE p.is_active = true
    """
    params = {}
    conds = []
    if "power" in answers:
        pwr = float(answers["power"])
        conds.append("p.power_kw >= :pmin AND p.power_kw <= :pmax")
        params["pmin"] = pwr * 0.9
        params["pmax"] = pwr * 1.1
    if "speed" in answers:
        spd = int(answers["speed"])
        conds.append("p.speed_rpm >= :smin AND p.speed_rpm <= :smax")
        params["smin"] = spd * 0.95
        params["smax"] = spd * 1.05
    if "manufacturer" in answers and answers["manufacturer"] != "Любой":
        conds.append("m.name = :manuf")
        params["manuf"] = answers["manufacturer"]
    if "price_max" in answers:
        conds.append("p.price <= :pmax")
        params["pmax"] = float(answers["price_max"])
    if conds:
        query += " AND " + " AND ".join(conds)
    query += " ORDER BY p.price LIMIT 20"
    result = db.execute(text(query), params)
    products = []
    for row in result:
        products.append({
            "id": row[0],
            "product_code": row[1],
            "name": row[2],
            "power_kw": float(row[3]) if row[3] else None,
            "speed_rpm": row[4],
            "price": float(row[5]) if row[5] else None,
            "manufacturer_name": row[6]
        })
    return products

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)