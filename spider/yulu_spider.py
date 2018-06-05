#coding:utf-8
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MySpider(scrapy.Spider):
    name = 'maoz'
    # request this url
    host_url = 'file:///Users/admin/Downloads/%E6%AF%9B%E6%B3%BD%E4%B8%9C%E8%91%97%E4%BD%9C%E7%94%B5%E5%AD%90%E4%B9%A6/yulu/'
    start_urls = ['file:///Users/admin/Downloads/%E6%AF%9B%E6%B3%BD%E4%B8%9C%E8%91%97%E4%BD%9C%E7%94%B5%E5%AD%90%E4%B9%A6/yulu/index.html']
    # callback function
    def parse(self, response):
        out = open('cate.txt','w')
        for title in response.css('blockquote a::text').extract():
          out.write(title.strip()+"\n")
        out.close()

        for href in response.css('blockquote a::attr(href)').extract():
            sub_url = self.host_url + href
            print sub_url
            # call another function
            yield scrapy.Request(sub_url, callback=self.parse_sub)
    def parse_sub(self, response):
        title = response.css('head title::text').extract_first()
        #title = unicode(title,'utf-8')
        name = "doc/"+title.strip()+".txt"
        print name
        out = open(name,'w')
        lines = response.css('body p::text').extract()
        for l in lines:
          print l
          out.write(l)
        #yield {
        #  'title': response.css('.top h2').extract_first(),
          #'content': response.css('.content p::text').extract_first(),
        #}
