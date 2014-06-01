# -*- coding: utf-8 -*-

from xml.dom.minidom import parseString
import urllib
import time
import sys
print sys.getdefaultencoding()

def returnURL(node):
  url = node.getElementsByTagName('guid')[0].toxml()
  return url.replace('<guid>','').replace('</guid>','')

def getFilenameFromURL(url):
  filename = url.rpartition('/')[2]
  return filename

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
  
  

data = ''
pairs = {}
xmlPrefix = 'http://thebrewingnetwork.com/'
download_prefix = 'http://s125483039.onlinehome.us/archive/'
xmlFiles = ['brewstrong.xml', 'jamilshow.xml','lunchmeet.xml', 'sundayshow.xml', 'drhomebrew.xml', 'homebrewedchef.xml']
for i in xmlFiles:
  f = urllib.urlopen(xmlPrefix + i)
  data = f.read()
  f.close()
  dom = parseString(data)
  for things in dom.getElementsByTagName('item'):
    title = returnTitle(things)
    if title in pairs:
      if pairs[title] == returnURL(things):
	print 'panic: ' + title
    else:
      pairs[title] = returnURL(things)
print len(pairs)

"""
for i in pairs:
  print 'key is:\t', i, '\tvalue is:\t', pairs[i]
"""
"""
tmp_key = 'The Session 03-24-14 Left Hand Brewing'
print 'key is:\t', tmp_key, '\nvalue is:\t', pairs[tmp_key]
print 'key is:\t', tmp_key, '\nvalue is:\t', pairs[tmp_key].rpartition('/')[2]
filename = pairs[tmp_key].rpartition('/')[2]
location = download_prefix + filename
print 'key is:\t', tmp_key, '\nlocation is:\t', location
local_name = tmp_key + '.mp3'
print 'key is:\t', tmp_key, '\nlocal_name is:\t', local_name

urllib.urlretrieve(location, local_name, reporthook)
"""
