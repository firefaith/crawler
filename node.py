#!/usr/bin/python
# ! -*- coding=utf-8 -*-

import ConfigParser as cp
import os, re, sys
import pinyin, uuid
from jinja2 import Environment, PackageLoader
import datetime, copy, shutil, zipfile

reload(sys)
sys.setdefaultencoding('utf-8')


class ConvertHtml(object):
    ''' 读取文件，转换为html保存，同时提取目录 '''

    def __init__(self):
        conf = cp.ConfigParser()
        conf.read('level.conf')
        self.level_map = {}
        self.level_map[conf.get("level1", "j1").decode("utf8")] = 1
        self.level_map[conf.get("level2", "p1").decode("utf8")] = 2
        self.level_map[conf.get("level2", "p2").decode("utf8")] = 2
        self.templates = conf.get("templates", "templates_path")
        env = Environment(loader=PackageLoader(__name__, self.templates))
        env.trim_blocks = True
        env.lstrip_blocks = True
        self.toc_tpl = env.get_template(conf.get("templates", "toc"))
        self.item_tpl = env.get_template(conf.get("templates", "page"))
        self.content_tpl = env.get_template(conf.get("templates", "content"))

    def getlevel(self, text):
        for pattern in self.level_map:
            if re.search(pattern, text):
                return self.level_map[pattern]
        return 0  # content

    def line2p(self, l):
        return "<p>%s</p>" % l

    def line2h(self, l, hx, nid):
        return "<h%d id=\"%s\">%s</h%d>" % (hx, nid, l, hx)

    def navid(self, order_n):
        return "nav-%d" % order_n

    def filename(self, filepath):
        ''' get file's pinyin name and file name'''
        name = os.path.basename(filepath).split(".")[0]
        pname = pinyin.get(name, format="strip")
        pname = pname.replace("(","").replace(")","").replace("（","").replace("）","").replace("～","_")
        return (pname, name)

    def readfilelistfromcate(self, cate_path, input_dir):
        filelist = []
        with open(cate_path, 'r') as f:
            for title in f:
                # scode = chardet.detect(title)['encoding']
                title = title.strip()
                input_path = input_dir + "/" + title + ".txt"
                filelist.append(input_path)
        return filelist

    def readfile(self, dir, decd="gbk"):
        filelist = []
        for root, dirs, files in os.walk(dir, topdown=False):
            for name in files:
                if name.endswith("txt"):
                    filelist.append(os.path.join(root, name).strip().decode(decd))
            for name in dirs:
                filelist += self.readfile(os.path.join(root, name))

        return filelist

    def get_section_item(self, fname, title):
        item = {}
        item['name'] = fname
        item['title'] = title
        item['full'] = "Text/" + fname
        item['media_type'] = "application/xhtml+xml"
        return item

    def write_item(self, data, fname, output_dir):
        output_path = os.path.join(output_dir, "OEBPS", "Text", fname)
        output_f = open(output_path, 'w')
        item_buf = self.item_tpl.render(data)
        output_f.write(item_buf)
        output_f.close()

    def write_toc(self, category, output_dir):
        '''
        write toc
        :param category: list of subcate
        :return:
        '''
        out_toc = open(os.path.join(output_dir, "OEBPS", "toc.ncx"), 'w')
        toc = self.toc_tpl.render({"cates": category})
        out_toc.write(toc)

    def write_content_opf(self, params, output_dir):
        cnt = self.content_tpl.render(params)
        out_cnt = open(os.path.join(output_dir, "OEBPS", "content.opf"), 'w')
        out_cnt.write(cnt)


    def check_output(self, output_dir):
        if os.path.exists(output_dir) :
            shutil.rmtree(output_dir)
            print "clear output dir:", output_dir
            #os.makedirs(output_dir)
            #print "create output dir:", output_dir

    def preprocess(self, line):
        line = line.decode("utf8").strip()
        line = line.replace("<", "(")
        line = line.replace(">", ")")
        return line

    def copy_template(self, output_dir):
        # copy templates files to output_dir
        #os.system('cp -r ' + self.templates + '/epubtmp ' + output_dir + '/')
        shutil.copytree(os.path.join(self.templates,"epubtmp"),output_dir)

    def zipdir(self,path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))
            for dir in dirs:
                self.zipdir(os.path.join(root,dir),ziph)

    def zipfile(self,input,output):
        zipf = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)
        self.zipdir(input, zipf)
        zipf.close()

    def pack_epub(self, output_dir, book_name):
        self.zipfile(output_dir,os.path.join(output_dir,book_name+".epub"))
        print 'Completed!'

    def convert(self, filepathlist, params, output_dir):
        ''' 一个文件对应一个html文件,title1,..,titlen or named by file name'''

        self.check_output(output_dir)
        self.copy_template(output_dir)
        title = params["title"]
        order = 0
        title_id = self.navid(order)
        title_html = self.line2h(title, 1, title_id)
        # html.append(title_html)
        cate = []
        sections = []
        for filepath in filepathlist:
            sub_order = order + 1
            sub_pname, sub_name = self.filename(filepath)
            print "file name",sub_name
            sub_outf = "%s.html" % sub_pname
            sub_id = self.navid(sub_order)
            sub_src_url = "Text/%s#%s" % (sub_outf, sub_id)

            sub_html = self.line2h(sub_name, 1, sub_id)
            binfo = BaseInfo(level=0, label=sub_name, content_src=sub_src_url, order=sub_order)
            sub_cate = Category(baseInfo=binfo)

            fhtml = [sub_html]

            sections.append(self.get_section_item(sub_outf, sub_name))

            with open(filepath, 'r') as f:
                for line in f:
                    cline = self.preprocess(line)
                    level = self.getlevel(cline)
                    if level == 0:
                        fhtml.append(self.line2p(cline))
                    else:
                        sub_order += 1
                        nid = self.navid(sub_order)
                        fhtml.append(self.line2h(cline, level, nid))

                        src_url = "Text/%s#%s" % (sub_outf, nid)
                        binfo = BaseInfo(level=level, label=cline, order=sub_order, content_src=src_url)
                        sub_cate.add_node(baseInfo=binfo)

                # output html
                out = {"content": fhtml, "title": sub_name}
                self.write_item(out, sub_outf, output_dir)
                # add to category
                cate.append(sub_cate)
        # output category
        self.write_toc(cate, output_dir)
        # output content opf
        params['files'] = sections[:]
        self.write_content_opf(params, output_dir)
        self.pack_epub(output_dir, title)
        return ""


