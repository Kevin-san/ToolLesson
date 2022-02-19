#!/usr/bin/env python

from alvintest import testspider
from alvinspider import videospider

if __name__ == '__main__':
    videospider.main()
    testspider.test_groupspider_download_spider_results()
    