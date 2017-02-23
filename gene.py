#!/usr/bin/env python2
#coding:utf-8
import sys,os
from jinja2 import Template
from jinja2 import Environment,PackageLoader
import chardet
reload(sys)
sys.setdefaultencoding('utf-8')
# read cate
cate_path = sys.argv[1]

cate_f = open(cate_path,'r')
header1="""
<html>
<header>
<title>
"""
header2="""</title>
</header>
<body>
"""
bottom="""
</body>
</html>
"""
no=0
sections=[]
while 1:
    lines = cate_f.readlines(100)
    if not lines:
        break
    for title in lines:
        print title
        #scode = chardet.detect(title)['encoding']
        #print scode
        title = title.strip()
        input_path = "doc/"+ title +".txt"
        output_path = "output/"+ str(no) +".html"
        item={}
        item['name'] = "x"+str(no)+".html"
        item['title']=title
        item['full'] = "Text/"+str(no)+".html"
        item['media_type'] = "application/xhtml+xml"
        sections.append(item)
        no = no + 1
        input_f = open(input_path,'r')
        output_f = open(output_path,'w')
        # write header
        output_f.write(header1)
        output_f.write(title)
        output_f.write(header2+"\n")
        while 1:
          content_lines = input_f.readlines(100)
          if not content_lines:
              # write bottom
              output_f.write(bottom)
              output_f.close()
              input_f.close()
              break
          # write body
          for cline in content_lines:
           output_f.write("<p>"+cline+"</p>\n")
        
# output toc
params={}
params['sections']=sections[:]
params['spine']=sections[:]
params['files']=sections[:]

out_toc = open('toc.ncx','w')
out_cnt = open('content.opf','w')
env = Environment(loader=PackageLoader(__name__, 'templates'))  
env.trim_blocks = True
env.lstrip_blocks = True
toc_tpl = env.get_template('00_toc.ncx')
cnt_tpl = env.get_template('00_content.opf')

toc = toc_tpl.render(params)
cnt = cnt_tpl.render(params)

out_toc.write(toc)
out_toc.close()

out_cnt.write(cnt)
out_cnt.close()


