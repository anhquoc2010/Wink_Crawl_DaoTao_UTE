import os
import smtplib
import pandas as pd
from crawl_noti_daotao_ute.get_noti_from_db import is_subject_in_notification

def send_mail_smtp(receiver, title, content):
    EMAIL_SMTP_SERVER = "smtp.gmail.com"
    EMAIL_PORT = 587  # For starttls
    EMAIL_USER = "winkbotute@gmail.com"
    EMAIL_PASS = "bwiqiobkzbkuhife"
    EMAIL_MESSAGE = f"Subject: {title}\n\n{content}"

    try:
        server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, receiver, EMAIL_MESSAGE.encode('utf-8'))
        server.close()
        print("SMTP: Successfully sent the mail")
    except Exception as e:
        print(f"SMTP: Failed to send mail: {e}")

def send_mail(data):
    status, title, content = is_subject_in_notification(data[1], data[2])
    if status:
        send_mail_smtp(str(data[0]) + "@sv.ute.udn.vn", title, content)
        print(f"[V]SENDMAIL: SEND MAIL TO {data[0]} with {title} - {content}")

def send_mail_timetable(student_id):
    if os.path.exists('./timetable.csv'):
        gen = pd.read_csv('./timetable.csv', chunksize=10000)
        df = pd.concat((x.query(f"student_id == {student_id}") for x in gen), ignore_index=True)
        df.apply(send_mail, axis=1)
        print("[V]TIMETABLE: DONE SEND MAIL !!")
    else:
        print("[!]TIMETABLE: NO FILE TO READ DATA !!")
