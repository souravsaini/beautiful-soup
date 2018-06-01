#!/usr/bin/python

from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from sys import argv, exit

SERVER = "https://weather.com"
PARSER = 'lxml'

def daily(doc):
	city_name = doc.find('h1', class_='today_nowcard-location').text
	city_temp = doc.find('div', class_="today_nowcard-temp").find("span").text
	temp_phrase = doc.select('.today_nowcard-phrase')[0].text 
	feels_like = doc.select('.deg-feels')[0].text


	print("City       : {}".format(city_name))
	print("Temperature: {}".format(city_temp))
	print("Weather    : {}".format(temp_phrase))
	print("Feels like : {}".format(feels_like))


def hourly(doc):
	link = None
	anchors = doc.find_all('a')
	for anchor in anchors:
		if anchor['href'].find('hourbyhour') >= 0:
			link = anchor
			break

	url = SERVER+link['href']
	soup = BeautifulSoup(request.urlopen(url).read(), PARSER)

	hourly_time_list = soup.select('.hourly-time')
	hourly_date_list = soup.select('.hourly-date')
	description_list = soup.select('td.description')
	temp_list = soup.select('td.temp span')
	feels_list = soup.select('td.feels span')
	precipitation_list=soup.select('td.precip div > span:nth-of-type(2)')
	humidity_list=soup.select('td.humidity > span')

	# TODO
	# Precipitation, Humidity, Wind

	for index in range(len(hourly_time_list)):
		print("On {} ({}) weather is {}, temperature is {}, it feels like {}, its precipitation is {} and humidity is {}"
			.format(
				hourly_time_list[index].text, 
				hourly_date_list[index].text, 
				description_list[index].text,
				temp_list[index].text,
				feels_list[index].text,
				precipitation_list[index].text,
				humidity_list[index].text
			)
		)

#def weekly(doc):


def main(lat=31.53, long=75.92, type=''):
	try:
		url = SERVER + "/en-IN/weather/today/l/{},{}?temp=c".format(lat, long)
		html_doc = request.urlopen(url).read()
		doc = BeautifulSoup(html_doc, PARSER)
		# print(doc.prettify())

		if type == '':
			daily(doc)
		elif type == 'hourly':
			hourly(doc)
#		elif type== 'weekly':
#			weekly(doc)

	except HTTPError:
		print('Latitute and Longitute are invalid')
		exit(1)

if __name__ == '__main__':
	try:
		lat = float(argv[1])
		long = float(argv[2])
		main(lat, long, argv[3])
	except IndexError:
		main()
	except ValueError:
		main(type=argv[1])