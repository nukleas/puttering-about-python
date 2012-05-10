#AutoURL-Related Documents 
#By Nukleas
#This script pulls URLS from a list file, pulls their title using BeautifulSoup, and outputs them into an output file all ready for additional editing
#
import urllib2
import sys
import urlparse
from sys import argv
from BeautifulSoup import BeautifulSoup
from derrida_functions import *
pulled_url = ""
title_set = []
rd_rawfile=open("RDURL")
while True:
	pulled_url = rd_rawfile.readline().strip()
	checked_URL = checkURL(pulled_url)
	if checked_URL == 0: break
	soup=makeSoup(checked_URL)
	if not soup.head.find(attrs={"name" : "article_title"}): # Yo dawg, if this doesn't find anything, lets look elsewhere.
		line=soup.find('ti') #how about <ti> tages?
		if not line:break # Oh well. Next!
		text=line.contents[0].title() #Extract that data
		article_title=unescape(text.title()) # Pwn those unicodes
		print article_title # Just cause I like seeing the program work.
		title_set.append([article_title, checked_URL]) # Add the results to the list
	if soup.head.find(attrs={"name" : "article_title"}): # Yeah man, direct XML metadata.
		for line in soup.head.findAll(attrs={"name" : "article_title"}): 
			article_title = unescape(line.get('content')) # Might as well merge the whole unescape thing.
			print article_title # Cause why not, right?
			title_set.append([article_title, checked_URL])
#print title_set # for debugging purposes
print "Final Processing Stage: Compiling Related Documents"
final_set=[]
for line in title_set:
	fullline="|"+line[0]+"|"+line[1]+"||" # Add all the silly stuff we use
	final_set.append(fullline)
final_final="~".join(final_set)
print final_final
output_file=open('output.txt', 'w')
output_file.write(final_final)