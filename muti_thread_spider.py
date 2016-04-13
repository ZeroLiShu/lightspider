#! /usr/bin/python
# -*- coding: utf-8 -*-

from light_spider_re import spider_index_detail, MAX_PAGE_INDEX
from producer_customer import producer, customer, mediator

spider_op = spider_index_detail()

class index_spider(producer):

    def __init__(self, name, jobq, sindex, eindex, web_page):
        producer.__init__(self, name, jobq)
        self.sindex = sindex
        self.eindex = eindex
        self.web_page = web_page

    def _produce(self):
        detail_href_list = spider_op.iterate_index_page(self.sindex, self.sindex + 1, self.web_page)
        self.sindex += 1
        return detail_href_list

    def _done(self):
        if self.sindex < self.eindex:
            return False
        else:
            return True


class detail_spider(mediator):

    def __init__(self, name, jobq_in, jobq_out, web_page):
        mediator.__init__(self, name, jobq_in, jobq_out)
        self.web_page = web_page

    def _consume(self, job):
        return spider_op.iterate_detail_page(job, self.web_page)

class zip_spider(customer):

	def __init__(self, name, jobq):
		customer.__init__(self, name, jobq)

	def _consume(self, job):
		(href_id, href) = job
		return spider_op.zip_into_db(href_id, href)
