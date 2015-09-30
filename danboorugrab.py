#!/usr/bin/python

import requests
import re
import wget
import sys

outputString = ''
urlList = []
notFound = True
tagString = ''
urlString = ''
for i in sys.argv[1:]:
  tagString += i + '+'
tagString = tagString[:-1]
sourceUrl = 'http://danbooru.donmai.us/posts?&tags=' + tagString
while notFound:
  print "Checking page %s" % sourceUrl
  r = requests.get(sourceUrl)
  match = re.findall('data-file-url="(.+?)"', r.text)
  if len(match) == 0:
    notFound = False
  for i in match:
    url = 'http://danbooru.donmai.us' + i
    urlList.append(url)
  try:
    sourceUrl = 'http://danbooru.donmai.us' + re.search('next" href="(.+?)"', r.text).group(1)
  except AttributeError:
    notFound = False
print 'Found %s items.  List URLs? y/N' % len(urlList)
toList = raw_input()
toList = toList.lower()
if toList == 'y' or toList == 'yes':
  for i in urlList:
    urlString += i + '\n'
  print urlString
  print 'Save URL list? y/N'
  saveList = raw_input()
  if saveList == 'y'or savelist == 'yes':
    f = open(tagString + '.txt', 'w')
    f.write(urlString)
    f.close()
print 'Download them all? y/N'
downloadThem = raw_input()
if downloadThem == 'y' or downloadThem == 'yes':
  dlcount = 1
  for i in urlList:
    print '\nDownloading file %s of %s' % (dlcount, len(urlList))
    wget.download(i)
    dlcount += 1