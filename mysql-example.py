import pymysql

def get_connection():
    host = ''
    username = ''
    password = ''
    db_name = ''
    db = pymysql.connect(host, username, password, db_name, cursorclass=pymysql.cursors.DictCursor)
