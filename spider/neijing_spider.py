#coding:utf-8
import scrapy
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')

class MySpider(scrapy.Spider):
    name = 'neijing'
    # request this url
    host_url = 'http://www.pharmnet.com.cn'
    start_urls = ['http://www.pharmnet.com.cn/tcm/knowledge/detail/100677.html']
    output_dir = "doc/neijing/"
    def __init__(self):
        if(os.path.exists(self.output_dir)):
          print "exist",self.output_dir
          os.removedirs(self.output_dir)
        os.makedirs(self.output_dir)
        #"上古天真论——《黄帝内经·素问》第一篇_中医药_医药网"
    # callback function
    def parse(self, response):
        out = open('{}_cate.txt'.format(self.name),'w')
        for title in response.css('td[width*="262"] div a::text').extract():
          out.write(title.strip()+"\n")
        out.close()

        for href in response.css('td[width*="262"] div a::attr(href)').extract():
            sub_url = href
            print sub_url
            # call another function
            yield scrapy.Request(sub_url, callback=self.parse_sub)

    def parse_sub(self, response):
        title = response.css('head title::text').extract_first()
        if("--" in title):
            subtitle = title.split("--")[0].strip()
            title_n = title.split("》")[1].split("_")[0]
            title = "{}_{}".format(title_n,subtitle)
        else:
            print "diff Title",title
        #title = unicode(title,'utf-8')
        title = str(title)
        name = self.output_dir+"/"+title.strip()+".txt"
        print name
        #out = open(name,'w')
        lines = response.css('td.maintext font#fontsize div::text').extract()
        for l in lines[:-1]:
            print l
        #    out.write(l.strip())
        #    out.write("\n")
        #yield {
        #  'title': response.css('.top h2').extract_first(),
          #'content': response.css('.content p::text').extract_first(),
        #}
