# -*- coding: utf-8 -*-

from xml.dom.minidom import parseString
from datetime import datetime
import requests
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

def returnPubDate(node):
  title = node.getElementsByTagName('pubDate')[0].toxml()
  return title.replace('<pubDate>','').replace('</pubDate>','')

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

def downloadFile(req, directory, local_name):
  dl = 0
  total_length = req.headers.get('content-length')
  with open(directory+'/'+local_name, 'wb') as fd:
    for chunk in req.iter_content(chunk_size=1024):
      dl += len(chunk)
      fd.write(chunk)
      done = int(50 * dl / int(total_length))
      sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
      sys.stdout.flush
  
  
  
 
xmlPrefix = 'http://thebrewingnetwork.com/'
download_prefix = 'http://s125483039.onlinehome.us/archive/'
# xmlFiles = ['brewstrong.xml', 'jamilshow.xml','lunchmeet.xml', 'sundayshow.xml', 'drhomebrew.xml', 'homebrewedchef.xml']
xmlFiles = ['brewstrong.xml', 'jamilshow.xml','lunchmeet.xml', 'sundayshow.xml', 'homebrewedchef.xml']
# xmlFiles = ['homebrewedchef.xml']

runDownload = 1

data = ''
downloaded = 0
existingSize = 0
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
    pubDate = returnPubDate(thing)
#    print pubDate
    d = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S %Z')
    pubDate = d.strftime('%Y-%m-%d')
#    print pubDate
    URLFilename = getFilenameFromURL(URL)
    if URLFilename in pairs:
      print 'panic: ' + title +'; ' + URL
    else:
      pairs[URLFilename] = [title, i, downloaded, existingSize, pubDate]

# check what files are downloaded
for key in pairs:
  local_name = pairs[key][4] + ' ' + format_filename(pairs[key][0]) + '.mp3'
  directory = pairs[key][1].partition('.')[0]
  if os.path.isfile(directory+'/'+local_name):
    pairs[key][2] = 1
    pairs[key][3] = os.path.getsize(directory+'/'+local_name)
'''
for keys,values in pairs.items():
  print(keys)
  print(values)
'''

i = 0
for key in pairs:
  i += 1
  location = download_prefix + key
  local_name = pairs[key][4] + ' ' + format_filename(pairs[key][0]) + '.mp3'
  local_length = pairs[key][3]
  directory = pairs[key][1].partition('.')[0]
  if not os.path.exists(directory):
    os.makedirs(directory)
  print i, ': ', directory+'/'+local_name, '\t\t'
  r = requests.get(location, stream=True)
  remote_length = int(r.headers.get('content-length'))
  print 'pairs[key][2]:' , pairs[key][2], '\tlocal size: ' , local_length , '\tremote size: ' , remote_length
  if not pairs[key][2]:
    print 'Not down already, downloading'
    if runDownload:
      downloadFile(r, directory, local_name)
  elif (local_length < remote_length):
    print 'Local size less than remote size, downloading'
    if runDownload:
      downloadFile(r, directory, local_name)
  else:
    print 'Already done, local size: ' , pairs[key][3] , '\t  remote size: ' , remote_length
  print i, ' done, ', len(pairs)-i, ' to go\n'


'''
key = 'bs_042814QA.mp3'
location = download_prefix + key
local_name = format_filename(pairs[key][0]) + '.mp3'
directory = pairs[key][3].partition('.')[0]
if not os.path.exists(directory):
  os.makedirs(directory)
print i, ': ', directory+'/'+local_name, '\n'
'''


# urllib.urlretrieve(location, directory+'/'+local_name, reporthook)



