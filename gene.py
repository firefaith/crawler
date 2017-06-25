#!/usr/bin/env python2
#coding:utf-8
import sys,os
from jinja2 import Template
from jinja2 import Environment,PackageLoader
import chardet
import uuid
reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv)<5:
  print "1-category file path,2-input content files parent path,3-output path"
  print "4-template path"
  print "5-book name"
  sys.exit(1)

# read cate
cate_path = sys.argv[1]
input_dir = sys.argv[2]
output_dir = sys.argv[3]
template_dir = sys.argv[4]
book_name = sys.argv[5]

cate_f = open(cate_path,'r')
# load templates
if (os.path.exists(template_dir)==False):
  print 'no templates dir:',template_dir
  sys.exit(1)
env = Environment(loader=PackageLoader(__name__, template_dir))  
env.trim_blocks = True
env.lstrip_blocks = True

# check output dir
if (os.path.exists(output_dir)==False):
  os.makedirs(output_dir)
  print "create output dir:",output_dir
else:
  os.system('rm -rf '+output_dir+"/*")
  print "clear output dir:", output_dir

# copy templates files to output_dir
os.system('cp -r ' + template_dir + '/epubtmp ' + output_dir+'/')

# convert txt to html
no=0
sections=[]
while 1:
    lines = cate_f.readlines(100)
    if not lines:
        break
    for title in lines:
        print title
        #scode = chardet.detect(title)['encoding']
        title = title.strip()
        input_path = input_dir +"/"+ title +".txt"
        output_path = output_dir + "/epubtmp/OEBPS/Text/"+ str(no) +".html"
        item = {}
        item['name'] = "No"+str(no)+".html"
        item['title'] = title
        item['full'] = "Text/"+str(no)+".html"
        item['media_type'] = "application/xhtml+xml"
        sections.append(item)
        no = no + 1
        input_f = open(input_path,'r')
        output_f = open(output_path,'w')
        content = []
        while 1:
          content_lines = input_f.readlines(10000)
          if not content_lines:
              break
          for cline in content_lines:
            content.append(cline)
        item['content'] = content
        item_tpl = env.get_template('item.html')
        # output page
        item_buf = item_tpl.render(item)
        output_f.write(item_buf)
        output_f.close()
        input_f.close()

# output toc
params={}
params['sections'] = sections[:]
params['spine'] = sections[:]
params['files'] = sections[:]
params['title'] = book_name
params['creator'] = os.environ['USER']
#params['publisher'] = book_name
params['identifier'] = uuid.uuid1() 

# output
out_toc = open(output_dir+'/epubtmp/OEBPS/toc.ncx','w')
out_cnt = open(output_dir+'/epubtmp/OEBPS/content.opf','w')
toc_tpl = env.get_template('00_toc.ncx')
cnt_tpl = env.get_template('00_content.opf')

toc = toc_tpl.render(params)
cnt = cnt_tpl.render(params)

out_toc.write(toc)
out_toc.close()

out_cnt.write(cnt)
out_cnt.close()


# pack  to epub

os.system('cd '+output_dir+'/epubtmp && zip -r '+book_name+'.epub ' + './* && mv '+book_name+".epub ../")
print 'Completed!'
