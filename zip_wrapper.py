#! /usr/bin/python
# -*- coding: utf-8 -*-
import StringIO, gzip, os, tarfile

def gzip_decode_from_bytes(data):
	compressedstream = StringIO.StringIO(data)
	gziper = gzip.GzipFile(fileobj=compressedstream) 
	decompressed_data = gziper.read()
	return decompressed_data

class tar_helper:
	"""This is a class for zip operations
		import zip_wrapper

		helper = zip_wrapper.tar_helper()
		helper.zip_dir('test')
		helper.unzip_dir('test.tar.gz')
	"""
	def zip_dir(self, dirname):
		if not os.path.isdir(dirname):
			print('dir_path is invalid: %s'%(dirname))
			return
		t = tarfile.open(dirname + ".tar.gz", "w:gz")
		for root, dir, files in os.walk(dirname):
			print root, dir, files
			for file in files:
				fullpath = os.path.join(root, file)
				t.add(fullpath)
		t.close()

	def unzip_dir(self, filename, todir='.'):
		if not os.path.isfile(filename):
			print('file_path is invalid: %s'%(filename))
			return
		t = tarfile.open(filename)
		t.extractall(path=todir)
		t.close()
