from selenium import webdriver
import os
import time
import pandas as pd
from datetime import datetime
from datetime import timedelta

os.chdir('C:/Users/HF_BI/Documents/Flights/Output')
template = 'https://www.google.com/flights/#search;f=SYD;t=LAX;d=2017-01-29;r=2017-02-05'

def cleanToAirport(dfField):
    toAirportCleaned = []
    for item in dfField:
        new_air = item.split(',')
        output = []
        for value in new_air:
            output.append(value.strip())
        toAirportCleaned.append(output)

    return toAirportCleaned

def cleanDate(dfField):
    cleanedDates = []
    for item in dfField:
        cleanedDates.append(datetime.strptime(item,'%d/%m/%Y').strftime('%Y-%m-%d'))
    return cleanedDates

'''
sleepTime = 6
fromAirport = ['SYD']
toAirport = ['LAX']
fromDate = ['2017-01-29']
toDate = ['2017-02-05']
maxPrice = ['1000']
oneWayBl = [True]
oneWay = []
if oneWayBl[0] == True:
    oneWay.append('tt=o')
'''

# Parameters
sleepTime = 6
df = pd.read_csv('Input.csv')
fromAirport = list(df.from_airport)
toAirport = list(df.to_airports)
fromDateStart = cleanDate(df.from_date_start)
fromDateEnd = cleanDate(df.from_date_end)
duration = list(df.min_duration)
maxPrice = df.max_price
oneWay = []
for bl in df.one_way:
    if bl==True:
        oneWay.append('tt=o')
    else:
        oneWay.append('')

indRow = 0

flightKey = indRow

toDateStart = datetime.strftime(datetime.strptime(fromDateStart[indRow],'%Y-%m-%d') + timedelta(days=int(duration[indRow])), '%Y-%m-%d')

os.mkdir('%sairport_%s' % (time.strftime("%Y%m%d-%H%M%S"),indRow))
os.chdir('%sairport_%s' % (time.strftime("%Y%m%d-%H%M%S"),indRow))

# iterate through toAirports

url = 'https://www.google.com/flights/#search;f=%s;t=%s;d=%s;r=%s;%s;mp=%s' % (
    fromAirport[indRow], toAirport[indRow], fromDateStart[indRow], toDateStart, oneWay[indRow], maxPrice[indRow])
print('url: %s' % url)
driver = webdriver.Firefox()
driver.get(url)
time.sleep(sleepTime)
pageSource = driver.page_source
driver.quit()
params = pd.DataFrame({'flight_key':flightKey,
                       'from_airport':fromAirport[indRow],
                       'to_airport':toAirport[indRow],
                       'from_date':fromDateStart[indRow],
                       'to_date':toDateStart[indRow],
                       'max_price':maxPrice[indRow],
                       'one_way_flag':oneWay[indRow]})

params.to_csv('params_%s_%s.csv'%(indRow), index=None)

with open('data_%s_%s.txt'%(indRow), 'w+') as file:
    file.write(pageSource)

# with contextlib.closing(webdriver.Firefox()) as browser:
#     browser.get(url)
#     pageSource = browser.page_source




