#! /usr/bin/python
# -*- coding: utf-8 -*-
from urllib2 import Request, urlopen, URLError, HTTPError
import StringIO, gzip, re, sqlite3, time, os, socket

HOST_URL = 'http://208.94.244.98/bt/'
START_URL = HOST_URL + 'thread.php?fid=4&page='

ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
ACCEPT_ENCODING = 'gzip, deflate, sdch'
ACCEPT_LANGUAGE = 'zh-CN,zh;q=0.8'
CACHE_CONTROL = 'max-age=0'
CONNECTION = 'keep-alive'
#Cookie:c1707_ol_offset=72556; is_use_cookied=yes; is_use_cookiex=yes; c1707_lastpos=F4; c1707_lastvisit=17%091455586985%09%2Fbt%2Fthread.php%3Ffid%3D4%26page%3D1; c1707_threadlog=%2C4%2C
#Host:208.94.244.98
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36'

HEADERS = { 'User-Agent' : USER_AGENT,
    'Accept' : ACCEPT,
    'Accept-Encoding' : ACCEPT_ENCODING,
    'Cache-Control' : CACHE_CONTROL,
    'Connection' : CONNECTION,
}

 
def gzdecode(data):
    compressedstream = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj=compressedstream) 
    data2 = gziper.read()
    return data2

def detail_link_id(detail_link):
    href_split = detail_link.split('/')
    last = len(href_split) - 1
    link_id = href_split[last].strip('.html')
    return link_id
           
def detail_link_gen(match_list):
    for href in match_list:
        link_id = detail_link_id(href)
        yield (link_id, href)

def jpg_link(jpg_link):
    jpg_split = jpg_link.split('=')
    last = len(jpg_split) - 1
    link = jpg_split[last].strip('\"')
    return link

def write_file(dir, filename, content):
    filename=os.path.join(dir, filename)
    f = open(filename, 'wb')
    f.write(content)
    f.close()

def get_img_from_url(dir, jpg_link):
    req = Request(jpg_link, headers=HEADERS)
    try:
        response = urlopen(req, timeout=3)
        info = response.info()
        content = response.read()
    except URLError, e:
        if hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        elif hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
    except socket.error:
        print('socket.error: %s'%jpg_link)
        return
    
    jpg_link_list = jpg_link.split('/')
    img_name = jpg_link_list[len(jpg_link_list) - 1]
    write_file(dir, img_name, content)

def iterate_index_page(index):
    req = Request(START_URL + str(index), headers=HEADERS)
    try:
        response = urlopen(req)
    except URLError, e:
        if hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        elif hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason

    info = response.info()

    html = ""
    if info['Content-Encoding'] == "gzip":
        html = gzdecode(response.read())
    else:
        html = response.read()

    #print html
    #print info
    
    a_id = re.compile(r"htm_data/\d+/\d+/\d+\.html")
    match_id = list(set(a_id.findall(html)))

    return match_id

def iterate_detail_page(detail_link):
    req = Request(HOST_URL + detail_link, headers=HEADERS)
    try:
        response = urlopen(req)
    except URLError, e:
        if hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        elif hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason

    info = response.info()
    html = response.read()

    print info
    img_id = re.compile(r"src=\"http://.+?\.jpg\"")
    match_id = list(set(img_id.findall(html)))
    dir = detail_link_id(detail_link)
    
    if not os.path.exists(dir):
        os.mkdir(dir)
        
    for link in match_id:
        link = jpg_link(link)
        print('get_img_from_url: %s:%s'%(dir, link))
        get_img_from_url(dir, link)
        time.sleep(0.1)

def store_detail_link(match_id):
    conn = sqlite3.connect("./lightspider.s3db")
    c = conn.cursor()
    # Create table
    c.execute('''create table if not exists detail_link(link_id text PRIMARY KEY, link_href text)''')

    c.executemany('''replace into detail_link(link_id, link_href) values(?, ?)''', detail_link_gen(match_id))

    # Save (commit) the changes
    conn.commit()
    # We can also close the cursor if we are done with it
    c.close()

detail_link_list = []
for index in range(1, 2):
    detail_link_list.extend(iterate_index_page(index))
    time.sleep(0.1) # sleep 100ms
    print('extend detail_link_list by %d links'%(len(detail_link_list)))

store_detail_link(detail_link_list)


for detail_link in detail_link_list:
    iterate_detail_page(detail_link)
    time.sleep(0.1) # sleep 100ms

 
