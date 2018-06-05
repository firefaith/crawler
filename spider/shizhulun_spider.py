#coding:utf-8
import scrapy
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')

class MySpider(scrapy.Spider):
    name = 'dzdl'
    # request this url
    host_url = 'http://fofa.foxue.org/fjyw/sutra_sjlb/610/'
    start_urls = ['http://fofa.foxue.org/fjyw/sutra_sjlb/610/']
    output_dir = "doc"
    os.removedirs(output_dir)
    os.mkdir(output_dir)
    # callback function
    def parse(self, response):
        out = open('cate.txt','w')
        for title in response.css('dl#ahtcy_list_right dd a::text').extract():
          print title
          out.write(title.strip()+"\n")
        out.close()

        for href in response.css('dl#ahtcy_list_right dd a::attr(href)').extract():
            sub_url = href
            print sub_url
            # call another function
            yield scrapy.Request(sub_url, callback=self.parse_sub)
    def parse_sub(self, response):
        title = response.css('body div dd#Article h2::text').extract_first()
        title = title.strip()
        #title = unicode(title,'utf-8')
        name = self.output_dir+"/"+title.strip()+".txt"
        print name
        out = open(name,'w')
        lines = response.css('body div.ahtcy_content p::text').extract()
        for l in lines:
            print l
            out.write(l.strip())
            out.write("\n")
        #yield {
        #  'title': response.css('.top h2').extract_first(),
          #'content': response.css('.content p::text').extract_first(),
        #}
