# coding:utf-8
import scrapy
from scrapy.cmdline import execute
import sys, os

reload(sys)
sys.setdefaultencoding('utf-8')
import shutil


class MySpider(scrapy.Spider):
    name = 'gj'  # guji
    # request this url
    host_url = u'https://guji.supfree.net/'
    start_urls = [u'https://guji.supfree.net/']
    output_dir = "../book_raw_data/%s" % name
    cate_name = "../cate/%s.cate" % name
    cate_alink_pattern = "div.col-md-2 a::attr(href)"
    cate_title_pattern = "div.col-md-2 a::text"

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
        cate_out = open(self.cate_name, 'w')
        titles = []
        hrefs = []
        for title in response.css(self.cate_title_pattern).extract():
            titles.append(title.strip())
        for href in response.css(self.cate_alink_pattern).extract():
            sub_url = self.host_url + href
            hrefs.append(sub_url)
        for i in range(len(titles)):
            title = titles[i]
            # create diretory
            path = os.path.join(self.output_dir, title)
            os.makedirs(path)
            href = hrefs[i]
            print path,href
            yield scrapy.Request(href, callback=self.parse_book, meta={"parent": path})


    def parse_book(self, response):
        hrefs = []
        titles = []
        parent = response.meta['parent']
        for title in response.css("div.row div.col-md-6 a::text").extract():
            titles.append(title)
        for href in response.css("div.row div.col-md-6 a::attr(href)").extract():
            sub_url = self.host_url + href
            hrefs.append(sub_url)
        for i in range(len(titles)):
            sub_url = hrefs[i]
            title = titles[i]
            print "book", sub_url,title
            path = os.path.join(parent, title)
            if not os.path.exists(path.encode("gbk")):
                os.makedirs(path.encode("gbk"))
                yield scrapy.Request(sub_url, callback=self.parse_cate, meta={"parent": path})

    def parse_cate(self, response):
        parent = response.meta["parent"]
        titles = []
        hrefs = []
        for line in response.css('div.row div.col-md-6 a::text').extract():
            titles.append(line.strip())
        for href in response.css('div.row div.col-md-6 a::attr(href)').extract():
            url = self.host_url + href
            hrefs.append(url)
        for i in range(len(titles)):
            title = titles[i]
            url = hrefs[i]
            print "cate",i,title, url
            #yield scrapy.Request(url ,callback=self.parse_content, meta={"parent": parent,"title":title})


    def parse_content(self, response):
        title = response.meta["title"]
        parent = response.meta["parent"]
        # title = unicode(title,'utf-8')
        name = os.path.join(parent, title + ".txt")
        print "Write file", name
        with open(name, 'w') as out:
            ts = response.css("body tr.head td.smalltxt::text").extract()[0]
            ts = ts.strip()
            out.write(ts+"\n")
            for line in response.css('body td.tpc_content::text').extract():
                l = line.strip().encode("utf8")
                if l != "":
                    out.write(l)
                    out.write("\n")
        # yield {
        #  'title': response.css('.top h2').extract_first(),
        # 'content': response.css('.content p::text').extract_first(),
        # }


if __name__ == "__main__":
    filename = sys.argv[0]
    execute(['scrapy', 'runspider', filename,"-a","year=1946"])