class BaseInfo(object):
    def __init__(self, level, label, order=0, content_src=None):
        # order num as global order, label as category label,content src as html link in html
        self.order = order
        self.label = label
        self.content_src = content_src
        self.level = level

    def get_level(self):
        return self.level

    def set_level(self, level):
        self.level = level

    def __str__(self):
        # return str(self.__dict__)
        return "{} {} {}".format(self.level, self.label, self.content_src)


# l1  1
#  l1.1 2
#  l1.2 2
#    l1.2.1 3
#    l1.2.2 3
#  l1.3 2
# l2 1
class Category(object):
    def __init__(self, baseInfo):
        self.nodes = []  # sub category
        self.baseInfo = baseInfo

    def level(self):
        return self.baseInfo.get_level()

    def set_level(self, level):
        self.baseInfo.set_level(level)

    # def __str__(self):

    # 增加子目录，判断是最后一个目录的子目录，还是当前的子目录
    # 当前，则直接append
    # 最后一个的，则添加至最后一个
    def add_node(self, baseInfo):
        node = Category(baseInfo)
        self.add_sub(node)

    def add_sub(self, node):
        if len(self.nodes) == 0:  # first node
            # print "=0",node.baseInfo
            self.nodes.append(node)  # append node
        elif node.level() > self.nodes[-1].level():  # level 1 to n,
            # print ">"
            self.nodes[-1].add_sub(node)
        elif node.level() == self.nodes[-1].level():
            # print "=="
            self.nodes.append(node)
        else:  # node.level > nodes[-1].level
            # print ">"
            node.set_level(self.nodes[-1].level())
            self.nodes.append(node)

    def outp(self, n, node):
        outline = ["%s%s" % (" " * n, str(node.baseInfo))]
        for cell in node.nodes:
            lines = self.outp(n + 1, cell)
            outline.extend(lines)
        return outline

    def __str__(self):
        outline = self.outp(1, self)
        return "\n".join(outline)


class BookMeta(object):
    def __init__(self):
        self.title = None
        self.creator = os.environ['username']  # os.environ['USER']
        self.identifier = uuid.uuid1()
        self.description = None
        self.publisher = None
        self.date = datetime.datetime.now().strftime('%y-%m-%d');

    def getParams(self):
        params = {}
        x = self.__dict__
        for k in x:
            if x[k] is not None:
                params[k] = x[k]
        return params


if __name__ == "__main__":
    """
    n1 = Category(BaseInfo(1, "t1_start"))
    n1.add_node(BaseInfo(2, "t2.1"))
    n1.add_node(BaseInfo(3, "t3.1"))
    n1.add_node(BaseInfo(3, "t3.2"))
    n1.add_node(BaseInfo(2, "t2.2"))
    n1.add_node(BaseInfo(4, "t2.2.1.1"))
    n1.add_node(BaseInfo(3, "t2.2.1"))
    n1.add_node(BaseInfo(2, "t2.3"))
    
    # n1.add_node(1,"t1_end")
    print n1
    """

    ch = ConvertHtml()
    # cate_path = "/Users/admin/Public/workplace/pyproj/crawler/cate/lsfs.cate"
    # input_dir = "/Users/admin/Public/workplace/pyproj/crawler/book_raw_data/outglz"
    # filelist = ch.readfilelistfromcate(cate_path,input_dir)
    # ch.convert(filelist, "鸠摩罗什法师译丛",output_dir="tmp")

    name = "dzj"
    # cate_path = "/Users/admin/Public/workplace/pyproj/crawler/cate/%s.cate" % name
    input_dir = os.path.join(os.getcwd(), "book_raw_data", name,"大乘华严部".decode("utf8").encode("gbk"))
    output_dir = os.path.join(os.getcwd(), "epub", "dzj-hy")
    # filelist = ch.readfilelistfromcate(cate_path,input_dir)
    filelist = ch.readfile(input_dir)
    print input_dir
    for f in filelist:
        print f
    bookinfo = BookMeta()
    bookinfo.title = "大藏经-大乘华严部"
    bookinfo.creator = "世尊"
    bookinfo.description = "《乾隆大藏经》为清代官刻汉文大藏经，亦称《清藏》，又因经页边栏饰以龙纹名《龙藏》。它始刻于清雍正十一年（1733），完成于乾隆三年（1738）。全藏共收录经、律、论、杂著等1669部，7168卷。"
    bookinfo.publisher = "firefaith"
    params = bookinfo.getParams()

    ch.convert(filelist, params, output_dir=output_dir)
