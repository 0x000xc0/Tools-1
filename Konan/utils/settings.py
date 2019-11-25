#!/usr/bin/env python 
# -*- encoding: utf-8 -*-
################################################
# konan - Advanced Web Application Dir Scanner
# by: Momo (mallok) Outaadi
# https://github.com/m4ll0k
################################################

import re
import os
import sys
import urlparse
# --
from handler.output import Output
from colorama import init;init()

# TOOL PATH
ABS_PATH = os.path.dirname(os.path.realpath(__file__)).split('konan')[0]
TOOL_PATH = os.path.join(os.path.join(ABS_PATH,'konan'),'')

# TOOL PATH
RED = '\033[%s;31m'
YELLOW ='\033[%s;33m'
GREEN = '\033[%s;32m'
BLUE = '\033[%s;34m'
WHITE = '\033[%s;38m'
RESET = '\033[0m'

# BANNER
banner = """{0}
Konan {1} - Advanced Web Application Dir Scanner
by: Momo (mallok) Outaadi (github.com/m4ll0k)
{2}
""".format('-'*50,'(0.1)','-'*50)


# KWARGS
kwargs = {
			'hostname' : False,
			'agent'    : '',
			'ragent'   : False,
			'cookies'  : None,
			'headers'  : None,
			'redirect' : False,
			'proxy'    : None,
			'methods'  : False,
			'output'   : None,
			'timeout'  : 5,
			'delay'    : None,
			'output'   : None,
			'wordlist' : TOOL_PATH + '/db/dict.txt',
			'exts'     : None,
			'threads'  : 1,
			'recursive': False,
			'host'     : None,
			'force'    : False,
			'lowercase': False,
			'uppercase': False,
			'split'    : False,
			'ignore'   : None,
			'exclude'  : [],
			'only'     : [],
			'methods'  : False,
			'length'   : None,
			'dirs'     : [],
			'firstScan': False,
			'multiple' : False,
			'recDir'   : [],
			'subDir'   : []
		}

kwargs['agent'] = 'Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)'

usage = ''' 
\rUsage: konan.py [OPTIONS]\n
\t-u --url\tTarget URL (e.g: http://site.com, http://site.com/%%/index.php)
\t-U --url-list\tScan multiple targets given in a text file
\t-b --hostname\tMake request by hostname (ip addr)
\t-e --extension\tExtensions list separated by comma (e.g: php,html)
\t-w --wordlist\tSet wordlist (e.g: wordlist.txt)
\t-a --agent\tSet HTTP User-Agent header value
\t-r --ragent\tUse random User-Agent
\t-c --cookies\tSet HTTP Cookie header value

\t-H --headers\tSet HTTP Headers (e.g: "Accept: ..\\nTag: 1234\\n..")
\t-f --force\tForce extension for every wordlist entry
\t-x --exclude\tExclude status code separated by comma (e.g: 400,500)
\t-l --lowercase\tForce lowercase for every wordlist entry
\t-p --uppercase\tForce uppercase for every wordlist entry
\t-i --split\tSplit extension for every wordlist entry (test.php -> test)
\t-R --redirect\tAllow URL redirection, default is false
\t-d --delay\tDelay in seconds between each HTTP request
\t-P --proxy\tUse a proxy to connect to the target URL
\t-I --ignore\tIgnore words in wordlist, use regex (e.g: "^test[a-zA-Z0-9]*\.zip")
\t-m --methods\tCheck other methods (POST,PUT and DELETE)

\t-O --output\tOutput support json and txt format (e.g: out.json)
\t-C --length\tShow only if response length is ">","<" or "=" (e.g: ">1024")
\t-o --only\tShow only status code separated by comma (e.g: 200,302)
\t-t --threads\tMax number of concurrent HTTP requests
\t-T --timeout\tSeconds to wait before timeout connection
\t-E --recursive\tBruteforce recursively 
\t-D --dir-rec\tSpecify dir bruteforce recursively (e.g: test,dev)
\t-S --sub-dir\tSpecify sub-dir bruteforce (e.g: test,dev)
\t-h --help\tShow this help and exit
'''

# CONTENT PROCESS
def cProcess(condition,content):
	if '>' in condition:
		try:
			number = int(re.findall(r'\>(\d*)',condition,re.I)[0])
		except IndexError:
			return False
		if content > number:
			return True
	elif '<' in condition:
		try:
			number = int(re.findall(r'\<(\d*)',condition,re.I)[0])
		except IndexError:
			return False 
		if content < number:
			return True
	elif '=' in condition:
		try:
			number = int(re.findall(r'\=(\d*)',condition,re.I)[0])
		except IndexError:
			return False 
		if content == number:
			return True
	return False

# ALL WORD OPTIONS
wOption = [	'url=','url-list=','hostname','extension=','wordlist=',
			'agent=','ragent','cookies=','headers=','force','exclude=',
			'lowercase','uppercase','split','redirect','delay=','proxy=',
			'methods','output=','length=','ignore=','only=','threads=','timeout=','recursive',
			'dir-rec=','sub-dir=','help'
			]
# ALL LETTERS OPTIONS
lOption = 'u:U:e:w:a:c:H:x:I:d:D:P:S:O:C:o:t:T:bhrflpiRmE'

# URLPARSE
def urlParse(url):
	if url == '':
		Output().printWarn('Invalid Target URL, Please check your URL!!')
	_url = url
	path_end = False
	is_query = False
	parse = urlparse.urlparse(url)
	if parse.scheme == '':
		url = 'http://' + url
		parse = urlparse.urlparse(url)
		if parse.path != '':
			path_ext = parse.path[-10:]
			if re.search(r'\w*\.\w*',path_ext,re.I):
				path_end = True
		if parse.query != '':
			is_query = True
	elif parse.scheme != '':
		if parse.path != '':
			path_ext = parse.path[-10:]
			if re.search(r'\w*\.\w*',path_ext,re.I):
				path_end = True
			if parse.query != '':
				is_query = True
	if not _url.endswith('/') and path_end == False: 
		_url = url + '/'

	if r'%%' in _url:
		return _url,parse.netloc
	elif re.search(r'\%(\S*)\%',_url,re.I):
		return _url,parse.netloc
	elif is_query is True:
		_url =  _url.split('?')[0]
		if path_end:
			return _url.split(
				re.search(r'\/([a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*)',
					parse.path,re.I).group(0)[1:])[0],parse.netloc
	else:
		return _url,parse.netloc
	return _url,parse.netloc

# URL JOIN WITH PATH
def urlJoin(url,path):
	if url.endswith('/') and path.startswith('/'):
		return url + path[1:]
	elif not url.endswith('/') and not path.startswith('/'):
		return url + '/' + path 
	else:
		return url + path 

header = "\033[1mPERCENT\t -   TIME   - CODE  -   METHOD  - LENGTH - URL\033[0m\n%s"%('-'*55)

def printConfig():
	ban = banner
	ban += '\n%sURL:%s {url}\n\n'%(YELLOW%1,RESET)
	return ban+header

def StrToInt(list_):
	return_data = []
	for i in list_:
		return_data.append(int(i))
	return return_data

def printContent(count):
	if len(count) <= 5:
		if len(count) == 0:
			return '%s%s'%(count,' '*6)
		elif len(count) == 1:
			return '%s%s'%(count,' '*5)
		elif len(count) == 2:
			return '%s%s'%(count,' '*4)
		elif len(count) == 3:
			return '%s%s'%(count,' '*3)
		elif len(count) == 4:
			return '%s%s'%(count,' '*2)
		elif len(count) == 5:
			return '%s%s'%(count,' '*1)
	return str(count)