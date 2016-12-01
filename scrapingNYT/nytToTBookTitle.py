from lxml import html
import requests
from bs4 import BeautifulSoup
import urllib2
from urllib2 import urlopen, HTTPError
import string
import pickle

myfile = open('listTooManyNYTarticles','rb')
object_file = pickle.load(myfile)

urlAdditions = list(open('metaAdditions.csv', 'r'))
nameAdded = open('metaAdditionsTitles.csv', 'w').close()
nameAdded = open('metaAdditionsTitles.csv', 'a')

acceptableTypes = ['(book)', '(play)', '(tv program)', '(boo']

def getUrl(url):
	p = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
	soup = BeautifulSoup(p, "lxml")

	head = soup.find("head")
	keywords = head.find("meta", {'name':'keywords'})['content']
	return keywords



	#title = mainCol.find("h1", "title")
	#author = mainCol.find("h2", "author")

def processString(string):
	words = string.split(',')
	name = words[-1].lower()
	finalName = ''
	if any(x in name for x in acceptableTypes):
		finalName = name.split('(')
		del finalName[-1]
		finalName = ' '.join(finalName)
		return finalName
	else:
		for word in words:
			if any(x in word.lower() for x in acceptableTypes):
				finalName = word.split('(')
				del finalName[-1]
				finalName = ' '.join(finalName)
				return finalName
		print string
		print 'ALERT'
		return

def main():
	del urlAdditions[0]
	for row in urlAdditions:
		line = row.split(',')
		if line[6] == 'y':
			continue
		filename = line[1]
		reviewer = line[2]
		reviewer_gender = line[3]
		author = line[4]
		authorGender = line[5]
		numAuthors = line[6]
		date = line[7]
		url = line[8]
		
		try:
			string = getUrl(url)
			finalName = processString(string)
			finalName = finalName.encode('utf-8')
			row = row[:-1]
			nameAdded.write(row + ',' + finalName + '\n')
		except Exception, e:
			if '01SCHULMA.html' in url:
				raise
			print e
			print url
			print row



if __name__ == '__main__':
   main()