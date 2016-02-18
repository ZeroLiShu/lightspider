#! /usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3

class db_avgirls_helper:
	"""database operations for av bt girls
		import db_wrapper

		helper = db_wrapper.db_avgirls_helper()
		helper.create_db('test.s3db')

		row_list = [
			("1", "www.test.com", ""),
			("2", "www.test.com", ""),
		]

		helper.update_detail_link_table('test.s3db', row_list)
		link_id_list = helper.get_all_link_id('test.s3db')
		print link_id_list
	"""
	
	def create_db(self, dbname):
		conn = sqlite3.connect(dbname)
		c = conn.cursor()
		# Create table
		c.execute('''create table if not exists detail_link(link_id text PRIMARY KEY, link_href text, link_pic buffer)''')
		# Save (commit) the changes
		conn.commit()
		# We can also close the cursor if we are done with it
		c.close()
	
	def get_all_link_id(self, dbname):
		conn = sqlite3.connect(dbname)
		link_id_list = []
		for row in conn.execute('''select link_id from detail_link'''):
			link_id_list.append(row[0])
		return link_id_list
	
	def update_detail_link_table(self, dbname, row_list):
		conn = sqlite3.connect(dbname)
		c = conn.cursor()
		c.executemany('''replace into detail_link(link_id, link_href, link_pic) values(?, ?, ?)''', row_list)
		conn.commit()
		c.close()
