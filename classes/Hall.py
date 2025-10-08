from db import get_connection

class Hall:
    STATUSES = ['Вільний', 'Заброньований', 'Ремонт']

    def __init__(self, name, area, additional_services, hourly_rate, status='Вільний', id=None):
        self.id = id
        self.name = name
        self.area = area
        self.additional_services = additional_services
        self.hourly_rate = hourly_rate
        self.status = status

    @classmethod
    def _from_row(cls, row):
        return cls(
            id=row['ID'],
            name=row['Name'],
            area=float(row['Area']),
            additional_services=row['AdditionalServices'],
            hourly_rate=float(row['Hourly_Rate']),
            status=row['Status']
        )

    @classmethod
    def get_all(cls):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM Hall")
                return [cls._from_row(row) for row in cursor.fetchall()]

    @classmethod
    def get_by_id(cls, hall_id):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM Hall WHERE ID=%s", (hall_id,))
                row = cursor.fetchone()
                if not row:
                    raise Exception("Зала не знайдена")
                return cls._from_row(row)

    def save(self, conn=None):
        need_to_close = conn is None
        if need_to_close:
            conn = get_connection()

        try:
            with conn.cursor() as cursor:
                if self.id is None:
                    cursor.execute(
                        "INSERT INTO Hall (Name, Area, AdditionalServices, Hourly_Rate, Status) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        (self.name, self.area, self.additional_services, self.hourly_rate, self.status)
                    )
                    self.id = cursor.lastrowid
                else:
                    cursor.execute(
                        "UPDATE Hall SET Name=%s, Area=%s, AdditionalServices=%s, "
                        "Hourly_Rate=%s, Status=%s WHERE ID=%s",
                        (self.name, self.area, self.additional_services, self.hourly_rate, self.status, self.id)
                    )
            if need_to_close:
                conn.commit()
        finally:
            if need_to_close:
                conn.close()

    def delete(self):
        if self.id is None:
            raise Exception("Зала не існує в базі")
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Hall WHERE ID=%s", (self.id,))
                conn.commit()