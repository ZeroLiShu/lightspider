#! /usr/bin/python
# -*- coding: utf-8 -*-
from urllib2 import Request, urlopen, URLError, HTTPError
import re, socket

class page_helper:
	""""basic page operations"""
	
	def get_page_content(self, url, headers={}, timeout=0):
		req = Request(url, headers=headers)
		try:
			response = urlopen(req, timeout)
			return response.info(), response.read()
		except URLError, e:
			if hasattr(e, 'code'):
				print 'The server couldn\'t fulfill the request.'
				print 'Error code: ', e.code
			elif hasattr(e, 'reason'):
				print 'We failed to reach a server.'
				print 'Reason: ', e.reason
			return
		except socket.error:
			print('socket.error: %s'%jpg_link)
			return

	def get_href_id(self, href):
		href_split = href.split('/')
		last = len(href_split) - 1
		href_id = href_split[last].strip('.html')
		return href_id

class page_avgirls_helper(page_helper):
	"""page operations"""
	
	def get_detailpage_href_from_indexpage(self, index_html):
		href_match = re.compile(r"htm_data/\d+/\d+/\d+\.html")
		return list(set(href_match.findall(index_html)))
	
	def get_pic_href_from_detailpage(self, detail_html):
		pic_match = re.compile(r"http://.+?\.jpg")
		return list(set(img_id.findall(detail_html)))

	def get_bt_href_from_detailpage(self, detail_html):
		bt_match = re.compile(r"http://www\.jandown\.com/link\.php\?ref=[a-zA-Z0-9]+")
		return list(set(bt_id.findall(detail_html)))
