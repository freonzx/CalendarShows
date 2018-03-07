import requests
from bs4 import BeautifulSoup
import datetime
from colorama import init, Fore, Back, Style
from termcolor import colored

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

def isWeekDay(day):
	weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	for weekday in weekdays:
		if weekday in day:
			return True
	return False

def return_soup(url):
	source_code = requests.get(url, headers=headers)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, "html.parser")
	return soup
	
def searchRARBG(query):
	url = 'https://rarbg.is/torrents.php?category=18;41;49&search='+query+'&order=seeders&by=DESC'
	soup = return_soup(url)
	for link in soup.findAll('tr', {'class' : 'lista2'}):
		for k in link.findAll('a', href=True):
			if '/torrent/' in k['href']:
				return 'https://rarbg.is'+k['href']
	return False

url = 'https://www.pogdesign.co.uk/cat/'
init()

soup = return_soup(url)
series = open("series.txt","r")
lines = series.read().splitlines()
today = datetime.datetime.today().day
dayPrinted = False

# To be implemented a way to return the magnet links to a dictionary
magnet_dict = {}
episodes = []

for day in soup.findAll(True, {'class':['day','today']}):
	links = day.findAll('a')
	dayname = links[0].text
	daynumber = int(day.findAll('span', {'class' : 'sp1'})[0].text)
			
	for index, link in enumerate(links):
		if daynumber < today:
			if link.text in lines:
				if dayPrinted == False:
					print(colored(dayname, 'red'))
					dayPrinted = True
				episode_name = link.text+' '+links[index+1].text
				print(colored('\t'+episode_name, 'red'))
				episodes.append(episode_name)
				
				
		if daynumber >= today:
			
			if link.text in lines:
				if dayPrinted == False:
					print(colored(dayname, 'green'))
					dayPrinted = True
				print(colored('\t'+link.text + ' ' + links[index+1].text, 'yellow'))
	dayPrinted = False

print(colored('#############################################', 'green'))
print(colored('Looking for torrents of:', 'green'))
print(colored('#############################################', 'green'))
print(colored(episodes, 'yellow'))
for each in episodes:
	result = searchRARBG(each)
	if result:
		print (colored(result,'yellow'))
	else:
		print(colored('Something went wrong','red'))
		
input('DONE')
