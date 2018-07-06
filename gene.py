#!/usr/bin/python
#coding:utf-8
import os
import re
import sys
import uuid

from jinja2 import Environment, PackageLoader

reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv)<5:
  print """
  1-category file path
  2-input content files parent path
  3-output path
  4-template path
  5-book name"""
  sys.exit(1)

# read cate
cate_path = sys.argv[1]
input_dir = sys.argv[2]
output_dir = sys.argv[3]
template_dir = sys.argv[4]
book_name = sys.argv[5]

#cate_f = open(cate_path,'r')
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

# level config
zh_n = u'([一二三四五六七八九十百]+)'
h1=u"(\S+)经卷第%s(\S+)" % zh_n
h21=u"(\S+)品第%s之%s" % (zh_n,zh_n)
h22=u"(\S+)品第%s" % (zh_n)
h3=u"(\S+)奉诏译"
#levels = [h1,h2,h3]
levels = {}
levels[h1]=1
levels[h21]=2
levels[h3]=0 # author
levels[h22]=2

def getlevel(text):
  for pattern in levels:
    if re.search(pattern,text):
      return levels[pattern]
  return 0 # content

def getlevels(filepath):
  levels = []
  with open(filepath,'r') as f:
    pos = 0
    for line in f:
      cline = line.decode("utf8").strip()
      level = getlevel(cline)
      levels.append((cline,level))
      pos += 1
  return levels

def line2p(l):
  return "<p>%s<p>" % l
def line2h(l,hx,nid):
  return "<h%d id=%s>%s</h%d>" %(hx,nid,l,hx)
def navid(order_n):
  return "nav-%d" % order_n



# deprecate
def convert2html(text,limit=20,last_order=1):
  if len(text)>limit:
    return (None,"<p>%s</p>" % text)
  else:
    n = getlevel(text)
    print text,n
    if n < 0:
      return (None,"<p>%s</p>" % text)
    else:
      return "<h%d>%s</h%d>" % (n,text,n)
# deprecate
def getContent(input_path,convert=False,order=1):
    content = []
    with open(input_path,'r') as f:
      for cline in f:
        if convert:
          hline = convert2html(cline.decode("utf8").strip())
          content.append(hline)
        else:
          content.append(cline)
    return content
# convert txt to html
no=0
sections=[]
convert_flag = True # convert content to html/h1/h2/h3
with open(cate_path,'r') as f:
  for title in f:
    print title
    #scode = chardet.detect(title)['encoding']
    title = title.strip()
    input_path = input_dir +"/"+ title +".txt"
    item = {}
    item['name'] = "No"+str(no)+".html"
    item['title'] = title
    item['full'] = "Text/"+str(no)+".html"
    #topNode.add_sub(title,item['full'])
    item['media_type'] = "application/xhtml+xml"
    sections.append(item)
    content = getContent(input_path,convert_flag)
    item['content'] = content
    # output page
    if convert_flag:
      item_tpl = env.get_template('raw-line.html')
    else:
      item_tpl = env.get_template('item.html')
    item_buf = item_tpl.render(item)
    output_path = output_dir + "/epubtmp/OEBPS/Text/"+ str(no) +".html"
    output_f = open(output_path,'w')
    output_f.write(item_buf)
    output_f.close()
    no = no + 1
        

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
