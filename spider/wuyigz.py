#!/usr/bin/python

#
ex_url="https://search.51job.com/list/020000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="

#coding:utf-8
import scrapy
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
import shutil
class MySpider(scrapy.Spider):
    name = 'shzbl' # 伤寒杂病论
    # request this url
    n_url = 1
    ex_url="https://search.51job.com/list/020000,000000,0000,00,9,99,python,2,"
    param_url="lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="

    host_url = 'https://www.baikedang.com/'
    start_urls = ['https://www.baikedang.com/book/ShangHanZaBingLun']
    output_dir = "../book_raw_data/%s" % name
    cate_name = "../cate/%s.cate" % name
    cate_alink_pattern = "div.xs_contenct ul.bookml1 li a"

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
        cate_out = open(self.cate_name,'w')

        for title in response.css("%s::text" % self.cate_alink_pattern).extract():
          print title
          cate_out.write(title.strip()+"\n")
        cate_out.close()

        for href in response.css('%s::attr(href)' % self.cate_alink_pattern).extract():
            sub_url = self.host_url+href
            print sub_url
            # call another function
            yield scrapy.Request(sub_url, callback=self.parse_sub)
            #break
    def parse_sub(self, response):
        title = response.css('head title::text').extract_first()
        title = title.split(" ",-1)[0].strip()
        #title = unicode(title,'utf-8')
        name = self.output_dir+"/"+title+".txt"

        print "Write file",name

        out = open(name,'w')
        #lines = response.css('body div.xsmain p::text').extract()
        # 内嵌的tag也输出为text
        for line in response.css('body div.xsmain p'):
            l = "".join(line.xpath(".//text()").extract())
            l = l.strip()
            if l != "":
              out.write(l)
              out.write("\n")
        #yield {
        #  'title': response.css('.top h2').extract_first(),
          #'content': response.css('.content p::text').extract_first(),
        #}

if __name__ == "__main__":
    from scrapy.cmdline import execute
    execute(['scrapy','runspider','shzbl.py'])
    '''
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(MySpider)
    process.start() # the script will block here until the crawling is finished
    '''
