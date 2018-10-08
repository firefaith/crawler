#! -*- coding:utf-8 -*-
import scrapy
from scrapy.cmdline import execute
import sys, os

reload(sys)
sys.setdefaultencoding('utf-8')
import shutil


class MySpider(scrapy.Spider):
    name = 'dzj'  # 乾隆大藏经
    # request this url
    host_url = u'http://www.fomen123.com/dzj/'
    output_dir = "../book_raw_data/%s" % name
    start_urls = ['file:///C:/Users/Administrator/AppData/Local/Temp/tmpazrebe.html']
    cate_name = "../cate/%s.cate" % name
    cate_alink_pattern = "body map area::attr(href)"
    cate_title_pattern = "body map area::attr(title)"

    @staticmethod
    def keep_dir(path):
        if os.path.exists(path):
            shutil.rmtree(path)
            os.makedirs(path)
        else:
            os.makedirs(path)

    # first entry function
    def parse(self, response):
        cate_out = open(self.cate_name, 'w')
        titles = []
        hrefs = []
        for title in response.css(self.cate_title_pattern).extract():
            titles.append(title.strip())

        for href in response.css(self.cate_alink_pattern).extract():
            sub_url = self.host_url + href
            #print sub_url
            hrefs.append(sub_url)
        for i in range(len(titles)):
            title = titles[i]
            # create diretory
            path = "%s/%s" % (self.output_dir, title)
            href = hrefs[i]
            yield scrapy.Request(href, callback=self.parse_cate, meta={"parent": path})


    def parse_cate(self, response):
        hrefs = []
        titles = []
        parent = response.meta['parent']
        for title in response.css("td div a::text").extract():
            titles.append(title)
            #print title
        for href in response.css("td div a::attr(href)").extract():
            sub_url = self.host_url + href.replace("../", "")
            hrefs.append(sub_url)
            #print sub_url


if __name__ == "__main__":
    execute(['scrapy', 'runspider', 'fomen_cate.py'])
