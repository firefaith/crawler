#! -*-coding=utf-8 -*-
#! /usr/bin/python
import scrapy
import sys,os
#reload(sys)
#sys.setdefaultencoding('utf-8')
import shutil

class MySpider(scrapy.Spider):
    name = 'hdnj' # 皇帝内经
    # request this url
    host_url = 'https://www.gushiwen.org/'
    start_urls = ['https://www.gushiwen.org/guwen/huanglei.aspx']
    output_dir = "../book_raw_data/%s" % name
    cate_name = "../cate/%s.cate" % name
    cate_alink_pattern = "div.bookcont div span a"

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
          cate_out.write(title.strip().encode("utf8")+"\n")
        cate_out.close()

        for href in response.css('%s::attr(href)' % self.cate_alink_pattern).extract():
            sub_url = href
            #print sub_url
            # call another function
            yield scrapy.Request(sub_url, callback=self.parse_sub)
            #break
    def parse_sub(self, response):
        title = response.css('div.main3 div.left div.sons div.cont h1 span b::text').extract_first()
        title = title.split(u"·",-1)[-1].strip().encode("utf8")
        #title = unicode(title,'utf-8')
        name = self.output_dir+"/"+title+".txt"

        print "Write file",name

        out = open(name,'w')
        lines = response.css('div.main3 div.left div.sons div.cont div.contson p::text').extract()
        # 内嵌的tag也输出为text
        for line in lines:
            l = line.strip().encode("utf8")

            if l != "":
              out.write(l)
              out.write("\n")
        #yield {
        #  'title': response.css('.top h2').extract_first(),
          #'content': response.css('.content p::text').extract_first(),
        #}


if __name__ == "__main__":
    from scrapy.cmdline import execute
    filename = sys.argv[0]
    execute(['scrapy','runspider',filename])

