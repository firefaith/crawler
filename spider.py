#coding:utf-8
import scrapy
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')

class MySpider(scrapy.Spider):
    name = 'maoz'
    # request this url
    host_url = 'http://www.xiexingcun.com/maozedong/'
    start_urls = ['http://www.xiexingcun.com/maozedong/index59.htm']
    output_dir = "doc"
    os.removedirs(output_dir)
    os.mkdir(output_dir)
    # callback function
    def parse(self, response):
        out = open('cate.txt','w')
        for title in response.css('td a::text').extract():
          out.write(title.strip()+"\n")
        out.close()

        for href in response.css('td a::attr(href)').extract():
            sub_url = self.host_url + href
            print sub_url
            # call another function
            yield scrapy.Request(sub_url, callback=self.parse_sub)
    def parse_sub(self, response):
        title = response.css('td p b font::text').extract_first()
        #title = unicode(title,'utf-8')
        name = self.output_dir+"/"+title.strip()+".txt"
        print name
        out = open(name,'w')
        lines = response.css('td div div::text').extract()
        for l in lines:
        #    print l
            out.write(l)
        #yield {
        #  'title': response.css('.top h2').extract_first(),
          #'content': response.css('.content p::text').extract_first(),
        #}
