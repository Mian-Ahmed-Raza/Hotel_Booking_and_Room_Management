# app/models/review.py
from app.services.db import get_connection
from datetime import datetime


class Review:
    def __init__(self, id, booking_id, guest_name, rating, comment, created_at=None):
        self.id = id
        self.booking_id = booking_id
        self.guest_name = guest_name
        self.rating = rating
        self.comment = comment
        self.created_at = created_at

    @staticmethod
    def create_table():
        sql = """
        CREATE TABLE IF NOT EXISTS reviews (
            id INT AUTO_INCREMENT PRIMARY KEY,
            booking_id INT NOT NULL,
            guest_name VARCHAR(100) NOT NULL,
            rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (booking_id) REFERENCES bookings(id)
        ) ENGINE=InnoDB;
        """
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()

    @staticmethod
    def create(booking_id, guest_name, rating, comment):
        sql = "INSERT INTO reviews (booking_id, guest_name, rating, comment) VALUES (%s, %s, %s, %s)"
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, (booking_id, guest_name, rating, comment))
            conn.commit()
            return cur.lastrowid

    @staticmethod
    def get_all():
        sql = "SELECT id, booking_id, guest_name, rating, comment, created_at FROM reviews ORDER BY created_at DESC"
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return [Review(*row) for row in rows]

    @staticmethod
    def get_average_rating():
        sql = "SELECT AVG(rating) as avg_rating FROM reviews"
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchone()
            return result[0] if result and result[0] else 0.0

    @staticmethod
    def delete(review_id):
        sql = "DELETE FROM reviews WHERE id=%s"
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, (review_id,))
            conn.commit()
            return cur.rowcount
