#!/bin/bash

mkdir -p /usr/local/core_pdf_page/media
ln -s /mnt/in/音频 /usr/local/core_pdf_page/media/audio
ln -s /mnt/in/图片 /usr/local/core_pdf_page/media/img
ln -s /mnt/in/视频 /usr/local/core_pdf_page/media/video
ln -s /mnt/in/小说 /usr/local/core_pdf_page/media/novel
ln -s /mnt/in/学习 /usr/local/core_pdf_page/media/learn
ln -s /mnt/in/博客 /usr/local/core_pdf_page/media/blog
rm -f /usr/local/core_pdf_page/media/audio
rm -f /usr/local/core_pdf_page/media/img
rm -f /usr/local/core_pdf_page/media/video
rm -f /usr/local/core_pdf_page/media/novel
rm -f /usr/local/core_pdf_page/media/learn
rm -f /usr/local/core_pdf_page/media/blog
rm -rf /usr/local/core_pdf_page/*

cp -r /root/workspace/CorePdfPage/templates /usr/local/core_pdf_page
cp -r /root/workspace/CorePdfPage/static /usr/local/core_pdf_page
python3 /root/workspace/CorePdfPage/application/setup.py install
python3 /root/workspace/CorePdfPage/core/setup.py install
cp /root/workspace/CorePdfPage/manage.py /usr/local/core_pdf_page
cp /root/workspace/CorePdfPage/server.crt /usr/local/core_pdf_page
cp /root/workspace/CorePdfPage/startservice.sh /usr/local/core_pdf_page
cp /root/workspace/CorePdfPage/init_env.profile /usr/local/core_pdf_page
