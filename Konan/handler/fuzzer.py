#!/usr/bin/env python 
# -*- encoding: utf-8 -*-
################################################
# konan - Advanced Web Application Dir Scanner
# by: Momo (mallok) Outaadi
# https://github.com/m4ll0k
################################################

import threading
# --
from Queue import Queue
from utils.rstring import *
from utils.reports import * 
from net.request import *
from fuzzerdict import *
from utils.settings import *
from reportmanger import *
from output import *
from net.request import *


class Fuzzer(Request,Output):

	def __init__(self,url,kwargs,dictionary, threads=1,reportManager=None):
		Request.__init__(self,url,kwargs)
		Output.__init__(self)
		self.kwargs = kwargs
		self.dictionary = dictionary
		self.excludeStatusCodes = kwargs['exclude']
		self.includeStatusCodes = kwargs['only']
		self.methods = kwargs['methods']
		self.threads = []
		self.length = kwargs['length']
		self.threadsCount = threads
		self.running = False
		self.directories = Queue()
		self.recursive = kwargs['recursive']
		self.currentDirectory = ''
		self.indexMutex = threading.Lock()
		self.index = 0
		self.threadSetup()
		self.reportManager = ReportManager() if reportManager is None else reportManager

	def threadSetup(self):
		if len(self.threads) != 0:
			self.threads = []
		for thread in range(self.threadsCount):
			newThread = threading.Thread(target=self.thread_proc)
			newThread.daemon = True
			self.threads.append(newThread)


	def start(self):
		self.index = 0
		self.dictionary.reset()
		self.runningThreadCount = len(self.threads)
		self.running = True 
		self.finishedEvent = threading.Event()
		self.finishedThreadCondition = threading.Condition()
		self.playEvent = threading.Event()
		self.pausedSemaphore = threading.Semaphore(0)
		self.playEvent.set()
		for thread in self.threads:
			thread.start()

	def play(self):
		self.playEvent.set()

	def pause(self):
		self.playEvent.clear()
		for thread in self.threads:
			if thread.is_alive():
				self.pausedSemaphore.acquire()

	def handleInterrupt(self):
		option = ""
		self.pause()
		try:
			while True:
				if self.directories.empty():
					option = raw_input('\n[q/Q]uit / [c/C]ontinue: ')
				if option in ['q','Q','quit','QUIT','Quit']:
					self.running = False
					self.exit = True
					self.play()
					raise KeyboardInterrupt
				elif option in ['c','Continue','continue','CONTINUE','C']:
					self.play()
					return
				else:
					continue
		except KeyboardInterrupt, SystemExit:
			self.exit = True 
			raise KeyboardInterrupt

	def waitThreads(self):
		try:
			while self.running:
				try:
					self.finishedEvent.wait(0.3)
				except (KeyboardInterrupt, SystemExit) as e:
					self.handleInterrupt()
					if self.exit:
						raise 
					else:
						pass
		except (KeyboardInterrupt,SystemExit) as e:
			if self.exit:
				raise e
			self.handleInterrupt()
			if self.exit:
				raise e
			else:
				pass
		for thread in self.threads:
			thread.join()

	def wait(self):
		self.exit = False
		self.waitThreads()
		while not self.directories.empty():
			self.currentDirectory = self.directories.get()
			self.threadSetup()
			self.start()
			self.waitThreads()
		self.reportManager.save()
		self.reportManager.close()
		return

	def addDirectory(self,path):
		if self.recursive is False:
			return False
		if self.kwargs['recDir'] != []:
			for x in self.kwargs['recDir']:
				if x in self.kwargs['dirs']:
					pass
				else:
					self.kwargs['dirs'].append(x)
		if path != None and self.kwargs['firstScan'] is False:
			if path in self.kwargs['dirs']:
				pass
			else:
				self.kwargs['dirs'].append(path) 
		else:
			return False

	def finishThreads(self):
		self.running = False
		self.finishedEvent.set()

	def testPath(self,path,method='GET'):
		resp = self.http(path,method)
		return resp.code,resp

	def thread_proc(self):
		try:
			path = self.dictionary.next()
			while path is not None:
				try:
					if self.methods is True:
						for method in ['GET','POST','PUT',b'DELETE']:
							code,resp = self.testPath(path,method=method)
							if code != 404 and code != 405:
								if code in self.includeStatusCodes and (cProcess(self.length,resp.len_content) if self.length != None else True):
									print('- %s -\t%s\t - %s  - %s %s'%(code,resp.method,printContent(str(len(resp.content))),resp.url,' -> '+resp.headers['Location'] if code in [301,302] else ''))
									self.addDirectory(path)
									self.reportManager.addPath(code,resp.url,resp.len_content,resp.method)
									self.reportManager.save()
								elif code not in self.excludeStatusCodes and self.includeStatusCodes == [] and (cProcess(self.length,resp.len_content) if self.length != None else True):
									print('- %s -\t%s\t- %s   - %s %s'%(code,resp.method,printContent(str(len(resp.content))),resp.url,' -> '+resp.headers['Location'] if code in [301,302] else ''))
									self.addDirectory(path)
									self.reportManager.addPath(code,resp.url,resp.len_content,resp.method)
									self.reportManager.save()
								elif (cProcess(self.length,resp.len_content) if self.length != None else True) and self.includeStatusCodes == [] and self.excludeStatusCodes == []:
									print('- %s -\t%s\t- %s   - %s %s'%(code,resp.method,printContent(str(len(resp.content))),resp.url,' -> '+resp.headers['Location'] if code in [301,302] else ''))
									self.addDirectory(path)
									self.reportManager.addPath(code,resp.url,resp.len_content,resp.method)
									self.reportManager.save()
							# ------------------------------
							self.indexMutex.acquire()
							self.index += 1
							self.printlastPathEntry(path,self.index,len(self.dictionary))
							self.indexMutex.release()
							path = self.dictionary.next()
							if not self.playEvent.isSet():
								self.pausedSemaphore.release()
								self.playEvent.wait()
							if not self.running:
								break
							if path is None:
								self.running = False
								self.finishThreads()
					else:
						code,resp = self.testPath(path)
						if code != 404:
							# ---------------------------
							if code in self.includeStatusCodes and (cProcess(self.length,resp.len_content) if self.length != None else True):
								print('-  %s  -\t%s\t-  %s  - %s %s'%(code,resp.method,printContent(str(len(resp.content))),resp.url,' -> '+resp.headers['Location'] if code in [301,302] else ''))
								self.addDirectory(path)
								self.reportManager.addPath(code,resp.url,resp.len_content,resp.method)
								self.reportManager.save()

							elif code not in self.excludeStatusCodes and self.includeStatusCodes == [] and (cProcess(self.length,resp.len_content) if self.length != None else True):
								print('-  %s  -\t%s\t-  %s  - %s %s'%(code,resp.method,printContent(str(len(resp.content))),resp.url,' -> '+resp.headers['Location'] if code in [301,302] else ''))
								self.addDirectory(path)
								self.reportManager.addPath(code,resp.url,resp.len_content,resp.method)
								self.reportManager.save()
					
				 			elif (cProcess(self.length,resp.len_content) if self.length != None else True) and self.includeStatusCodes == [] and self.excludeStatusCodes == []:
								print('-  %s  -\t%s\t-  %s  - %s %s'%(code,resp.method,printContent(str(len(resp.content))),resp.url,' -> '+resp.headers['Location'] if code in [301,302] else ''))
								self.addDirectory(path)
								self.reportManager.addPath(code,resp.url,resp.len_content,resp.method)
								self.reportManager.save()
						# ------------------------------
						self.indexMutex.acquire()
						self.index += 1
						self.printlastPathEntry(path,self.index,len(self.dictionary))
						self.indexMutex.release()
						path = self.dictionary.next()
						if not self.playEvent.isSet():
							self.pausedSemaphore.release()
							self.playEvent.wait()
						if not self.running:
							break
						if path is None:
							self.running = False
							self.finishThreads()
				except Exception as e:
					#self.printWarn('%s'%e)
					continue
		except KeyboardInterrupt,SystemExit:
			if self.exit:
				raise e 
			self.handleInterrupt()
			if self.exit:
				raise e 
			pass
