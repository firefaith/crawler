# -*- coding:utf-8 -*-
import scrapy
import sys, os

reload(sys)
sys.setdefaultencoding('utf-8')

os.listdir()
class MySpider(scrapy.Spider):
    name = 'cbd'
    # request this url
    host_url = 'http://marxistphilosophy.org/ChenBoda/120601/'
    start_urls = ['http://marxistphilosophy.org/ChenBoda/120601/000.htm']
    titles = []
    urls = []

    def __init__(self):
        print("mkdir {}/doc".format(self.name))
        dir = "{}/doc".format(self.name)
        if (os.path.exists(dir) == False):
            os.makedirs(dir)

    def formatStr(self, s):
        return s.encode("latin1").decode("gbk").strip().replace("\n", "").replace("    ", "")

    # callback function
    def parse(self, response):
        out = open('{}/cate.txt'.format(self.name), 'w')
        for title in response.css('blockquote a::text').extract():
            st = self.formatStr(title)
            if st != None:
                out.write(st + "\n")
                self.titles.append(st)
        out.close()
        s=""
        s[-1]
        for href in response.css('blockquote a::attr(href)').extract():
            sub_url = self.host_url + href
            print sub_url
            self.urls.append(sub_url)
            # call another function
        for i in range(len(self.urls)):
            title = self.titles[i]
            url = self.urls[i]
            yield scrapy.Request(url, callback=self.parse_sub, meta={'title': title})

    def parse_sub(self, response):
        title = response.meta['title']
        # title = unicode(title,'utf-8')
        name = "{}/doc/".format(self.name) + title.strip() + ".txt"
        print name
        out = open(name, 'w')
        lines = response.css('body p font::text').extract()
        for l in lines:
            # print l
            nl = l.strip()
            if nl != '':
                out.write(nl + "\n")
                # yield {
                #  'title': response.css('.top h2').extract_first(),
                # 'content': response.css('.content p::text').extract_first(),
                # }
