from crawl_noti_daotao_ute.get_timetable_ute import get_timetable
from fastapi import FastAPI
import pandas as pd
from crawl_noti_daotao_ute.get_timetable_ute import save_csv
from crawl_noti_daotao_ute.send_mail import send_mail_timetable

app = FastAPI()

@app.get("/crawl_noti_daotao_ute/timetable")
def timetable_endpoint(student_id: str):
    student_name, timetable = get_timetable(student_id)
    subject = []
    for i in range(len(timetable)):
        subject_raw = timetable[i]
        ## get element 0 and 1 in subject
        subject.append({
            'student_id': student_id,
            'subject_id': subject_raw[0],
            'subject_name': subject_raw[1]
        })
    save_csv(subject)
    #read csv file
    gen = pd.read_csv('./timetable.csv', chunksize=10000)
    df = pd.concat((x.query(f"student_id == {student_id}") for x in gen), ignore_index=True)
    return {"student_id": student_id,
            "student_name": student_name.strip(),
            "subjects": df.to_dict('records')}

@app.post("/crawl_noti_daotao_ute/sendmail")
def sendmail_endpoint(student_id: str):
    timetable_endpoint(student_id)
    send_mail_timetable(student_id)
    return {"status": "success"}
