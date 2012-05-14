#AutoURL
#By Nader Heidari
#This script pulls URLS from a list file, pulls their title using BeautifulSoup, and outputs them into an output file all ready for additional editing
#
import urllib2
import sys
import urlparse
import re
import htmlentitydefs
from sys import argv
from BeautifulSoup import BeautifulSoup #Need that soup.
from derrida_functions import *
url=""
source_text=open("URL.txt") # Open the URL file.
output=open("output.txt",'w') #Open the output file, make it writable
output.truncate() #...but clear it first.
while True:
	url=source_text.readline()# Pull a line
	if not url: break # If it's empty, end the program
	if not urlparse.urlparse(url).scheme: # If the line isn't a good URL, maybe it just needs an http:// added. Add that.
		url = "http://"+url
	soup=""
	try:
		soup=makeSoup(url) # Makin' that soup!
	except:
		print "URLs are not proper. One ought to fix that in the URL file." # Y U NO GOOD INPUT
		break
	string=""
	try:
		for line in soup.head.title:
			string+=line.replace("\n","")
			totalstring=url.strip()+'|'+string.strip()
			print totalstring
			finalstring=unescape(totalstring)
			output.write(re.sub('[^A-Za-z0-9:\\/.,| &]+', '', finalstring))
			output.write("\n")
	except: print url+" is invalid. Please check URL file"
output.close()