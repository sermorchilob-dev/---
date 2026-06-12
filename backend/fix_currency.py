import sqlite3

conn = sqlite3.connect('motor.db')
conn.execute("UPDATE products SET currency = 'RUB' WHERE currency IS NULL;")
conn.commit()
print("✅ Поле currency обновлено")
conn.close()
