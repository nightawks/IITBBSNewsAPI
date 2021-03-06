try:
	import urllib.request as urllib2
except ImportError:
	import urllib2
from bs4 import BeautifulSoup
from datetime import datetime
import json
import twitter
import calendar

class News:

	@staticmethod
	def getNews () :
		'''
		Return a dictionary of top 30 news and their links
		No parameters reuired 
		'''
		result = []
		response = {}
		url = 'http://www.iitbbs.ac.in/news.php'
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page, 'html.parser')
		newsOl = soup.find('ol', attrs={'class': 'rectlist'})
		newsLi = newsOl.find_all('li')

		for link in newsLi:
			news = link.text.strip()
			
			if link.find('a').get('href')[:4] != 'http':
				link = 'http://www.iitbbs.ac.in/' + link.find('a').get('href')
			else:
				link = link.find('a').get('href')

			result.append({'text': news, 'url': link});

		response['count'] = len(newsLi)
		response['list'] = result
		return response

	@staticmethod
	def getEvents () :
		'''
		Return a dictionary of all listed upcoming events
		No parameters reuired 
		'''
		result = []
		response = {}
		url = 'http://www.iitbbs.ac.in/events.php'
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page, 'html.parser')
		newsOl = soup.find('ul', attrs={'class': 'orangearrow'})
		newsLi = newsOl.find_all('li')

		for link in newsLi:
			event = link.text.strip()
			
			if link.find('a').get('href')[:4] != 'http':
				link = 'http://www.iitbbs.ac.in/' + link.find('a').get('href')
			else:
				link = link.find('a').get('href')

			result.append({'text': event, 'url': link});

		response['count'] = len(newsLi)
		response['list'] = result
		return response


	@staticmethod
	def getNotices () :
		'''
		Return a dictionary of all listed Notices
		No parameters reuired 
		'''
		result = []
		response = {}
		url = 'http://www.iitbbs.ac.in/notices.php'
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page, 'html.parser')
		newsOl = soup.find('ul', attrs={'class': ''})
		newsLi = newsOl.find_all('li')

		for link in newsLi:
			notice = link.text.strip()
			
			if link.find('a').get('href')[:4] != 'http':
				link = 'http://www.iitbbs.ac.in/' + link.find('a').get('href')
			else:
				link = link.find('a').get('href')

			result.append({'text': notice, 'url': link});

		response['count'] = len(newsLi)
		response['list'] = result
		return response

	@staticmethod
	def getBusSchedule ():
		response = {}
		url = 'http://www.iitbbs.ac.in/transportation.php'
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page, 'html.parser')
		div = soup.find('div', attrs={'class': 'col-md-4'})
		anchors = div.find('p').find_all('a')

		for anchor in anchors:
			ftype = 'pdf' if anchor['href'][-3:] == 'pdf' else 'xls' 
			response[ftype] = 'www.iitbbs.ac.in/' + anchors[0]['href'][3:]

		return response

	@staticmethod
	def getTimeTable(roll, subject, day):

		if day is not None:
			if str.isdigit(day):
				day = int(day)
				day = calendar.day_name[day].lower()
			else:
				day = day.lower()

		with open("mappings.json","r") as f:
			subject_map = json.loads(f.read())
		if subject is not None and subject in subject_map:
			subject = subject_map[subject]

		year = str(min((datetime.now().year%100 - int(roll[0:2]) + 1), 4))
		today = str(datetime.today().weekday())
		branch = str(roll[2:4])
		dual_or_single = str(roll[5:6])
		dest = "res/" + year + "/" + branch + "/"\
				+ dual_or_single + "/" + "data.json"

		try:
			with open (dest, "r") as f:
				data = json.loads(f.read())
			if subject is None and day is None:
				return data
			elif subject is None:
				res=[]
				for subject in data['subjects']:
					if len(subject['timetable'][day]) != 0:
						val = {}
						val['subject'] = subject['subject']
						val['timings'] = subject['timetable'][day]
						res.append(val)
				return {'status':'Ok','subjects':res}
			elif day is None:
				res = {}
				for sub in data['subjects']:
					if sub['subject']==subject:
						res = sub['timetable']
				return {'status':'Ok','data':res}
			else:
				res=[]
				filtered_value = []
				for sub in data['subjects']:
					if len(sub['timetable'][day]) != 0:
						val = {}
						val['subject'] = sub['subject']
						val['timings'] = sub['timetable'][day]
						res.append(val)
				for result in res:
					print(result['subject'])
					if result['subject'] == subject:
						filtered_value.append(result['timings'])
				return {'status':'Ok','data':filtered_value}
		except Exception as e:
			print(e)
			return {'status':'404','data':[]}

	@staticmethod
	def getTweets():
		response = {}
		res = twitter.default_function()
		response['count'] = len(res)
		response['list'] = res
		return response