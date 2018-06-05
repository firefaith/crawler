#!/usr/bin/python
#coding:utf-8
import sys,os

print "hello"

print sys.argv[1]
inputf_name = sys.argv[1]
inputf = open(inputf_name,'r')

while(1):
  lines = inputf.readlines(1000)
  if not lines:
    break
  for line in lines:
    #print line.find("品")
    if(line.find("品第")!=-1):
       print line
    if(line.find("卷第")!=-1):
       print line
    
