#!/bin/bash

mkdir -p /usr/local/core_pdf_page/media
ln -s /mnt/in/音频 /usr/local/core_pdf_page/media/audio
ln -s /mnt/in/图片 /usr/local/core_pdf_page/media/img
ln -s /mnt/in/视频 /usr/local/core_pdf_page/media/video
ln -s /mnt/in/小说 /usr/local/core_pdf_page/media/novel
ln -s /mnt/in/学习 /usr/local/core_pdf_page/media/learn
ln -s /mnt/in/博客 /usr/local/core_pdf_page/media/blog
ln -s /mnt/in/Spider/Hider /usr/local/core_pdf_page/media/vhider
rm -f /usr/local/core_pdf_page/media/audio
rm -f /usr/local/core_pdf_page/media/img
rm -f /usr/local/core_pdf_page/media/video
rm -f /usr/local/core_pdf_page/media/novel
rm -f /usr/local/core_pdf_page/media/learn
rm -f /usr/local/core_pdf_page/media/blog
rm -f /usr/local/core_pdf_page/media/vhider
rm -rf /usr/local/core_pdf_page/*

cp -r /root/workspace/CorePdfPage/templates /usr/local/core_pdf_page
cp -r /root/workspace/CorePdfPage/static /usr/local/core_pdf_page
python3 /root/workspace/CorePdfPage/application/setup.py install
python3 /root/workspace/CorePdfPage/core/setup.py install
cp /root/workspace/CorePdfPage/manage.py /usr/local/core_pdf_page
cp /root/workspace/CorePdfPage/server.crt /usr/local/core_pdf_page
cp /root/workspace/CorePdfPage/startservice.sh /usr/local/core_pdf_page
cp /root/workspace/CorePdfPage/init_env.profile /usr/local/core_pdf_page

docker run -dit --name node-test node 
docker run -dit --name golang-test golang 
docker run -dit --name python-test python 
docker run -dit --name perl-test perl 
docker run -dit --name bash-test centos 
docker run -dit --name java-test java 

docker run --name node -dit e71b22bd886f
docker run --name golang -dit 37eabbc422cd
docker run --name python -dit a42e2a4f3833
docker run --name perl -dit 3e9417dedf6d
docker run --name bash -dit 5d0da3dc9764
docker run --name java -dit d23bdf5b1b1b

pip install poetry
pip install spleeter
2stems
4stems
5stems
