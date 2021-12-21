#!/bin/bash

cd /root/workspace/CorePdfPage
mkdir -p /usr/local/core_pdf_page
cp -r /root/workspace/CorePdfPage/templates /usr/local/core_pdf_page
cp -r /root/workspace/CorePdfPage/static /usr/local/core_pdf_page
python3 /root/workspace/CorePdfPage/application/setup.py install
python3 /root/workspace/CorePdfPage/core/setup.py install
cp /root/workspace/CorePdfPage/manage.py /usr/local/core_pdf_page
cp /root/workspace/CorePdfPage/server.crt /usr/local/core_pdf_page
cp /root/workspace/CorePdfPage/server.key /usr/local/core_pdf_page
cp /root/workspace/CorePdfPage/startservice.sh /usr/local/core_pdf_page
cp /root/workspace/CorePdfPage/init_env.profile /usr/local/core_pdf_page
