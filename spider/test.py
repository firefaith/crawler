#! -*- coding:utf-8 -*-
import scrapy
from scrapy.cmdline import execute
import sys, os,chardet,logging
import shutil


class MySpider(scrapy.Spider):

    name = 'dzj'  # 乾隆大藏经
    # request this url
    host_url = 'http://www.fomen123.com/dzj/'
    start_urls = ["file:///C:/Users/Administrator/AppData/Local/Temp/tmpt0xumq.html"]
    output_dir = "../book_raw_data/%s" % name
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
        titles = []
        hrefs = []
        text = response.body
        content_type = chardet.detect(text)
        print response.encoding,content_type
        #print text
        for title in response.css("title::text").extract():
            print type(title),repr(title)
            print title
            #print title.decode()

            break



if __name__ == "__main__":
    execute(['scrapy', 'runspider', 'test.py',"-LERROR"])
