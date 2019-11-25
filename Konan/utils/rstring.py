#!/usr/bin/env python 
# -*- encoding: utf-8 -*-
################################################
# konan - Advanced Web Application Dir Scanner
# by: Momo (mallok) Outaadi
# https://github.com/m4ll0k
################################################

import string 
import random

def rstring(len_):
	a = ""
	for i in xrange(0,len_):
		a += ''.join(random.choice(string.letters))
	return a 