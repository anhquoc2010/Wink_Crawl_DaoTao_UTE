import logging
import scrapy
from crawl_noti_daotao_ute.items import CrawlNotiDaotaoUteItem
from get_noti_from_db import is_old_notification

class CrawlNotiDaotaoUteSpider(scrapy.Spider):
    name = "crawl_noti_daotao_ute"

    def start_requests(self):
        urls = [
            'http://daotao.ute.udn.vn/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        notis = response.css('#pagemain > a[style]')
        next_page = response.css('#inner-column-container > div:nth-child(2) a:last-child')
        for noti in (notis):
            getdata = noti.css('a::attr(href)').get()
            print(getdata)
            if(is_old_notification(getdata.split('mid=')[-1])):
                logging.info("[!] OLD_DATA STOP !!")
                return
            yield scrapy.Request(url='http://daotao.ute.udn.vn/'+getdata, callback=self.get_noti)

        next_page = next_page[-1].css('a::attr(href)').get()
        print(next_page)
        yield scrapy.Request(url='http://daotao.ute.udn.vn/'+next_page,callback=self.parse)

    def get_noti(self, response):
        noti_db = CrawlNotiDaotaoUteItem()
        main_noti = response.css("#pagemain > table:nth-child(2)")
        for noti in main_noti:
            noti_db['id'] = response.url.split('mid=')[-1]
            title = noti.css('font b::text').get()
            noti_db['title']= title.strip()
            content = noti.css('tr:nth-child(2) td[style]::text').get()
            noti_db['content'] = content.strip()
            yield noti_db
            