import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_timetable(student_id):
    payload = {"masv": student_id}
    rq = requests.Session()

    utf_8 = rq.get('http://daotao.ute.udn.vn/svtkb.asp')
    page = rq.post('http://daotao.ute.udn.vn/svtkb.asp', data=payload)

    page.encoding = utf_8.apparent_encoding
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.select_one('#inner-column-container > div:nth-child(2) table:nth-of-type(1)')
    rows = table.find_all('tr')
    name = soup.select("#inner-column-container > div:nth-of-type(2) p")[0].text.split('\n')[3].replace('&nbsp', '').split(':')[-1]

    datas = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        datas.append([ele for ele in cols if ele])

    return name, datas

def save_csv(data):
    print(data)
    if data:
        if os.path.exists('./timetable.csv'):
            df = pd.read_csv('./timetable.csv')
            df2 = pd.DataFrame(data)
            df3 = df.append(df2)
            df3.to_csv('./timetable.csv', index=False)
        else:
            df2 = pd.DataFrame(data)
            df2.to_csv('./timetable.csv', index=False)

        df3 = pd.read_csv('./timetable.csv')
        df3 = df3.drop_duplicates(subset=['student_id', 'subject_id'])
        df3.to_csv('./timetable.csv', index=False)
