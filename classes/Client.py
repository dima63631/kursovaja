from db import get_connection

class Client:
    _connection = get_connection()

    def __init__(self, id=None, full_name=None, contact_info=None):
        self.id = id
        self.full_name = full_name
        self.contact_info = contact_info

    @classmethod
    def get_all(cls):
        if cls._connection is None:
            raise Exception("Підключення до бази не встановлено!")
        clients = []
        with cls._connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM Client")
            for row in cursor.fetchall():
                clients.append(
                    cls(id=row['ID'], full_name=row['FullName'], contact_info=row['ContactInfo'])
                )
        return clients

    @classmethod
    def get_by_id(cls, client_id):
        if cls._connection is None:
            raise Exception("Підключення до бази не встановлено!")
        with cls._connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM Client WHERE ID = %s", (client_id,))
            row = cursor.fetchone()
            if row:
                return cls(id=row['ID'], full_name=row['FullName'], contact_info=row['ContactInfo'])
            else:
                raise Exception("Клієнта з таким ID не знайдено")

    @classmethod
    def update(cls, client_id, fullname, contactinfo):
        if cls._connection is None:
            raise Exception("База не підключена")
        cursor = cls._connection.cursor()
        try:
            sql = "UPDATE Client SET FullName=%s, ContactInfo=%s WHERE ID=%s"
            cursor.execute(sql, (fullname, contactinfo, client_id))
            cls._connection.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()

    def save(self):
        if self._connection is None:
            raise Exception("Підключення до бази не встановлено!")
        cursor = self._connection.cursor()
        try:
            if self.id is None:
                sql = "INSERT INTO Client (FullName, ContactInfo) VALUES (%s, %s)"
                cursor.execute(sql, (self.full_name, self.contact_info))
                self.id = cursor.lastrowid
            else:
                sql = "UPDATE Client SET FullName=%s, ContactInfo=%s WHERE ID=%s"
                cursor.execute(sql, (self.full_name, self.contact_info, self.id))
            self._connection.commit()
        finally:
            cursor.close()

    def delete(self):
        if self.id is None:
            raise Exception("Неможливо видалити клієнта без ID")
        cursor = self._connection.cursor()
        try:
            sql = "DELETE FROM Client WHERE ID=%s"
            cursor.execute(sql, (self.id,))
            self._connection.commit()
            self.id = None
        finally:
            cursor.close()