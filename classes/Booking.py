from db import get_connection
from classes.Hall import Hall


class Booking:
    def __init__(self, id=None, client_id=None, hall_id=None, date=None, time=None, status='Активне'):
        self.id = id
        self.client_id = client_id
        self.hall_id = hall_id
        self.date = date
        self.time = time
        self.status = status

    @property
    def total_cost(self):
        hall = Hall.get_by_id(self.hall_id)
        return float(self.time) * hall.hourly_rate if hall else 0

    def save(self):
        import datetime
        conn = get_connection()
        cursor = conn.cursor()

        # якщо time = timedelta, переводимо у години (float)
        if isinstance(self.time, datetime.timedelta):
            hours = self.time.total_seconds() / 3600
        else:
            hours = float(self.time)

        if self.id is None:
            cursor.execute(
                "INSERT INTO Booking (client_id, hall_id, date, time, total_cost, status) VALUES (%s, %s, %s, %s, %s, %s)",
                (self.client_id, self.hall_id, self.date, hours, self.total_cost, self.status)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE Booking SET client_id=%s, hall_id=%s, date=%s, time=%s, total_cost=%s, status=%s WHERE id=%s",
                (self.client_id, self.hall_id, self.date, hours, self.total_cost, self.status, self.id)
            )
        conn.commit()
        cursor.close()
        conn.close()

    def delete(self):
        if self.id is None:
            raise Exception("Неможливо видалити бронювання без ID")
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                # Видалення бронювання
                cursor.execute("DELETE FROM Booking WHERE ID=%s", (self.id,))

                # Перевірка, чи є ще активні бронювання для цього залу
                cursor.execute(
                    "SELECT COUNT(*) FROM Booking WHERE HallID=%s AND Status='Активне'",
                    (self.hall_id,)
                )
                count = cursor.fetchone()[0]
                if count == 0:
                    hall = Hall.get_by_id(self.hall_id)
                    hall.status = 'Вільний'
                    hall.save(conn)

                conn.commit()
        finally:
            conn.close()

    @classmethod
    def get_all(cls):
        conn = get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM Booking")
                rows = cursor.fetchall()
                return [
                    cls(
                        id=r['ID'],
                        client_id=r['ClientID'],
                        hall_id=r['HallID'],
                        date=r['Date'],
                        time=r['Time'],
                        status=r['Status']
                    )
                    for r in rows
                ]
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, booking_id):
        conn = get_connection()
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM Booking WHERE ID=%s", (booking_id,))
                row = cursor.fetchone()
                if not row:
                    raise Exception("Бронювання не знайдено")
                return cls(
                    id=row['ID'],
                    client_id=row['ClientID'],
                    hall_id=row['HallID'],
                    date=row['Date'],
                    time=row['Time'],
                    status=row['Status']
                )
        finally:
            conn.close()
