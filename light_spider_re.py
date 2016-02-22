#! /usr/bin/python
# -*- coding: utf-8 -*-
import zip_wrapper, os_wrapper, page_wrapper, db_wrapper, time

#constant
HOST_URL = 'http://208.94.244.98/bt/'
START_URL = HOST_URL + 'thread.php?fid=4&page='
DB_NAME = 'lightspider.s3db'
MAX_SIZE = 1000*1000*100
MAX_PAGE_INDEX = 10

ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
ACCEPT_ENCODING = 'gzip, deflate, sdch'
ACCEPT_LANGUAGE = 'zh-CN,zh;q=0.8'
CACHE_CONTROL = 'max-age=0'
CONNECTION = 'keep-alive'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36'

HEADERS = { 'User-Agent' : USER_AGENT,
    'Accept' : ACCEPT,
    'Accept-Encoding' : ACCEPT_ENCODING,
    'Cache-Control' : CACHE_CONTROL,
    'Connection' : CONNECTION,
}

#helper
pagehelper = page_wrapper.page_avgirls_helper()
ziphelper = zip_wrapper.tar_helper()
dbhelper = db_wrapper.db_avgirls_helper(DB_NAME)

#spider class
class spider_index_detail:
	"""spider for crawling index page and following detail pages"""
	
	#public:

	def iterate_index_page(self, istart, iend):
		detail_href_list = []
		for index in range(istart, iend):
			iter_href_list = self._index_page(index)
			if iter_href_list == None:
				continue
			detail_href_list.extend(iter_href_list)
			time.sleep(0.1) # sleep 100ms
			print('extend detail_href_list by %d links'%(len(detail_href_list)))
		return detail_href_list

	def iterate_detail_page(self, href):
		href_id = pagehelper.get_href_id(href)
		info, content = pagehelper.get_page_content(HOST_URL + href, HEADERS, 3)
		if info == None or content == None:
			return None
		
		pic_list = pagehelper.get_pic_href_from_detailpage(content)
		bt_list = pagehelper.get_bt_href_from_detailpage(content)
		self._detail_page_download(href_id, pic_list, bt_list)
		return href_id
	
	#private:

	def _iterate_detail_page(self, detail_href_dict):
		for href_id, href in detail_href_dict.iteritems():
			self._detail_page(href_id, href)
			time.sleep(0.1)

	def _iterate_store_download(self, detail_href_dict):
		row_list = []
		total_size = 0
		for href_id, href in detail_href_dict.iteritems():
			#load .tar.gz file to memory
			size, content = os_wrapper.read_file(".", href_id + ".tar.gz")
			#create a new row and add to the dict
			row_list.append((href_id, href, content))
			#check if memory size is big, store to the database
			total_size += size
			if total_size > MAX_SIZE:
				dbhelper.update_detail_link_table(row_list)
				row_list = []
		#final store
		dbhelper.update_detail_link_table(row_list)

	def _index_page(self, index):
		info, content = pagehelper.get_page_content(START_URL + str(index), HEADERS, 3)
		if info == None or content == None:
			return None
		
		if info['Content-Encoding'] == "gzip":
			content = zip_wrapper.gzip_decode_from_bytes(content)
		return pagehelper.get_detailpage_href_from_indexpage(content)

	def _detail_page_download(self, href_id, pic_list, bt_list):
		#make a bundle download directory for href_id
		os_wrapper.check_and_create_dir(href_id)
		#download pictures to local files
		for pic in pic_list:
			info, content = pagehelper.get_page_content(pic, HEADERS, 3)
			if info == None or content == None:
				continue
			
			pic_split = pic.split('/')
			pic_name = pic_split[len(pic_split) - 1]
			os_wrapper.write_file(href_id, pic_name, content)
			time.sleep(0.1)
		#compress the bundle download directory
		#ziphelper.zip_dir(href_id)
