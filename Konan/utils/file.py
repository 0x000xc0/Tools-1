#!/usr/bin/env python 
# -*- encoding: utf-8 -*-
################################################
# konan - Advanced Web Application Dir Scanner
# by: Momo (mallok) Outaadi
# https://github.com/m4ll0k
################################################

import os

class File(object):
	def __init__(self,*file_path):
		self._path = fileUtils.buildPath(*file_path)
		
	def isValid(self):
		return fileUtils.isFile(self._path)

	def exists(self):
		return fileUtils.exists(self._path)

	def canRead(self):
		return fileUtils.canRead(self._path)

	def canWrite(self):
		return fileUtils.canWrite(self._path)

	def  read(self):
		return fileUtils.read(self._path)


class fileUtils(object):
	
	@staticmethod
	def buildPath(*file_path):
		return os.path.join(*file_path) if file_path else ''
	
	@staticmethod
	def exists(fileName):
		return os.access(fileName,os.F_OK)

	@staticmethod
	def canRead(fileName):
		if not os.access(fileName,os.R_OK):
			return False
		return True

	@staticmethod
	def canWrite(fileName):
		return os.access(fileName,os.W_OK)

	@staticmethod
	def read(fileName):
		return [x.strip() for x in open(fileName,'r')]

	@staticmethod
	def isDir(fileName):
		return os.path.isdir(fileName)

	@staticmethod
	def isFile(fileName):
		return os.path.isfile(fileName)
