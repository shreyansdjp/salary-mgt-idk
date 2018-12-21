from mysql import get_connection
from passlib.hash import sha256_crypt

def check_int(number):
    try:
        n = int(number)
        return True
    except ValueError:
        return False

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
            return False
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
            return False
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
            return None
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
            return False
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
            return False
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
            return None
        finally:
            cursor.close()

    def get(self, company_id):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `administrators` WHERE company_id=%s"
                cursor.execute(sql, (str(company_id)))
                self.connection.commit()
                if cursor.rowcount == 0:
                    return None
                return cursor.fetchall()
        except Exception as e:
            print(e)
            return None
        finally:
            cursor.close()

    def update(self, id, name, username, password, is_owner, company_id, is_supervisor=1):
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE `administrators` SET name=%s, username=%s, pass=%s, is_owner=%s, is_supervisor=%s \
                        WHERE id=%s AND company_id=%s;"
                password_hash = sha256_crypt.encrypt(password)
                cursor.execute(sql, (name, username, password_hash, str(is_owner), str(is_supervisor), str(id), str(company_id)))
                self.connection.commit()
                print(cursor.rowcount)
                if cursor.rowcount == 0:
                    return False
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()

    def delete(self, id, company_id):
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM `administrators` WHERE id=%s AND company_id=%s"
                cursor.execute(sql, (str(id), str(company_id)))
                self.connection.commit()
                if cursor.rowcount == 0:
                    return False
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()

    def get_one(self, id):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `administrators` WHERE id=%s;"
                cursor.execute(sql, (str(id)))
                self.connection.commit()
                if cursor.rowcount == 0:
                    return None
                return cursor.fetchone()
        except Exception as e:
            print(e)
            return None
        finally:
            cursor.close()

    def __del__(self):
        self.connection.close()


class Employee:

    def __init__(self):
        self.connection = get_connection()

    def if_exists(self, name, designation, department_no, company_id):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `employees` WHERE name=%s AND designation=%s AND department_no=%s AND company_id=%s"
                cursor.execute(sql, (name, designation, str(department_no), str(company_id)))
                self.connection.commit()
                if cursor.rowcount == 0:
                    return False
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()

    def create(self, name, hour_rate, hours_worked, designation, department_no, company_id):
        if self.if_exists(name, designation, department_no, company_id):
            return True
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO `employees` (`name`, `hour_rate`, `hours_worked`, `designation`, `department_no`, `company_id`) \
                        VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, str(hour_rate), str(hours_worked), designation, str(department_no), str(company_id)))
                self.connection.commit()
                if cursor.rowcount == 0:
                    return False
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()

    def get_one(self, id):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `employees` WHERE id=%s"
                cursor.execute(sql, (str(id)))
                self.connection.commit()
                if cursor.rowcount == 0:
                    return None
                return cursor.fetchone()
        except Exception as e:
            print(e)
            return None
        finally:
            cursor.close()

    def get(self, company_id):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `employees` WHERE company_id=%s"
                cursor.execute(sql, (company_id))
                self.connection.commit()
                if cursor.rowcount == 0:
                    return None
                return cursor.fetchall()
        except Exception as e:
            print(e)
            return None
        finally:
            cursor.close()

    def update(self, id, name, hour_rate, hours_worked, designation, department_no, company_id):
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE `employees` SET name=%s, hour_rate=%s, hours_worked=%s, designation=%s, department_no=%s \
                        WHERE id=%s AND company_id=%s;"
                cursor.execute(sql, (name, str(hour_rate), str(hours_worked), designation, str(department_no), str(id), str(company_id)))
                self.connection.commit()
                print(cursor.rowcount)
                if cursor.rowcount == 0:
                    return False
                return True
        except Exception as e:
            print('something went wrong')
            print(e)
            return False
        finally:
            cursor.close()

    def delete(self, id, company_id):
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM `employees` WHERE id=%s AND company_id=%s"
                cursor.execute(sql, (str(id), str(company_id)))
                self.connection.commit()
                if cursor.rowcount == 0:
                    return False
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()

    def __del__(self):
        self.connection.close()
