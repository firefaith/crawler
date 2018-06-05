#coding:utf-8
import scrapy
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')

class MySpider(scrapy.Spider):
    name = 'dzdl'
    # request this url
    host_url = 'http://www.zysj.com.cn/'
    start_urls = ['http://www.zysj.com.cn/lilunshuji/sishengxinyuan/index.html']
    output_dir = "doc"
    os.removedirs(output_dir)
    os.mkdir(output_dir)
    # callback function
    def parse(self, response):
        out = open('cate.txt','w')
        for title in response.css("ul#table-of-contents li[data-cc^='1'] a::text").extract():
          print title
          out.write(title.strip()+"\n")
        out.close()

        for href in response.css('ul#table-of-contents li a::attr(href)').extract():
            if(href.find("#")==-1):
               sub_url = self.host_url+href
               #print sub_url
            # call another function
               #yield scrapy.Request(sub_url, callback=self.parse_sub)
    def parse_sub(self, response):
        title = response.css('head title::text').extract_first()
        title = title.split("_",-1)[1].strip()
        #title = unicode(title,'utf-8')
        name = self.output_dir+"/"+title.strip()+".txt"

        print "Write file",name

        out = open(name,'w')
        lines = response.css('body div#content p::text').extract()
        for l in lines:
            print l
            out.write(l.strip())
            out.write("\n")
        #yield {
        #  'title': response.css('.top h2').extract_first(),
          #'content': response.css('.content p::text').extract_first(),
        #}
