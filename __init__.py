#! /usr/bin/python
# -*- coding: utf-8 -*-


from Queue import Queue
from muti_thread_spider import index_spider, detail_spider, zip_spider

def main():
    job_queue = Queue()
    spider_p = index_spider("index spider", job_queue)
    spider_p.start()


    zip_queue = Queue()


    spider_m_1 = detail_spider("detail spider 1", job_queue, zip_queue)
    spider_m_2 = detail_spider("detail spider 2", job_queue, zip_queue)
    spider_m_3 = detail_spider("detail spider 3", job_queue, zip_queue)
    spider_m_4 = detail_spider("detail spider 4", job_queue, zip_queue)
    spider_m_5 = detail_spider("detail spider 5", job_queue, zip_queue)

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


if __name__ == '__main__':
    main()
