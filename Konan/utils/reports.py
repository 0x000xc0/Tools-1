#!/usr/bin/env python 
# -*- encoding: utf-8 -*-
################################################
# konan - Advanced Web Application Dir Scanner
# by: Momo (mallok) Outaadi
# https://github.com/m4ll0k
################################################

import json

class BaseReport(object):
	def __init__(self,fileName):
		self.fileName = fileName
		self.open()
		self.pathList = {
				'code' : None,
				'url'  : None,
				'content' : None,
				'method' : None
				}

	def addPath(self,status,path,content,method):
		self.pathList['code'] = status
		self.pathList['url'] = path
		self.pathList['content'] = content
		self.pathList['method'] = method

	def open(self):
		self.file = open(self.fileName,'w+')

	def save(self):
		self.file.writelines(self.generate())

	def close(self):
		self.file.close()

	def generate(self):
		raise NotImplementedError

class JsonReport(BaseReport):
	def generate(self):
		msg = '''{\n\t"code"\t\t:\t"%s",\n\t"method"\t:\t"%s",\n\t"content"\t:\t"%s",\n\t"url"\t\t:\t"%s"\n}\n\n'''%(
			self.pathList['code'],
			self.pathList['method'],
			self.pathList['content'],
			self.pathList['url']
			)
		return json.loads(json.dumps(msg,sort_keys=True,indent=4))

class TextReport(BaseReport):
	def generate(self):
		msg = ' {0} -\t{1}\t-\t{2}\t- {3}\n'.format(
			self.pathList['code'],
			self.pathList['method'],
			self.pathList['content'],
			self.pathList['url']
			)
		return msg