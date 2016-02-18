#! /usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3

class db_avgirls_helper:
	"""database operations for av bt girls
		import db_wrapper

		helper = db_wrapper.db_avgirls_helper('test.s3db')
		helper.create_db()

		row_list = [
			("1", "www.test.com", ""),
			("2", "www.test.com", ""),
		]

		helper.update_detail_link_table(row_list)
		link_id_list = helper.get_all_link_id()
		print link_id_list
	"""
	#private:
	_dbname = ""
	
	def __init__(self, dbname):
		self._dbname = dbname

	def create_db(self):
		conn = sqlite3.connect(self._dbname)
		# Create table
		conn.execute('''create table if not exists detail_link(link_id text PRIMARY KEY, link_href text, link_pic buffer)''')
		# Save (commit) the changes
		conn.commit()
		# We can also close the cursor if we are done with it
		conn.close()
	
	def get_all_link_id(self):
		conn = sqlite3.connect(self._dbname)
		link_id_list = []
		for row in conn.execute('''select link_id from detail_link'''):
			link_id_list.append(row[0])
		return link_id_list
	
	def update_detail_link_table(self, row_list):
		conn = sqlite3.connect(self._dbname)
		conn.executemany('''replace into detail_link(link_id, link_href, link_pic) values(?, ?, ?)''', row_list)
		conn.commit()
		conn.close()
