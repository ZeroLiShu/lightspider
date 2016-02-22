#! /usr/bin/python
# -*- coding: utf-8 -*-

import threading, time


class producer(threading.Thread):
    def __init__(self, name, jobq):
        threading.Thread.__init__(self)
        self.name = name
        self.data = jobq
    
    def run(self):
        while True:
            if self._done():
                break;
            job_list = self._produce()
            for job in job_list:
                self.data.put(job)
            time.sleep(0.1)
    
    def _produce(self):
        pass
    
    def _done(self):
        pass

class customer(threading.Thread):
    def __init__(self, name, jobq):
        threading.Thread.__init__(self)
        self.name = name
        self.data = jobq
    
    def run(self):
        while True:
            if self.data.qsize() > 0:
                self._consume(self.data.get())
            time.sleep(0.1)
    
    def _consume(self, job):
        pass

class mediator(threading.Thread):
    def __init__(self, name, jobq_in, jobq_out):
        threading.Thread.__init__(self)
        self.name = name
        self.data_in = jobq_in
        self.data_out = jobq_out
    
    def run(self):
        while True:
            if self.data_in.qsize() > 0:
                new_job = self._consume(self.data_in.get())
                self.data_out.put(new_job)
            time.sleep(0.1)
    
    def _consume(self, job):
        pass
