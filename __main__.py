#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import getopt

if not __package__:
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.insert(0, path)

from Queue import Queue
from lightspider.muti_thread_spider import index_spider, detail_spider, zip_spider

def usage():
    print '''
This program use a spider to crawl a website with pages.
usage:
        -h, --help  print usage
        -u, --url website start url
        -s, --sindex start page index
        -e, --eindex end page index
'''

HOST_URL = 'http://208.94.244.98/bt/'
MAX_PAGE_INDEX = 1000

class index_detail_page:

    def __init__(self, host):
        self.host = host

    def get_index_page_url(self, index):
        return self.host + 'thread.php?fid=4&page=' + str(index)

    def get_detail_page_url(self, href):
        return self.host + href


def main():
    try:
        options,args = getopt.getopt(sys.argv[1:],"hu:s:e:",["help","url=","sindex=", "eindex="])
    except getopt.GetoptError:
        sys.exit()

    url = HOST_URL
    sindex = 1
    eindex = MAX_PAGE_INDEX
    for name, value in options:
        if name in ('-h', '--help'):
            usage()
        elif name in ('-u', '--url'):
            url = value
        elif name in ('-s', '--sindex'):
            sindex = int(value)
        elif name in ('-e', '--eindex'):
            eindex = int(value)

    job_queue = Queue()
    zip_queue = Queue()

    web_page = index_detail_page(url)

    spider_p = index_spider("index spider", job_queue, sindex, eindex, web_page)
    spider_p.start()

    spider_m_1 = detail_spider("detail spider 1", job_queue, zip_queue, web_page)
    spider_m_2 = detail_spider("detail spider 2", job_queue, zip_queue, web_page)
    spider_m_3 = detail_spider("detail spider 3", job_queue, zip_queue, web_page)
    spider_m_4 = detail_spider("detail spider 4", job_queue, zip_queue, web_page)
    spider_m_5 = detail_spider("detail spider 5", job_queue, zip_queue, web_page)

    spider_m_1.start()
    spider_m_2.start()
    spider_m_3.start()
    spider_m_4.start()
    spider_m_5.start()

    spider_c_1 = zip_spider("zip spider 1", zip_queue)
    spider_c_2 = zip_spider("zip spider 2", zip_queue)

    spider_c_1.start()
    spider_c_2.start()


    spider_p.join()
    spider_m_1.join()
    spider_m_2.join()
    spider_m_3.join()
    spider_m_4.join()
    spider_m_5.join()
    spider_c_1.join()
    spider_c_2.join()

main()
