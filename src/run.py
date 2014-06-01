# -*- coding: utf-8 -*-

from xml.dom.minidom import parseString
import urllib
import time
import sys
import string
import os
print sys.getdefaultencoding()

def returnURL(node):
  url = node.getElementsByTagName('guid')[0].toxml()
  return url.replace('<guid>','').replace('</guid>','')

def getFilenameFromURL(url):
  filename = url.rpartition('/')[2]
  return filename

def getLength(node):
  return 1

def returnTitle(node):
  title = node.getElementsByTagName('title')[0].toxml()
  return title.replace('<title>','').replace('</title>','')

def reporthook(count, block_size, total_size):
  global start_time
  if count == 0:
    start_time = time.time()
    return
  duration = time.time() - start_time
  progress_size = int(count * block_size)
  speed = int(progress_size / (1024 * duration))
  percent = int(count * block_size * 100 / total_size)
  sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
    (percent, progress_size / (1024 * 1024), speed, duration))
  sys.stdout.flush
  
def format_filename(s):
  valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
  filename = ''.join(c for c in s if c in valid_chars)
  return filename
  
  
  
 
xmlPrefix = 'http://thebrewingnetwork.com/'
download_prefix = 'http://s125483039.onlinehome.us/archive/'
xmlFiles = ['brewstrong.xml', 'jamilshow.xml','lunchmeet.xml', 'sundayshow.xml', 'drhomebrew.xml', 'homebrewedchef.xml']



data = ''
pairs = {}
for i in xmlFiles:
  f = urllib.urlopen(xmlPrefix + i)
  data = f.read()
  f.close()
  dom = parseString(data)
  for thing in dom.getElementsByTagName('item'):
    length = getLength(thing)
    title = returnTitle(thing)
    URL = returnURL(thing)
    URLFilename = getFilenameFromURL(URL)
    if URLFilename in pairs:
      print 'panic: ' + title +'; ' + URL
    else:
      pairs[URLFilename] = [title, URL, URLFilename, i]
i = 0

for key in pairs:
  print i, ' done, ', len(pairs)-i, ' to go\n'
  i +=1
  location = download_prefix + key
  local_name = format_filename([key][0]) + '.mp3'
  directory = pairs[key][3].partition('.')[0]
  if not os.path.exists(directory):
    os.makedirs(directory)
  urllib.urlretrieve(location, directory+'/'+local_name, reporthook)
