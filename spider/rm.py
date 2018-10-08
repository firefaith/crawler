# coding:utf-8
import scrapy
from scrapy.cmdline import execute
import sys, os

reload(sys)
sys.setdefaultencoding('utf-8')
import shutil
from scrapy.settings import default_settings
default_settings.CONCURRENT_REQUESTS = 100

class MySpider(scrapy.Spider):
    name = 'rm'  # renming
    # request this url
    host_url = u'http://rmrbw.xyz/'
    start_urls = [u'http://rmrbw.xyz/simple/index.php']
    output_dir = "../book_raw_data/%s" % name
    cate_name = "../cate/%s.cate" % name
    cate_alink_pattern = "li a::attr(href)"
    cate_title_pattern = "li a::text"

    @staticmethod
    def keep_dir(path):
        if os.path.exists(path):
            shutil.rmtree(path)
            os.makedirs(path)
        else:
            os.makedirs(path)

    # first entry function
    def parse(self, response):
        year = getattr(self, 'year', None)
        self.keep_dir(self.output_dir)
        cate_out = open(self.cate_name, 'w')
        titles = []
        hrefs = []
        inyear = []
        i = 0
        for title in response.css(self.cate_title_pattern).extract():
            title = title.replace("年", os.sep).replace("月", "")
            if year in title:
                inyear.append(i)
            titles.append(title.strip())
            i+=1

        for href in response.css(self.cate_alink_pattern).extract():
            sub_url = self.host_url + href
            hrefs.append(sub_url)
        for i in inyear:
            title = titles[i]
            # create diretory
            path = os.path.join(self.output_dir, title)
            print path
            os.makedirs(path)
            href = hrefs[i]
            yield scrapy.Request(href, callback=self.parse_pages, meta={"parent": path})


    def parse_pages(self, response):
        hrefs = []
        parent = response.meta['parent']
        for href in response.css("td center a::attr(href)").extract():
            sub_url = self.host_url + href
            hrefs.append(sub_url)
            print "page", sub_url
            yield scrapy.Request(sub_url, callback=self.parse_page, meta={"parent": parent})


    def parse_page(self, response):
        parent = response.meta["parent"]
        titles = []
        hrefs = []
        for line in response.css('li a::text').extract():
            titles.append(line.strip())
        for href in response.css('li a::attr(href)').extract():
            url = self.host_url + href
            hrefs.append(url)
        for i in range(len(titles)):
            title = titles[i]
            url = hrefs[i]
            print title, url
            yield scrapy.Request(url ,callback=self.parse_content, meta={"parent": parent,"title":str(i)+"_"+title})


    def parse_content(self, response):
        title = response.meta["title"]
        parent = response.meta["parent"]
        # title = unicode(title,'utf-8')
        name = os.path.join(parent, title + ".txt")
        print "Write file", name
        #with open(name, 'w') as out:
        ts = response.css("body tr.head td.smalltxt::text").extract()[0]
        ts = ts.strip()
        #out.write(ts+"\n")
        lines = []
        for line in response.css('body td.tpc_content::text').extract():
            l = line.strip().encode("utf8")
            if l != "":
                lines.append(l)
                #out.write(l)
                #out.write("\n")
        yield {
            "ts":ts,
            "title":title,
            "content":"\n".join(lines)
        }

        # yield {
        #  'title': response.css('.top h2').extract_first(),
        # 'content': response.css('.content p::text').extract_first(),
        # }


if __name__ == "__main__":
    execute(['scrapy', 'runspider', 'rm.py',"-a","year=1947 -o renmin.json"])
