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
		link_href_list = helper.get_all_link_href()
		print link_href_list
	"""
	#private:
	dbname = ""

	def __init__(self, dbname):
		self.dbname = dbname
		self.create_db()

	def create_db(self):
		conn = sqlite3.connect(self.dbname)
		# Create table
		conn.execute('''create table if not exists detail_link(link_id text PRIMARY KEY, link_href text, link_pic buffer)''')
		# Save (commit) the changes
		conn.commit()
		# We can also close the cursor if we are done with it
		conn.close()

	def get_all_link_href(self):
		conn = sqlite3.connect(self.dbname)
		link_href_list = [row[0] for row in conn.execute('''select link_href from detail_link''')]
		return link_href_list

	def update_detail_link_table(self, row_list):
		conn = sqlite3.connect(self.dbname)
		conn.executemany('''replace into detail_link(link_id, link_href, link_pic) values(?, ?, ?)''', row_list)
		conn.commit()
		conn.close()
