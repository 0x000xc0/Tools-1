#!/usr/bin/env python 
# -*- encoding: utf-8 -*-
################################################
# konan - Advanced Web Application Dir Scanner
# by: Momo (mallok) Outaadi
# https://github.com/m4ll0k
################################################

import re
import time
import socket
import random
import urlparse
import urllib3
import requests

from utils.rstring import *
from handler.output import *

class Request(Output):
	headers = {
		'Accept-Language' : 'en-us',
		'Accept-Encoding' : 'identity',
		'Keep-Alive' : '300',
		'Connection' : 'keep-alive',
		'Cache-Control' : 'max-age=0'
	}

	def __init__(self,url,kwarg):
		Output.__init__(self)
		self.url = url
		self.host = kwarg['host']
		self.cookies = kwarg['cookies']
		self.useragent = kwarg['agent']
		self.newheaders = kwarg['headers']
		self.redirect = kwarg['redirect']
		self.timeout = kwarg['timeout']
		self.proxy = kwarg['proxy']
		self.ragent = kwarg['ragent']
		self.methods = kwarg['methods']
		self.byhostname = kwarg['hostname']
		self.delay = kwarg['delay']
		self.proxies = {}
		self.ip = None
		# set host
		if self.host != None:
			self.setHeader('Host',self.host)
		# set user-agent
		if self.useragent != None:
			self.setHeader('User-Agent',self.useragent)
		# set random user-agent
		if self.ragent is True:
			self.setHeader('User-Agent',randomAgent())
		# set cookie
		if self.cookies != None:
			self.setHeader('Cookie',self.cookies)
		# set headers
		if self.newheaders != None:
			for header in self.newheaders.split('\\n'):
				if header != " " and header != None:
					self.setHeader(header.split(':')[0],header.split(':')[1])
		# set proxies
		if self.proxy != None:
			self.proxies['http'] = self.proxy
			self.proxies['https'] = self.proxy

	def setHeader(self,name,value):
		self.headers.update({name:value})

	def parserPath(self,url,word):
		if word.endswith('/'): word = word[:-1]
		if word.startswith('/'): word = word[1:]
		if url.endswith('/'): url = url[:-1] # ERROR HERE
		# //
		if r'%%' in url:
			return url.replace(r'%%',word)
		# sub %WORD%
		elif re.search(r'\%(\S*)\%',url,re.I):
			return re.sub(r'\%(\S*)\%',word,url)
		else:
			return url +'/'+ word
 
	def http(self,word,method='GET'):
		port = None
		host = None
		if self.byhostname:
			if ':' in self.host:
				host,port = self.host.split(':') 
			else:
				host = self.host
			# -- 
			try:
				self.ip = socket.gethostbyname(host)
			except socket.gaierror:
				self.printWarn('CONNECTION ERROR: Temporary failure in name resolution',True)
		# --
		if self.ip != None:
			self.url = re.sub(self.host,self.ip+(':'+str(port) if port != None else ''),self.url)
		# -- 
		response = None
		try:
			resp = requests.packages.urllib3.disable_warnings(
				urllib3.exceptions.InsecureRequestWarning
				)
			resp = requests.request(
				url = self.parserPath(self.url,word),
				method=method,
				data=None if method == 'GET' else randomData(),
				headers = self.headers,
				allow_redirects = self.redirect,
				verify = False,
				proxies = self.proxies,
				timeout = self.timeout
			)
			response = resp
			if self.delay is not None:
				time.sleep(self.delay)
		except requests.exceptions.TooManyRedirects as e:
			return not 1
		except requests.exceptions.SSLError as e:
			return not 1
		except requests.ConnectionError as e:
			return not 1
		except (requests.exceptions.ConnectTimeout,
			requests.exceptions.ReadTimeout,
			requests.exceptions.Timeout,socket.timeout) as e:
			return 1
		return Response(response)		


def randomAgent():
	agents = [
	"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"
	"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36"
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
	"Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
	"Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
	"Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
	"Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
	"Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
	"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)",
	"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
	"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
	"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
	"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)",
	"Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)",
	"Mozilla/4.0 (Compatible; MSIE 8.0; Windows NT 5.2; Trident/6.0)",
	"Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
	"Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))",
	"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
	"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0",
	"Mozilla/5.0 (X11; Linux i686; rv:67.0) Gecko/20100101 Firefox/67.0",
	"Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.28 Safari/537.36 OPR/61.0.3298.6 (Edition developer)",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.134 Safari/537.36 Vivaldi/2.5.1525.40"
	]
	return agents[random.randint(0,len(agents))]

def randomData():
	return "{0}={1}&{2}={3}".format(
		rstring(5),rstring(10),rstring(5),rstring(10))

class Response(object):
	def __init__(self,response):
		self.code = response.status_code if response != None else 404 
		self.method = response.request.method if response != None else '' 
		self.content = response._content if response != None else '' 
		self.text = response.text  if response != None else '' 
		self.len_content = len(self.content)
		self.reason = response.reason if response != None else '' 
		self.url = response.url if response != None else ''  
		self.headers = response.headers if response != None else {}