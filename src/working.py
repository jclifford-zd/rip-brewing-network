>>> from xml.dom.minidom import parseString
>>> f = open('xml/brewstrong.xml','rb')
>>> data = f.read()
>>> f.close()
>>> dom = parseString(data)
>>> for i in dom.getElementsByTagName('guid'):
...     print i.toxml().replace('<guid>','').replace('</guid>','')

>>> f = open('urls.txt','wb')
>>> for i in dom.getElementsByTagName('guid'):
...     f.write(i.toxml().replace('<guid>','').replace('</guid>',''))
...     f.write('\n')


from xml.dom.minidom import parseString
files = ['xml/brewstrong.xml', 'xml/jamilshow.xml','xml/lunchmeet.xml', 'xml/sundayshow.xml', 'xml/drhomebrew.xml', 'xml/homebrewedchef.xml']
for i in files:
  f = open(i,'rb')
  data = f.read()
  f.close()
  dom = parseString(data)
  for i in dom.getElementsByTagName('guid'):
    print i.toxml().replace('<guid>','').replace('</guid>','')

f = open('urls.txt','wb')
for i in dom.getElementsByTagName('guid'):
    f.write(i.toxml().replace('<guid>','').replace('</guid>',''))
    f.write('\n')


=================

itemlist = dom.getElementsByTagName('item')
print itemlist.toxml()

=================


def returnURL(node):
  url = node.getElementsByTagName('guid')[0].toxml()
  url.replace('<guid>','').replace('</guid>','')

def getFilenameFromURL(url):
  filename = url.rpartition('/')[2]

def returnTitle(node):
  title = node.getElementsByTagName('title')[0].toxml()
  title.replace('<title>','').replace('</title>','')
  
urllib.urlretrieve(url, filename)



http://www.thebrewingnetwork.com/membersarchive/ses_2014-05-19_Pendragon.mp3
http://s125483039.onlinehome.us/archive/ses_2014-05-19_Pendragon.mp3

