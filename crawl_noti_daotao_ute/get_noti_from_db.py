import mysql.connector

MYSQL_HOST = "localhost"
MYSQL_DATABASE = "crawl_noti_daotao_ute"
MYSQL_TABLE = "notification"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_PORT = 3306
MYSQL_UPSERT = False
MYSQL_RETRIES = 3
MYSQL_CLOSE_ON_ERROR = True
MYSQL_CHARSET = 'utf8'

database = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE,
    auth_plugin='mysql_native_password'
)

def is_old_notification(id_notification):
    cursor = database.cursor()
    cursor.execute("select * from notification order by id desc")

    results = cursor.fetchall()
    for result in results:
        old_id_notification, _, _ = result
        if int(id_notification) == old_id_notification:
            return True
    return False

def is_subject_in_notification(subject_id, subject_name):
    cursor = database.cursor()
    cursor.execute("select * from notification order by id desc")

    results = cursor.fetchall()
    for result in results:
        _, title, content = result
        if subject_id in title or subject_name in title or subject_id in content or subject_name in content:
            return True, title, content
    return False, _, _
