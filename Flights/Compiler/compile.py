from selenium import webdriver
import os
import time
from bs4 import BeautifulSoup

os.chdir('C:/Users/HF_BI/Documents/Flights/Output')

'''Gather Data'''

template = 'https://www.google.com/flights/#search;f=SYD;t=LAX;d=2017-01-29;r=2017-02-05'
url = 'https://www.google.com/flights'

# parameters

sleepTime = 6
fromAirport = 'SYD'
toAirport = 'LAX'
fromDate = '2017-01-29'
toDate = '2017-02-05'
maxPrice = '1000'

url = 'https://www.google.com/flights/#search;f=%s;t=%s;d=%s;r=%s;mp=%s' %(
    fromAirport, toAirport, fromDate, toDate, maxPrice)

# with contextlib.closing(webdriver.Firefox()) as browser:
#     browser.get(url)
#     pageSource = browser.page_source

driver = webdriver.Firefox()
driver.get(url)
time.sleep(sleepTime)
pageSource = driver.page_source
driver.quit()

with open('data.txt', 'w+') as file:
    file.write(pageSource)

'''Parse Data'''

soup = BeautifulSoup(pageSource, 'lxml')

# Best flights
flights = []
strFlight = ""
for link in soup.findAll('a'):
    if 'google.com/flights/#search' in str(link):
        flights.append(link)
        strFlight += str(link)
        # print(link)
        # print('\nnext\n')

flightSoup = BeautifulSoup(strFlight, 'lxml')

def findPrices():
    prices = []
    for flight in flightSoup.findAll('a'):
        for price in flight.findChildren()[2]:
            prices.append(price)
    return prices

prices = findPrices()

def findTime():
    data = []
    times = []
    for flight in flightSoup.findAll('a'):
        for timeData in flight.findChildren()[4]:
            data.append(str(timeData))
    for element in data:
        elements = BeautifulSoup(element, 'lxml')
        for spans in elements.findAll('div', class_='EESPNGB-d-Xb'):
            times.append(spans.text)
    return times
times = findTime()

def findDuration():
    durations = []
    for flight in flightSoup.findAll('a'):
        for duration in flight.findAll('div', class_='EESPNGB-d-D'):
            durations.append(duration.text)
    return durations

durations = findDuration()

for price, time, duration in zip(prices, times, durations):
    print(price, time, duration)