#!/usr/bin/env python 
# -*- encoding: utf-8 -*-
################################################
# konan - Advanced Web Application Dir Scanner
# by: Momo (mallok) Outaadi
# https://github.com/m4ll0k
################################################

import sys
import getopt

from utils.settings import *
from handler.output import * 
from utils.file import *
from handler.handler import *

class Konan(Output):
	def __init__(self):
		Output.__init__(self)
		self.url = None
		self.urls = None
		self.exts = None
		self.wordlist = None

	def main(self):
		if len(sys.argv) < 2:
			print usage
			sys.exit(0)
		try:
			opts,args = getopt.getopt(sys.argv[1:],lOption,wOption)
		except getopt.GetoptError as e:
			print usage
			sys.exit(0)
		for i in range(len(opts)):
			if(opts[i][0] in('-u','--url')): self.url,kwargs['host'] = urlParse(opts[i][1])
			if(opts[i][0] in('-U','--url-list')): 
				self.urls = File(opts[i][1])
				if self.urls.exists() is False:
					self.printWarn('FILE ERROR: file %s not exists'%(opts[i][1]))
				if self.urls.canRead() is False:
					self.printWarn('FILE ERROR: can\'t read %s file'%(opts[i][1]))
				self.urls = self.urls.read()
			if(opts[i][0] in('-b','--hostname')): kwargs['hostname'] = True
			if(opts[i][0] in('-e','--extension')): kwargs['exts'] = opts[i][1].split(',')
			if(opts[i][0] in('-w','--wordlist')): kwargs['wordlist'] = opts[i][1]
			if(opts[i][0] in('-r','--ragent')): kwargs['ragent'] = True
			if(opts[i][0] in('-O','--output')):kwargs['output'] = opts[i][1]
			if(opts[i][0] in('-a','--agent')):kwargs['agent'] = opts[i][1]
			if(opts[i][0] in('-c','--cookies')):kwargs['cookies'] = opts[i][1]
			if(opts[i][0] in('-H','--headers')):kwargs['headers'] = opts[i][1]
			if(opts[i][0] in('-f','--force')):kwargs['force'] = True
			if(opts[i][0] in('-x','--exclude')):kwargs['exclude']= StrToInt(opts[i][1].split(','))
			if(opts[i][0] in('-l','--lowercase')):kwargs['lowercase'] = True
			if(opts[i][0] in('-p','--uppercase')):kwargs['uppercase'] = True
			if(opts[i][0] in('-i','--split')):kwargs['split'] = True
			if(opts[i][0] in('-I','--ignore')):kwargs['ignore']=opts[i][1]
			if(opts[i][0] in('-R','--redirect')):kwargs['redirect'] = True
			if(opts[i][0] in('-d','--delay')):kwargs['delay'] = int(opts[i][1])
			if(opts[i][0] in('-P','--proxy')):kwargs['proxy'] = opts[i][1]
			if(opts[i][0] in('-m','--methods')):kwargs['methods'] = True
			if(opts[i][0] in('-C','--length')):kwargs['length'] = opts[i][1]
			if(opts[i][0] in('-o','--only')):kwargs['only'] = StrToInt(opts[i][1].split(','))
			if(opts[i][0] in('-t','--threads')):kwargs['threads'] = int(opts[i][1])
			if(opts[i][0] in('-T','--timeout')):kwargs['timeout'] = float(opts[i][1])
			if(opts[i][0] in('-E','--recursive')):kwargs['recursive'] = True
			if(opts[i][0] in('-D','--dir-rec')):
				kwargs['recursive'] = True
				kwargs['recDir'] = opts[i][1].split(',')
			if(opts[i][0] in('-S','--sub-dir')):
				kwargs['subDir'] = opts[i][1].split(',')
			if(opts[i][0] in('-h','--help')):
				print usage
				sys.exit(0)
		# -- print banner and url
		print printConfig().format(url=self.url)
		# -- single URL
		if self.url != None:
			Handler(self.url,kwargs)
		# -- multiple TARGET's provided by file 
		elif self.urls != None:
			kwargs['multiple'] = True
			for _url in self.urls:
				url,kwargs['host'] = urlParse(_url)
				print '\n\n%sURL:%s %s\n\n%s'%(YELLOW%1,RESET,url,header)
				Handler(url,kwargs)
			print '\nTask Completed'
		# -- recursively
		if kwargs['recursive'] and kwargs['dirs'] != []:
			kwargs['firstScan'] = not 0
			for _dir in kwargs['dirs']:
				url,kwargs['host'] = urlParse(urlJoin(self.url,_dir))
				print '\n\n%sDirectory:%s %s\n\n%s'%(YELLOW%1,RESET,url,header)
				Handler(url,kwargs)
			print '\nTask Completed'
		# -- scan sub-dir
		if kwargs['subDir'] != []:
			for _dir in kwargs['subDir']:
				url,kwargs['host'] = urlParse(urlJoin(self.url,_dir))
				print '\n\n%sDirectory:%s %s\n\n%s'%(YELLOW%1,RESET,url,header)
				Handler(url,kwargs)
			print '\nTask Completed'
		return not 1
try:
	Konan().main()
except Exception as e:
	Output().printWarn(e)