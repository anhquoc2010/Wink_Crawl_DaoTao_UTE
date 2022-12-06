import time
import os

cd_noti = 'crawl_noti_daotao_ute'
cd_scrapy = 'crawl_noti_daotao_ute\spiders'
get_data = 'scrapy crawl crawl_noti_daotao_ute'

while True:
    print("STATUS: START CRAWL DATA")
    if os.path.exists(cd_noti):
        if os.path.exists(cd_scrapy):
            os.system(get_data)
        else:
            os.chdir(cd_noti)
            os.system(get_data)
    print("STATUS: STOP")
    print("WAIT 5 MINUTES")
    time.sleep(5*60)