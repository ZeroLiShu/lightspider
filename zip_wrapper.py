#! /usr/bin/python
# -*- coding: utf-8 -*-
import StringIO, gzip

class zip_wrapper:
    """This is a class for gzip operations"""
    def gzip_decode_from_bytes(self, data):
        compressedstream = StringIO.StringIO(data)
        gziper = gzip.GzipFile(fileobj=compressedstream) 
        decompressed_data = gziper.read()
        return decompressed_data