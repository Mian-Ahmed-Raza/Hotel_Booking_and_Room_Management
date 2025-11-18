# app/models/user.py
def create_table():
sql = """
CREATE TABLE IF NOT EXISTS users (
id INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(100) UNIQUE NOT NULL,
password VARCHAR(255) NOT NULL,
full_name VARCHAR(255)
) ENGINE=InnoDB;
"""
with get_connection() as conn:
cur = conn.cursor()
cur.execute(sql)
conn.commit()


@staticmethod
def create(username, password, full_name=None):
sql = "INSERT INTO users (username, password, full_name) VALUES (%s, %s, %s)"
with get_connection() as conn:
cur = conn.cursor()
cur.execute(sql, (username, password, full_name))
conn.commit()
return cur.lastrowid


@staticmethod
def get_by_username(username):
sql = "SELECT id, username, password, full_name FROM users WHERE username=%s"
with get_connection() as conn:
cur = conn.cursor()
cur.execute(sql, (username,))
row = cur.fetchone()
if row:
return User(*row)
return None


@staticmethod
def update(id, **kwargs):
fields = []
params = []
for k, v in kwargs.items():
fields.append(f"{k}=%s")
params.append(v)
params.append(id)
sql = f"UPDATE users SET {', '.join(fields)} WHERE id=%s"
with get_connection() as conn:
cur = conn.cursor()
cur.execute(sql, tuple(params))
conn.commit()
return cur.rowcount


@staticmethod
def delete(id):
sql = "DELETE FROM users WHERE id=%s"
with get_connection() as conn:
cur = conn.cursor()
cur.execute(sql, (id,))
conn.commit()
return cur.rowcount