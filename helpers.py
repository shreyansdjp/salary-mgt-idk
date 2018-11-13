from mysql import get_connection
from passlib.hash import sha256_crypt

class Company:

    def __init__(self):
        self.connection = get_connection()

    def if_exists(self, name, registration_no):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `companies` WHERE name=%s AND registration_no=%s"
                cursor.execute(sql, (name, registration_no))
                self.connection.commit()
                if cursor.rowcount == 0:
                    return False
                return True
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    def create(self, name, address, registration_no):
        if self.if_exists(name, registration_no):
            return True
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO companies (`name`, `address`, `registration_no`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (name, address, registration_no))
                self.connection.commit()
                if cursor.rowcount == 0:
                    return False
                return True
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    def get(self, name, registration_no):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `companies` WHERE name=%s AND registration_no=%s"
                cursor.execute(sql, (name, registration_no))
                self.connection.commit()
                if cursor.rowcount == 0:
                    return None
                return cursor.fetchone()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
    
    def __del__(self):
        self.connection.close()


class Administrator:

    def __init__(self):
        self.connection = get_connection()

    def if_exists(self, username):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `administrators` WHERE username=%s"
                cursor.execute(sql, (username))
                self.connection.commit()
                if cursor.rowcount == 0:
                    return False
                return True
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    def create(self, name, username, password, company_id, is_owner=0, is_supervisor=1):
        if self.if_exists(username):
            return True
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO `administrators` (`name`, `username`, `pass`, `is_owner`, `is_supervisor`, `company_id`) \
                        VALUES (%s, %s, %s, %s, %s, %s)"
                password_hash = sha256_crypt.encrypt(password)
                cursor.execute(sql, (name, username, password_hash, str(is_owner), str(is_supervisor), str(company_id)))
                self.connection.commit()
                if cursor.rowcount == 0:
                    return False
                return True
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    def verify_and_get(self, username, password):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `administrators` WHERE username=%s"
                cursor.execute(sql, (username))
                self.connection.commit()
                if cursor.rowcount == 0:
                    return None
                result = cursor.fetchone()
                if sha256_crypt.verify(password, result['pass']):
                    return result
                return None
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    def __del__(self):
        self.connection.close()


class Employee:

    def __init__(self):
        self.connection = get_connection()

    def __del__(self):
        self.connection.close()
