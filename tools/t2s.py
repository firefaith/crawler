# -*- coding=utf8 -*-
from zh_wiki import *
import json
t2s={"羅":"罗","經":"经"}
for k in zh2Hans:
    if len(k)==3:
        t2s[k.decode("utf-8")] = zh2Hans.get(k).decode("utf-8")
    else:
    	print k,len(k)

print t2s

def tran2simp(sentence):
	s=[]
	for w in sentence.decode("utf-8"):
		s.append(t2s.get(w,w))
	return "".join(s).encode("utf-8")
