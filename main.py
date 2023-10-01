import requests
import datetime
import os
from twilio.rest import Client

today = datetime.date.today()

yesterday = today - datetime.timedelta(days = 2)
day_before = today - datetime.timedelta(days = 3)
print(yesterday,day_before)


# News API key, from https://newsapi.org/
NEWS_SITE = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "key"
NEWS_PARAMETERS = {
    'q':'IBM+stock',
    'qInTitle':'IBM',
    'from':f'{day_before}',
    'apiKey':NEWS_API_KEY

}

# all these need to be changed to valid credentials

# Alpha Vantage API key, from https://www.alphavantage.co/
AV_API_KEY = "key"
STOCK = "https://www.alphavantage.co/query"
STOCK_PARAMETERS = {
    'function':'TIME_SERIES_DAILY',
    'symbol':'IBM',
    'apikey': AV_API_KEY
}



# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "sid"
auth_token = "token"

client = Client(account_sid, auth_token)


response_stock = requests.get(url=STOCK, params=STOCK_PARAMETERS)
response_stock.raise_for_status()
stock_data = response_stock.json()
needed_stock_data = stock_data["Time Series (Daily)"][f"{yesterday}"]["4. close"]
needed_stock_data2 = stock_data["Time Series (Daily)"][f"{day_before}"]["4. close"]

differnce_of_stocks = (float(needed_stock_data2) - float(needed_stock_data))
if differnce_of_stocks >0:
    updown = '👍'
else:
    updown = '👎'
diff_percentage = round((abs(differnce_of_stocks)/float(needed_stock_data))*100)
if diff_percentage> 0:
    print('get news')
    response_news = requests.get(url=NEWS_SITE, params=NEWS_PARAMETERS)
    response_news.raise_for_status()
    data_news = response_news.json()["articles"]
    data_fortext = data_news[:3]
    list_ofnews = [f"Headline : {data_news['title']} \nBrief:{data_news['description']}" for data_news in data_fortext]
    print(data_fortext)
    print(list_ofnews)
    for text in list_ofnews:
        message = client.messages.create(
            body=f'Stock:{updown}\n{text}',
            from_='+12565734672',
            to='contact_number'
        )


else:
    print(f'profit {abs(differnce_of_stocks)}$')









# Twilio SID & TOKEN, from https://www.twilio.com/
TWILIO_SID = "mytwiliosid"
TWILIO_TOKEN = "mytwiliotoken"
# Twilio phone number to send the SMS from
TWILIO_NUMBER = "notmynumber"
# real phone number to send the SMS to
TARGET_NUMBER = "mynumber"
