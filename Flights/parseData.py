from bs4 import BeautifulSoup
import os
import pandas as pd

os.chdir('C:/Users/HF_BI/Documents/Flights/Output')

''' Get page data from Google Flights'''

ind = [0]
with open('data%s.txt'%str(ind[0]), 'r+') as file:
    pageSource = file.read()

''' Parse page data'''

soup = BeautifulSoup(pageSource, 'lxml')

# Best flights
flights = []
strFlight = ""
for link in soup.findAll('a'):
    if 'google.com/flights/#search' in str(link):
        flights.append(link)
        strFlight += str(link)

flightSoup = BeautifulSoup(strFlight, 'lxml')

'''Parsing rules for Google Flights'''

def findPrices():
    prices = []
    for flight in flightSoup.findAll('a'):
        for price in flight.findChildren()[2]:
            prices.append(price)
    return prices

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

def findDuration():
    durations = []
    for flight in flightSoup.findAll('a'):
        for duration in flight.findAll('div', class_='EESPNGB-d-D'):
            durations.append(duration.text)
    return durations

def findHref():
    hrefs = []
    for ahref in flightSoup.findAll('a'):
        hrefs.append(ahref.get('href'))
    return hrefs

def findService():
    services = []
    for flight in flightSoup.findAll('a'):
        for company in flight.findAll('div', class_='EESPNGB-d-j'):
            if len(company.findAll('div')) > 0:
                for subcompany in company.findAll('div', class_='EESPNGB-d-k'):
                    content = ""
                    for contents in subcompany.contents:
                        if str(contents) != '<br/>':
                            content += str(contents) + ", "
                    services.append(content.rstrip()[:-1])

            else:
                services.append(company.text)
    return services

def findAirport():
    # If searched multiple airports, find the correct one
    pass

prices = findPrices()
times = findTime()
durations = findDuration()
hrefs = findHref()
services = findService()

''' Returning data in a pandas dataframe'''
df = pd.DataFrame({'flight_key':[ind[0] for x in prices],
                   'price':[int(x[1:]) for x in prices],
                   'time':times,
                   'duration':durations,
                   'href':hrefs,
                   'airline':services})

dfParams = pd.read_csv('params0.csv', encoding='ISO-8859-1')
dfAll = pd.merge(left=df, right=dfParams, how='inner', left_on='flight_key', right_on='flight_key')
print(dfAll.head())
dfAll.to_csv('data0.csv', index=None)