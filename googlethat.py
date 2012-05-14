import sys # Used to add the BeautifulSoup folder the import path
import urllib2 # Used to read the html document
import re
from sys import argv
from BeautifulSoup import BeautifulSoup
output=open("output.txt",'w')
output.truncate() #...but clear it first.
### Create opener with Google-friendly user agent
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
### Open page & generate soup
### the "start" variable will be used to iterate through 10pages.
search_query=raw_input()
url = "http://www.google.com/search?q="+search_query.replace(" ","+")
page = opener.open(url)
soup = BeautifulSoup(page)

	### Parse and find
	### Looks like google contains URLs in <cite> tags.
	### So for each cite tag on each page (10), print its bcontents (url)
for cite in soup.findAll('cite'):
	print "http://"+cite.text
	output.write("http://"+cite.text)
	output.write("\n")
output=open("output.txt")
url2=output.readline()
print url2
page2=urllib2.urlopen(url2)
soup2 = BeautifulSoup(page2)
string=""
output=open("output.txt",'w')
for line in soup2.head.title:
	totalstring=url2.strip()+'|'+line.strip()
	print totalstring
	output.write(re.sub('[^A-Za-z0-9:\\/.,| &]+', '', totalstring))
print soup2.head.title