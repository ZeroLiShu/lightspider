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
'''

HOST_URL = 'http://208.94.244.98/bt/'

def main():
    try:
        options,args = getopt.getopt(sys.argv[1:],"hu:i:",["help","url=","index="])
    except getopt.GetoptError:
        sys.exit()

    url = HOST_URL
    index = 1
    for name, value in options:
        if name in ('-h', '--help'):
            usage()
        elif name in ('-u', '-url'):
            url = value
        elif name in ('-i', '-index'):
            index = value


main()
