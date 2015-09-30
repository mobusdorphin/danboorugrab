#!/usr/bin/python

import requests
import re
import wget

outputString = ''
for page in xrange(100):
  r = requests.get('http://danbooru.donmai.us/posts?page=' + str(page) + '&tags=oshino_shinobu')
  match = re.findall('data-file-url="(.+?)"', r.text)
  for i in match:
    url = 'http://danbooru.donmai.us' + i
    wget.download(url)
