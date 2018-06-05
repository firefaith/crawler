# -*- coding=utf-8 -*-
#!/usr/bin/python
# === format gaolizang buddism 
import sys,os
from t2s import *
ipath = sys.argv[1]
#fname = sys.argv[1]
opath = sys.argv[2]



endSymbol = ["。",".","?","？"]


def is_title(sentence):
    if "品第" in sentence or "经卷第" in sentence or "奉诏译" in sentence:
        return True
    return False 

def format(fname,oname):
    with open(oname,'w') as outf:
        bufline = []
        with open(fname,'r') as f:
          for l in f:
              fl = l.strip()
              if fl != '':
                  fl = tran2simp(fl)
              if is_title(fl):
                  outf.write(fl+"\n")
              elif fl != '' and fl[-1] in endSymbol:
                bufline.append(fl)
                outf.write("".join(bufline)+"\n")
                bufline = []
              else:
                bufline.append(fl)

for root, dirs, files in os.walk(ipath, topdown=False):
    for name in files:
        fname = os.path.join(root, name)
        oname = "{}/{}".format(opath,name)
        format(fname,oname)
        print "output",oname
