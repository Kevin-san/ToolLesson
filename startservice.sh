#!/bin/bash


docker rm $(docker ps -a -q)
docker run -dit --name node-test node
docker run -dit --name golang-test golang
docker run -dit --name python-test python
docker run -dit --name perl-test perl
docker run -dit --name bash-test centos
docker run -dit --name java-test java
python3 /usr/local/core_pdf_page/manage.py

