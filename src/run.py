# -*- coding: utf-8 -*-

from xml.dom.minidom import parseString
import urllib
import time
import sys
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
  sys.stdout.flush()
  
 
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
# for i in pairs:
#   print i, ':\t', pairs[i][0]
print len(pairs)

tmp_key = 'cybi01-31-11.mp3'
location = download_prefix + tmp_key
print 'key is:\t', tmp_key, '\nlocation is:\t', location
local_name = pairs[tmp_key][0] + '.mp3'
directory = '~/'+pairs[tmp_key][3].partition('.')[0]
print directory
if not os.path.exists(directory):
  os.makedirs(directory)
print 'key is:\t', tmp_key, '\nlocal_name is:\t', local_name
urllib.urlretrieve(location, directory+'/'+local_name, reporthook)

