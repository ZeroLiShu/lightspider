#! /usr/bin/python
# -*- coding: utf-8 -*-

from light_spider_re import spider_index_detail, MAX_PAGE_INDEX
from producer_customer import producer, customer, mediator

spider_op = spider_index_detail()

class index_spider(producer):
    
    index = 1
    
    def __init__(self, name, jobq):
        producer.__init__(self, name, jobq)
    
    def _produce(self):
        detail_href_list = spider_op.iterate_index_page(self.index, self.index + 1)
        self.index += 1
        return detail_href_list
    
    def _done(self):
        if self.index < MAX_PAGE_INDEX:
            return False
        else:
            return True


class detail_spider(mediator):
    
    def __init__(self, name, jobq_in, jobq_out):
        mediator.__init__(self, name, jobq_in, jobq_out)
    
    def _consume(self, job):
        return spider_op.iterate_detail_page(job)
        