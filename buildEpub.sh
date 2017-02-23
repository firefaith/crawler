#!/usr/bin/env bash
if [ $# -lt 1 ]; then
  echo "1 for epub file name $#"
  exit 1
fi
outF=$1
rm -R epubtmp
rm ${outF}.zip 
cp -R templates/epubtmp ./
cp -R output/* epubtmp/OEBPS/Text/
cp  content.opf epubtmp/OEBPS/
cp  toc.ncx epubtmp/OEBPS/
zip -r ${outF}.zip epubtmp

cp ${outF}.zip ~/Calibre\ 书库/${outF}.epub
