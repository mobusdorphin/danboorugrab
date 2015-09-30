#!/usr/bin/python

import requests
import re
import wget
import sys
import os


###########################
# Set some variables

outputString = ''
urlList = []
notFound = True
tagString = ''
urlString = ''

###########################
# Determine tags to search

try: 
  sys.argv[1]
  for i in sys.argv[1:]:
    tagString += i + '+'
  tagString = tagString[:-1]
except IndexError:
  tagString = raw_input('Enter tags separated by spaces or by +:  ').replace(' ', '+')
sourceUrl = 'http://danbooru.donmai.us/posts?tags=' + tagString

###########################
# Keep checking pages as long as we're getting a result and tabulate each URL to a list

while notFound:
  print "Checking page %s" % sourceUrl
  try: r = requests.get(sourceUrl)
  except: 
    print 'Request failed, retrying...'
    try: r = requests.get(sourceUrl)
    except: 
      print 'Request failed, retrying...'
      try: r = requests.get(sourceUrl)
      except: 
        print 'Request failed after three attempts.  Aborting'
        exit(1)
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
for i in urlList:
  urlString += i + '\n'

###########################
# Confirm with user everything is kosher before writing to disk

print 'Found %s items.  List URLs? y/N' % len(urlList)
toList = raw_input()
toList = toList.lower()
if toList == 'y' or toList == 'yes':
  print urlString

print 'Save URL list? y/N'
saveList = raw_input()
saveList = saveList.lower()
if saveList == 'y' or saveList == 'yes':
  f = open(tagString + '.txt', 'w')
  f.write(urlString)
  f.close()

print 'Download them all? y/N'
downloadThem = raw_input()
downloadThem = downloadThem.lower()

###########################
# Have user specify a target directory 

if downloadThem == 'y' or downloadThem == 'yes':
  dirNotConfirmed = True
  while dirNotConfirmed:
    directory = raw_input('Save in what directory?:  (Leave blank for current dir)')
    try:
      if directory == '': # If blank, use current directory
        break
      if os.path.isdir(directory): # If directory exists, change to it
        os.chdir(directory)
      elif os.path.isfile(directory): # If exists but is a file, complain and try again
        print 'File exists but is not a directory.  Please enter a valid directory\n'
        continue
      else:
        print '%s does not exist.  Create?:  y/N' % directory # Otherwise, offer to create the directory
        createDirectory = raw_input()
        createDirectory = createDirectory.lower()  
        if createDirectory == 'y' or createDirectory == 'yes':
          if os.path.exists(directory):
#                 If for some reason the path is created between the time we checked if the file 
#                 exists and when we want to create it, complain and try again
            print 'Something went terribly wrong.  Please specify another directory' 
            continue
          os.makedirs(directory)
          os.chdir(directory)
        else:
          continue
      print 'Preparing to download %s files to %s.  Confirm y/N' % (len(urlList), os.getcwd())
      confirmation = raw_input() # Finally, confirm that everything we've done is fully kosher for passover
      confirmation = confirmation.lower()
      if confirmation == 'y' or confirmation == 'yes': # If so, allow dirNotConfirmed to change value, which  
#                                               will break the loop allowing us all to move on with our lives
        pass
      else:            # Otherwise, we do it all over again
        continue
      dirNotConfirmed = False
    except OSError as oops:
      print oops

###########################
# Finally, download the things

  dlcount = 1
  for i in urlList:
    filename = re.search('data/(.+)', i).group(1)
    print '\nDownloading file %s (%s of %s)' % (filename, dlcount, len(urlList))
    if os.path.isfile(filename):
      print 'File Exists, skipping'
      dlcount += 1
      continue
    wget.download(i)
    dlcount += 1

print '\n'
exit(0)
