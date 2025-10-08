from db import get_connection


class Payment:
    def __init__(self, booking_id, amount, status='Очікується', payment_id=None):
        self.id = payment_id
        self.booking_id = booking_id
        self.amount = amount
        self.status = status

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id:
                cursor.execute(
                    """
                    UPDATE Payment
                    SET BookingID=%s, Amount=%s, Status=%s
                    WHERE ID=%s
                    """,
                    (self.booking_id, self.amount, self.status, self.id)
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO Payment (BookingID, Amount, Status)
                    VALUES (%s, %s, %s)
                    """,
                    (self.booking_id, self.amount, self.status)
                )
                self.id = cursor.lastrowid
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def mark_paid(self):
        if not self.id:
            raise ValueError("Платіж не має ID.")
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Payment SET Status='Сплачено' WHERE ID=%s",
                (self.id,)
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def get_all(cls):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM Payment")
            payments = [
                cls(
                    booking_id=row['BookingID'],
                    amount=float(row['Amount']),
                    status=row['Status'],
                    payment_id=row['ID']
                )
                for row in cursor.fetchall()
            ]
            return payments
        finally:
            cursor.close()
            conn.close()
