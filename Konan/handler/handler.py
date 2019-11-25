#!/usr/bin/env python 
# -*- encoding: utf-8 -*-
################################################
# konan - Advanced Web Application Dir Scanner
# by: Momo (mallok) Outaadi
# https://github.com/m4ll0k
################################################

import os 
import sys
# --
from utils.reports import *
from utils.settings import *
# ---
from output import *
from fuzzerdict import *
from reportmanger import *
from fuzzer import *
from net.request import *

class Handler(Request,Output):
	def __init__(self,url,kwargs):
		self.kwargs = kwargs
		Output.__init__(self)
		Request.__init__(self,url,kwargs)
		try:
			# test the connection to the TARGET
			try:
				resp = self.http('','GET')
				if type(resp) == bool:
					self.printWarn('CONNECTION ERROR: check your Connection or Target URL!',False)
					sys.exit(0)
			except Exception as e:
				sys.exit(0)
			# init
			self.reportManager = ReportManager()
			self.setupReports()
			self.dict_ = FuzzerDict(self.kwargs['wordlist'],self.kwargs)
			fuzzer = Fuzzer(url,kwargs,self.dict_,kwargs['threads'],self.reportManager)
			fuzzer.start()
			fuzzer.wait()
		except Exception as e:
			self.printWarn(e)
			sys.exit(0)
		except (KeyboardInterrupt, SystemExit) as e:
			self.printWarn('Terminated by user...')
			sys.exit(0)
		if kwargs['recursive'] is False or kwargs['multiple'] is False or kwargs['subDir'] == []:
			print '\nTask Completed'

	def setupReports(self):
		# -- output report ---
		if self.kwargs['output'] != None:
			output = self.kwargs['output']
			try:
				path,ext = output.split('.')
			except ValueError as e:
				self.printWarn('OUTPUT ERROR: Extension file (text or json) not specified!',not 0)
			# -- 
			if ext == 'txt': self.reportManager.addOutput(TextReport(output))
			elif ext == 'json': self.reportManager.addOutput(JsonReport(output))
			else: self.printWarn('Output file extension not supported!',not 0)
