#!/usr/bin/env python 
# -*- encoding: utf-8 -*-
################################################
# konan - Advanced Web Application Dir Scanner
# by: Momo (mallok) Outaadi
# https://github.com/m4ll0k
################################################

import sys
import time
import threading

from colorama import init;init()

class Output(object):
	def __init__(self):
		self.lastLength = 0
		self.lastOutput = ''
		self.lastInLine = False
		self.mutex = threading.Lock()
		self.checkedPaths = []
		self.blacklist = {}
		self.mutexCheckedPaths = threading.Lock()
		self.basePath = None

	def printInLine(self,string):
		self.mutex.acquire()
		sys.stdout.write('\033[1K')
		sys.stdout.write('\033[0G')
		sys.stdout.write(string)
		sys.stdout.flush()
		self.lastInLine = True
		self.mutex.release()

	def printlastPathEntry(self,path,index,length):
		p = lambda x,y: float(x)/float(y)*100
		self.printInLine('{1:.2f}%\t - {time} '.format(path,p(index,length),time=time.strftime('%H:%M:%S')))

	def printWarn(self,string,e=True):
		print '\033[1;31m[ ! ]\033[0m \033[1m%s\033[0m'%(string)
		if e: sys.exit(0)