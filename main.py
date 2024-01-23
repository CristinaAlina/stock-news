import requests
import os
from datetime import datetime as dt
from datetime import timedelta
import calendar
from twilio.rest import Client

STOCK = "TSLA"


def get_previous_day_date(input_date: dt) -> str:
    """Returns previous day date according to input date, not include the weekend dates, in string format."""
    day_of_week = calendar.weekday(input_date.year, input_date.month, input_date.day)

    if day_of_week == 0:
        previous_day_date = input_date - timedelta(days=3)
    elif day_of_week == 6:
        previous_day_date = input_date - timedelta(days=2)
    else:
        previous_day_date = input_date - timedelta(days=1)

    return previous_day_date.strftime("%Y-%m-%d")


def get_close_price(input_date_str: str) -> float:
    """Returns close price from json data format according to input date string format."""
    global alpha_avantage_data

    return float(alpha_avantage_data["Time Series (Daily)"][input_date_str]["4. close"])


## Used https://www.alphavantage.co
# Find out if STOCK price increase/decreases by 5% between yesterday and the day before yesterday.
ALPHA_AV_API_KEY = os.environ.get("ALPHAAV_API_KEY")
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_AV_API_KEY
}
response = requests.get(url="https://www.alphavantage.co/query", params=parameters)
response.raise_for_status()

# Json includes datetime data without weekend dates
all_json_data = response.json()

today_date = dt.today()

# Get yesterday and previous day of yesterday dates in format %Y-%m-%d
yesterday_date = get_previous_day_date(today_date)
prv_yesterday_date = get_previous_day_date(dt.strptime(yesterday_date, "%Y-%m-%d"))

# Get closing prices for target dates
yesterday_closing_price = get_close_price(yesterday_date)
prv_yesterday_closing_price = get_close_price(prv_yesterday_date)

# Get the percentage of increase or decrease difference between those two dates
difference_closing_prices = round(float(yesterday_closing_price - prv_yesterday_closing_price), 2)
percentage_closing_prices = round(difference_closing_prices / yesterday_closing_price * 100, 2)

## Used https://newsapi.org
# Get the first 3 news pieces for the STOCK.
if abs(percentage_closing_prices) >= 5:
    news_api_key = os.environ.get("NEWS_API_KEY")
    news_api_parameters = {
        "q": STOCK,
        "searchIn": "title,description",
        "from": prv_yesterday_date,
        "to": yesterday_date,
        "pageSize": 3,
        "apiKey": news_api_key
    }
    news_api_response = requests.get(url="https://newsapi.org/v2/everything", params=news_api_parameters)
    news_api_response.raise_for_status()
    news_api_data = news_api_response.json()

    articles_list = []
    articles_list = [{"Headline": dict_data["title"], "Brief": dict_data["description"]}
                     for dict_data in news_api_data["articles"]]

    ## Used https://www.twilio.com
    # Send a separate message with the percentage change and each article's title and description to your phone number.
    TWILIO_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    your_phone_number = os.environ.get("MY_PHONE_NUMBER")
    TWILIO_phone_number = "+18147525328"  # This is a random phone number that TWILIO will generate for you

    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    client = Client(TWILIO_account_sid, TWILIO_auth_token)
    for article in articles_list:
        if percentage_closing_prices < 0:
            rise_or_fall_sign = "🔻"
        else:
            rise_or_fall_sign = "🔺"
        msg_body = (f"{STOCK}: {rise_or_fall_sign}{abs(percentage_closing_prices)}%\n"
                    f"Headline: {article["Headline"]}.\n"
                    f"Brief: {article["Brief"]}")
        message = client.messages.create(body=msg_body, from_=TWILIO_phone_number, to=your_phone_number)

        print(message.status)
