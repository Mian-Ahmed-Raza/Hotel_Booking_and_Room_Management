# app/models/booking.py
from app.services.db import get_connection
from datetime import datetime


class Booking:
    def __init__(self, id, guest_name, guest_phone, room_id, check_in, check_out, total_price, status, created_at=None):
        self.id = id
        self.guest_name = guest_name
        self.guest_phone = guest_phone
        self.room_id = room_id
        self.check_in = check_in
        self.check_out = check_out
        self.total_price = total_price
        self.status = status
        self.created_at = created_at

    @staticmethod
    def create_table():
        sql = """
        CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            guest_name VARCHAR(100) NOT NULL,
            guest_phone VARCHAR(20) NOT NULL,
            room_id INT NOT NULL,
            check_in DATE NOT NULL,
            check_out DATE NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            status VARCHAR(20) DEFAULT 'Confirmed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (room_id) REFERENCES rooms(id)
        ) ENGINE=InnoDB;
        """
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()

    @staticmethod
    def create(guest_name, guest_phone, room_id, check_in, check_out, total_price, status='Confirmed'):
        sql = """INSERT INTO bookings (guest_name, guest_phone, room_id, check_in, check_out, total_price, status) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, (guest_name, guest_phone, room_id, check_in, check_out, total_price, status))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def get_all():
        sql = """SELECT b.id, b.guest_name, b.guest_phone, b.room_id, b.check_in, b.check_out, 
                        b.total_price, b.status, b.created_at
                 FROM bookings b ORDER BY b.created_at DESC"""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return [Booking(*row) for row in rows]

    @staticmethod
    def get_by_id(booking_id):
        sql = """SELECT id, guest_name, guest_phone, room_id, check_in, check_out, 
                        total_price, status, created_at
                 FROM bookings WHERE id=%s"""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, (booking_id,))
            row = cur.fetchone()
            if row:
                return Booking(*row)
            return None

    @staticmethod
    def get_active():
        sql = """SELECT id, guest_name, guest_phone, room_id, check_in, check_out, 
                        total_price, status, created_at
                 FROM bookings WHERE status IN ('Confirmed', 'Checked-in') 
                 ORDER BY check_in"""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return [Booking(*row) for row in rows]

    @staticmethod
    def update(booking_id, **kwargs):
        fields = []
        params = []
        for k, v in kwargs.items():
            fields.append(f"{k}=%s")
            params.append(v)
        params.append(booking_id)
        sql = f"UPDATE bookings SET {', '.join(fields)} WHERE id=%s"
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, tuple(params))
            conn.commit()
            return cur.rowcount

    @staticmethod
    def delete(booking_id):
        sql = "DELETE FROM bookings WHERE id=%s"
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, (booking_id,))
            conn.commit()
            return cur.rowcount
