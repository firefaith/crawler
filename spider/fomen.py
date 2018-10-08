# coding:utf-8
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
    start_urls = [u'http://www.fomen123.com/dzj/']
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
        self.keep_dir(self.output_dir)
        cate_out = open(self.cate_name, 'w')
        titles = []
        hrefs = []
        for title in response.css(self.cate_title_pattern).extract():
            print title
            titles.append(title.strip())

        for href in response.css(self.cate_alink_pattern).extract():
            sub_url = self.host_url + href
            print sub_url
            hrefs.append(sub_url)
        for i in range(len(titles)):
            title = titles[i]
            # create diretory
            path = "%s/%s" % (self.output_dir, title)
            os.makedirs(path)
            href = hrefs[i]
            yield scrapy.Request(href, callback=self.parse_cate, meta={"parent": path})


    def parse_cate(self, response):
        hrefs = []
        titles = []
        parent = response.meta['parent']
        for title in response.css("td div a::text").extract():
            titles.append(title)
            print title
        for href in response.css("td div a::attr(href)").extract():
            sub_url = self.host_url + href.replace("../", "")
            hrefs.append(sub_url)
            print sub_url
        headers = {
            "Host": "www.fomen123.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Cookie": "AJSTAT_ok_times=1; UM_distinctid=16546b74a1614a-0d39505b3e811f-323b5b03-100200-16546b74a172f3; __51cke__=; __tins__2897421=%7B%22sid%22%3A%201534549641047%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201534551441047%7D; __51laig__=4; CNZZDATA2436867=cnzz_eid%3D1450641568-1534516301-http%253A%252F%252Fwww.fomen123.com%252F%26ntime%3D1534549558",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }

        for i in range(len(titles)):
            title = titles[i]
            href = hrefs[i]
            yield scrapy.Request(href ,headers=headers,callback=self.parse_content, meta={"parent": parent,"title":title})


    def parse_content(self, response):
        title = response.meta["title"]
        parent = response.meta["parent"]
        # title = unicode(title,'utf-8')
        name = parent + "/" + title + ".txt"
        print "Write file", name
        out = open(name, 'w')
        # lines = response.css('body div.xsmain p::text').extract()
        # 内嵌的tag也输出为text
        for line in response.css('body td.style p::text').extract():
            #l = "".join(line.xpath(".//text()").extract())
            #print l
            l = line.strip().encode("utf8")
            if l != "":
                out.write(l)
                out.write("\n")
        # yield {
        #  'title': response.css('.top h2').extract_first(),
        # 'content': response.css('.content p::text').extract_first(),
        # }


if __name__ == "__main__":
    execute(['scrapy', 'runspider', 'fomen.py'])
