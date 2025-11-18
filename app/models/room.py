# app/models/room.py
from app.services.db import get_connection


class Room:
    def __init__(self, id, room_number, room_type, price, status, description=None):
        self.id = id
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.status = status
        self.description = description

    @staticmethod
    def create_table():
        sql = """
        CREATE TABLE IF NOT EXISTS rooms (
            id INT AUTO_INCREMENT PRIMARY KEY,
            room_number VARCHAR(10) UNIQUE NOT NULL,
            room_type VARCHAR(50) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            status VARCHAR(20) DEFAULT 'Available',
            description TEXT
        ) ENGINE=InnoDB;
        """
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()

    @staticmethod
    def create(room_number, room_type, price, status='Available', description=None):
        sql = "INSERT INTO rooms (room_number, room_type, price, status, description) VALUES (%s, %s, %s, %s, %s)"
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, (room_number, room_type, price, status, description))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def get_all():
        sql = "SELECT id, room_number, room_type, price, status, description FROM rooms ORDER BY room_number"
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return [Room(*row) for row in rows]

    @staticmethod
    def get_by_id(room_id):
        sql = "SELECT id, room_number, room_type, price, status, description FROM rooms WHERE id=%s"
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, (room_id,))
            row = cur.fetchone()
            if row:
                return Room(*row)
            return None

    @staticmethod
    def get_available():
        sql = "SELECT id, room_number, room_type, price, status, description FROM rooms WHERE status='Available' ORDER BY room_number"
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return [Room(*row) for row in rows]

    @staticmethod
    def update(room_id, **kwargs):
        fields = []
        params = []
        for k, v in kwargs.items():
            fields.append(f"{k}=%s")
            params.append(v)
        params.append(room_id)
        sql = f"UPDATE rooms SET {', '.join(fields)} WHERE id=%s"
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, tuple(params))
            conn.commit()
            return cur.rowcount

    @staticmethod
    def delete(room_id):
        sql = "DELETE FROM rooms WHERE id=%s"
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, (room_id,))
            conn.commit()
            return cur.rowcount
