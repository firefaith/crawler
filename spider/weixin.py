#coding:utf-8
import scrapy
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')
# 
# 1512121089&ver=1
# 
class MySpider(scrapy.Spider):
    name = 'weixin'
    # request this url
    
    ts = datetime.datetime.now().strftime('%s')
    signature = '9gf9dMQklxhyq2H9eyv-sLOD2iTu5QZyUcn2*p-AFvWf67Xlp3Ec-Wd*qfuw*8cbX9Q*kS6*6-VMyG51rEZ1ig=='
    lvjian_url = 'https://mp.weixin.qq.com/profile?src=3&timestamp={}&signature={}'.format(ts,signature)
    start_urls = [lvjian_url]
    host_url = 'https://mp.weixin.qq.com/profile?'
    # callback function
    def parse(self, response):
        #for href in response.css('div h4#weui_media_title::attr(href)').extract():
        for href in response.css('div h4::text').extract():
            sub_url = self.host_url + href
            print sub_url
            # call another function
            #yield scrapy.Request(sub_url, callback=self.parse_sub)
    def parse_sub(self, response):
        title = response.css('td p b font::text').extract_first()
        #title = unicode(title,'utf-8')
        name = "doc/"+title.strip()+".txt"
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
