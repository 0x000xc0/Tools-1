#!/usr/bin/env python 
# -*- encoding: utf-8 -*-
################################################
# konan - Advanced Web Application Dir Scanner
# by: Momo (mallok) Outaadi
# https://github.com/m4ll0k
################################################

import re
import threading
from utils.file import *
from output import *
 
class FuzzerDict(Output):
	def __init__(self,path,kwargs):
		Output.__init__(self)
		self.extensions = kwargs['exts']
		self.entries = []
		self.currentIndex = 0
		self.isSelected = False
		self.condition = threading.Condition()
		self._path = path 
		self.dictionaryFile = File(self._path)
		self.force = kwargs['force']
		self.lowercase = kwargs['lowercase']
		self.uppercase = kwargs['uppercase']
		self.split = kwargs['split']
		self.ignore = kwargs['ignore']
		self.generate()

	def generate(self):
		self.entries = []
		for line in self.dictionaryFile.read():
			if self.force:
				for ext in self.extensions:
					line = line + '.' + ext
					if line not in self.entries:
						self.entries.append(line)
				self.isSelected = True
			if self.split:
				if '.' in line:
					line = line.split('.')[0]
					if line not in self.entries:
						self.entries.append(line)
				self.isSelected = True
			if self.lowercase:
				if line.lower() not in self.entries:
					self.entries.append(line.lower())
				self.isSelected = True
			if self.uppercase:
				if line.upper() not in self.entries:
					self.entries.append(line.upper())
				self.isSelected = True
			if self.isSelected is False:
				if line not in self.entries:
					self.entries.append(line)
			# --
			if self.ignore != None:
				try:
					regexp = re.search(self.ignore,line,re.I)
					if regexp:
						try:
							word = regexp.group(0)
							del self.entries[self.entries.index(word)]
						except (AttributeError,ValueError) as e:
							pass
				except re.error as e:
					self.printWarn('REGEX ERROR: %s'%e.message,not 0)

	def regenerate(self):
		self.generate()
		self.reset()

	def nextWithIndex(self,basePath=None):
		self.condition.acquire()
		try:
			result = self.entries[self.currentIndex]
		except IndexError:
			self.condition.release()
			return None,None
		self.currentIndex = self.currentIndex + 1
		currentIndex = self.currentIndex
		self.condition.release()
		return currentIndex,result

	def next(self,basePath=None):
		_,path = self.nextWithIndex(basePath)
		return path

	def reset(self):
		self.condition.acquire()
		self.currentIndex = 0
		self.condition.release()

	def __len__(self):
		return len(self.entries)