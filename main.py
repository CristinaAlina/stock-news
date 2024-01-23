import requests
import os
from datetime import datetime as dt
from datetime import timedelta
import calendar
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


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


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

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

# Output json data for tests
# alpha_avantage_data = {'Meta Data': {'1. Information': 'Daily Prices (open, high, low, close) and Volumes', '2. Symbol': 'TSLA', '3. Last Refreshed': '2024-01-22', '4. Output Size': 'Compact', '5. Time Zone': 'US/Eastern'}, 'Time Series (Daily)': {'2024-01-22': {'1. open': '212.2600', '2. high': '217.8000', '3. low': '206.2700', '4. close': '208.8000', '5. volume': '117952527'}, '2024-01-19': {'1. open': '209.9900', '2. high': '213.1900', '3. low': '207.5600', '4. close': '212.1900', '5. volume': '102260343'}, '2024-01-18': {'1. open': '216.8800', '2. high': '217.4500', '3. low': '208.7400', '4. close': '211.8800', '5. volume': '108595431'}, '2024-01-17': {'1. open': '214.8600', '2. high': '215.6700', '3. low': '212.0100', '4. close': '215.5500', '5. volume': '103164400'}, '2024-01-16': {'1. open': '215.1000', '2. high': '223.4900', '3. low': '212.1800', '4. close': '219.9100', '5. volume': '115355046'}, '2024-01-12': {'1. open': '220.0800', '2. high': '225.3400', '3. low': '217.1501', '4. close': '218.8900', '5. volume': '123043812'}, '2024-01-11': {'1. open': '230.5700', '2. high': '230.9300', '3. low': '225.3700', '4. close': '227.2200', '5. volume': '105873612'}, '2024-01-10': {'1. open': '235.1000', '2. high': '235.5000', '3. low': '231.2900', '4. close': '233.9400', '5. volume': '91628502'}, '2024-01-09': {'1. open': '238.1100', '2. high': '238.9646', '3. low': '232.0400', '4. close': '234.9600', '5. volume': '96705664'}, '2024-01-08': {'1. open': '236.1400', '2. high': '241.2500', '3. low': '235.3000', '4. close': '240.4500', '5. volume': '85166580'}, '2024-01-05': {'1. open': '236.8600', '2. high': '240.1196', '3. low': '234.9001', '4. close': '237.4900', '5. volume': '92240035'}, '2024-01-04': {'1. open': '239.2500', '2. high': '242.7000', '3. low': '237.7300', '4. close': '237.9300', '5. volume': '102629283'}, '2024-01-03': {'1. open': '244.9800', '2. high': '245.6800', '3. low': '236.3200', '4. close': '238.4500', '5. volume': '121082599'}, '2024-01-02': {'1. open': '250.0800', '2. high': '251.2500', '3. low': '244.4100', '4. close': '248.4200', '5. volume': '104654163'}, '2023-12-29': {'1. open': '255.1000', '2. high': '255.1900', '3. low': '247.4300', '4. close': '248.4800', '5. volume': '100891578'}, '2023-12-28': {'1. open': '263.6600', '2. high': '265.1300', '3. low': '252.7100', '4. close': '253.1800', '5. volume': '113619943'}, '2023-12-27': {'1. open': '258.3500', '2. high': '263.3400', '3. low': '257.5200', '4. close': '261.4400', '5. volume': '105853348'}, '2023-12-26': {'1. open': '254.4900', '2. high': '257.9700', '3. low': '252.9100', '4. close': '256.6100', '5. volume': '86892382'}, '2023-12-22': {'1. open': '256.7600', '2. high': '258.2200', '3. low': '251.3700', '4. close': '252.5400', '5. volume': '93370094'}, '2023-12-21': {'1. open': '251.9000', '2. high': '254.7999', '3. low': '248.5500', '4. close': '254.5000', '5. volume': '109594227'}, '2023-12-20': {'1. open': '256.4100', '2. high': '259.8400', '3. low': '247.0000', '4. close': '247.1400', '5. volume': '125096987'}, '2023-12-19': {'1. open': '253.4800', '2. high': '258.3399', '3. low': '253.0100', '4. close': '257.2200', '5. volume': '106287276'}, '2023-12-18': {'1. open': '253.7800', '2. high': '258.7400', '3. low': '251.3600', '4. close': '252.0800', '5. volume': '116416490'}, '2023-12-15': {'1. open': '251.2100', '2. high': '254.1300', '3. low': '248.3000', '4. close': '253.5000', '5. volume': '135932762'}, '2023-12-14': {'1. open': '241.2200', '2. high': '253.8800', '3. low': '240.7900', '4. close': '251.0500', '5. volume': '160829239'}, '2023-12-13': {'1. open': '234.1900', '2. high': '240.3000', '3. low': '228.2000', '4. close': '239.2900', '5. volume': '146286348'}, '2023-12-12': {'1. open': '238.5500', '2. high': '238.9900', '3. low': '233.8700', '4. close': '237.0100', '5. volume': '95328313'}, '2023-12-11': {'1. open': '242.7400', '2. high': '243.4410', '3. low': '237.4500', '4. close': '239.7400', '5. volume': '97913888'}, '2023-12-08': {'1. open': '240.2700', '2. high': '245.2700', '3. low': '239.2701', '4. close': '243.8400', '5. volume': '103126829'}, '2023-12-07': {'1. open': '241.5500', '2. high': '244.0800', '3. low': '236.9800', '4. close': '242.6400', '5. volume': '107142262'}, '2023-12-06': {'1. open': '242.9200', '2. high': '246.5700', '3. low': '239.1709', '4. close': '239.3700', '5. volume': '125905295'}, '2023-12-05': {'1. open': '233.8700', '2. high': '246.6600', '3. low': '233.7000', '4. close': '238.7200', '5. volume': '137971115'}, '2023-12-04': {'1. open': '235.7500', '2. high': '239.3733', '3. low': '233.2902', '4. close': '235.5800', '5. volume': '104099817'}, '2023-12-01': {'1. open': '233.1400', '2. high': '240.1900', '3. low': '231.9000', '4. close': '238.8300', '5. volume': '121331709'}, '2023-11-30': {'1. open': '245.1400', '2. high': '245.2200', '3. low': '236.9100', '4. close': '240.0800', '5. volume': '132353196'}, '2023-11-29': {'1. open': '249.2100', '2. high': '252.7500', '3. low': '242.7600', '4. close': '244.1400', '5. volume': '135401335'}, '2023-11-28': {'1. open': '236.6800', '2. high': '247.0000', '3. low': '234.0100', '4. close': '246.7200', '5. volume': '148549913'}, '2023-11-27': {'1. open': '236.8900', '2. high': '238.3300', '3. low': '232.1000', '4. close': '236.0800', '5. volume': '112031763'}, '2023-11-24': {'1. open': '233.7500', '2. high': '238.7500', '3. low': '232.3300', '4. close': '235.4500', '5. volume': '65125203'}, '2023-11-22': {'1. open': '242.0400', '2. high': '244.0100', '3. low': '231.4000', '4. close': '234.2100', '5. volume': '118117078'}, '2023-11-21': {'1. open': '235.0400', '2. high': '243.6200', '3. low': '233.3400', '4. close': '241.2000', '5. volume': '122288000'}, '2023-11-20': {'1. open': '234.0400', '2. high': '237.1000', '3. low': '231.0200', '4. close': '235.6000', '5. volume': '116562402'}, '2023-11-17': {'1. open': '232.0000', '2. high': '237.3900', '3. low': '226.5400', '4. close': '234.3000', '5. volume': '142766234'}, '2023-11-16': {'1. open': '239.4900', '2. high': '240.8800', '3. low': '230.9600', '4. close': '233.5900', '5. volume': '136816819'}, '2023-11-15': {'1. open': '239.2900', '2. high': '246.7000', '3. low': '236.4500', '4. close': '242.8400', '5. volume': '150353975'}, '2023-11-14': {'1. open': '235.0300', '2. high': '238.1350', '3. low': '230.7200', '4. close': '237.4100', '5. volume': '149771642'}, '2023-11-13': {'1. open': '215.6000', '2. high': '225.4000', '3. low': '211.6101', '4. close': '223.7100', '5. volume': '140447569'}, '2023-11-10': {'1. open': '210.0300', '2. high': '215.3800', '3. low': '205.6900', '4. close': '214.6500', '5. volume': '131310128'}, '2023-11-09': {'1. open': '219.7500', '2. high': '220.8000', '3. low': '206.6800', '4. close': '209.9800', '5. volume': '142110454'}, '2023-11-08': {'1. open': '223.1500', '2. high': '224.1500', '3. low': '217.6400', '4. close': '222.1100', '5. volume': '106584841'}, '2023-11-07': {'1. open': '219.9800', '2. high': '223.1200', '3. low': '215.7200', '4. close': '222.1800', '5. volume': '116900130'}, '2023-11-06': {'1. open': '223.9800', '2. high': '226.3200', '3. low': '215.0000', '4. close': '219.2700', '5. volume': '117335820'}, '2023-11-03': {'1. open': '221.1500', '2. high': '226.3701', '3. low': '218.4000', '4. close': '219.9600', '5. volume': '119534790'}, '2023-11-02': {'1. open': '212.9700', '2. high': '219.2000', '3. low': '211.4500', '4. close': '218.5100', '5. volume': '125987621'}, '2023-11-01': {'1. open': '204.0400', '2. high': '205.9900', '3. low': '197.8500', '4. close': '205.6600', '5. volume': '121661656'}, '2023-10-31': {'1. open': '196.1200', '2. high': '202.8000', '3. low': '194.0700', '4. close': '200.8400', '5. volume': '118068273'}, '2023-10-30': {'1. open': '209.2800', '2. high': '210.8800', '3. low': '194.6700', '4. close': '197.3600', '5. volume': '136448167'}, '2023-10-27': {'1. open': '210.6000', '2. high': '212.4100', '3. low': '205.7700', '4. close': '207.3000', '5. volume': '94881173'}, '2023-10-26': {'1. open': '211.3200', '2. high': '214.8000', '3. low': '204.8800', '4. close': '205.7600', '5. volume': '115112635'}, '2023-10-25': {'1. open': '215.8800', '2. high': '220.1000', '3. low': '212.2000', '4. close': '212.4200', '5. volume': '107065087'}, '2023-10-24': {'1. open': '216.5000', '2. high': '222.0500', '3. low': '214.1100', '4. close': '216.5200', '5. volume': '118231113'}, '2023-10-23': {'1. open': '210.0000', '2. high': '216.9800', '3. low': '202.5100', '4. close': '212.0800', '5. volume': '150683368'}, '2023-10-20': {'1. open': '217.0100', '2. high': '218.8606', '3. low': '210.4200', '4. close': '211.9900', '5. volume': '138010095'}, '2023-10-19': {'1. open': '225.9500', '2. high': '230.6100', '3. low': '216.7800', '4. close': '220.1100', '5. volume': '170772713'}, '2023-10-18': {'1. open': '252.7000', '2. high': '254.6300', '3. low': '242.0800', '4. close': '242.6800', '5. volume': '125147846'}, '2023-10-17': {'1. open': '250.1000', '2. high': '257.1830', '3. low': '247.0800', '4. close': '254.8500', '5. volume': '93562909'}, '2023-10-16': {'1. open': '250.0500', '2. high': '255.3999', '3. low': '248.4800', '4. close': '253.9200', '5. volume': '88917176'}, '2023-10-13': {'1. open': '258.9000', '2. high': '259.6000', '3. low': '250.2200', '4. close': '251.1200', '5. volume': '102296786'}, '2023-10-12': {'1. open': '262.9200', '2. high': '265.4100', '3. low': '256.6307', '4. close': '258.8700', '5. volume': '111508114'}, '2023-10-11': {'1. open': '266.2000', '2. high': '268.6000', '3. low': '260.9000', '4. close': '262.9900', '5. volume': '103706266'}, '2023-10-10': {'1. open': '257.7500', '2. high': '268.9400', '3. low': '257.6500', '4. close': '263.6200', '5. volume': '122656030'}, '2023-10-09': {'1. open': '255.3100', '2. high': '261.3600', '3. low': '252.0500', '4. close': '259.6700', '5. volume': '101377947'}, '2023-10-06': {'1. open': '253.9800', '2. high': '261.6500', '3. low': '250.6500', '4. close': '260.5300', '5. volume': '118121812'}, '2023-10-05': {'1. open': '260.0000', '2. high': '263.6000', '3. low': '256.2500', '4. close': '260.0500', '5. volume': '119159214'}, '2023-10-04': {'1. open': '248.1400', '2. high': '261.8600', '3. low': '247.6000', '4. close': '261.1600', '5. volume': '129721567'}, '2023-10-03': {'1. open': '248.6100', '2. high': '250.0200', '3. low': '244.4500', '4. close': '246.5300', '5. volume': '101985305'}, '2023-10-02': {'1. open': '244.8100', '2. high': '254.2799', '3. low': '242.6200', '4. close': '251.6000', '5. volume': '123810402'}, '2023-09-29': {'1. open': '250.0000', '2. high': '254.7700', '3. low': '246.3500', '4. close': '250.2200', '5. volume': '128522729'}, '2023-09-28': {'1. open': '240.0200', '2. high': '247.5500', '3. low': '238.6500', '4. close': '246.3800', '5. volume': '117058870'}, '2023-09-27': {'1. open': '244.2620', '2. high': '245.3300', '3. low': '234.5800', '4. close': '240.5000', '5. volume': '136597184'}, '2023-09-26': {'1. open': '242.9800', '2. high': '249.5500', '3. low': '241.6601', '4. close': '244.1200', '5. volume': '101993631'}, '2023-09-25': {'1. open': '243.3800', '2. high': '247.1000', '3. low': '238.3100', '4. close': '246.9900', '5. volume': '104636557'}, '2023-09-22': {'1. open': '257.4000', '2. high': '257.7888', '3. low': '244.4800', '4. close': '244.8800', '5. volume': '127524083'}, '2023-09-21': {'1. open': '257.8500', '2. high': '260.8600', '3. low': '254.2100', '4. close': '255.7000', '5. volume': '119951516'}, '2023-09-20': {'1. open': '267.0400', '2. high': '273.9300', '3. low': '262.4606', '4. close': '262.5900', '5. volume': '122514643'}, '2023-09-19': {'1. open': '264.3500', '2. high': '267.8500', '3. low': '261.2000', '4. close': '266.5000', '5. volume': '103704040'}, '2023-09-18': {'1. open': '271.1600', '2. high': '271.4400', '3. low': '263.7601', '4. close': '265.2800', '5. volume': '101543305'}, '2023-09-15': {'1. open': '277.5500', '2. high': '278.9800', '3. low': '271.0000', '4. close': '274.3900', '5. volume': '133692313'}, '2023-09-14': {'1. open': '271.3200', '2. high': '276.7094', '3. low': '270.4200', '4. close': '276.0400', '5. volume': '107709842'}, '2023-09-13': {'1. open': '270.0700', '2. high': '274.9800', '3. low': '268.1000', '4. close': '271.3000', '5. volume': '111673737'}, '2023-09-12': {'1. open': '270.7600', '2. high': '278.3900', '3. low': '266.6000', '4. close': '267.4800', '5. volume': '135999866'}, '2023-09-11': {'1. open': '264.2700', '2. high': '274.8500', '3. low': '260.6100', '4. close': '273.5800', '5. volume': '174667852'}, '2023-09-08': {'1. open': '251.2200', '2. high': '256.5200', '3. low': '246.6700', '4. close': '248.5000', '5. volume': '118559635'}, '2023-09-07': {'1. open': '245.0700', '2. high': '252.8100', '3. low': '243.2650', '4. close': '251.4900', '5. volume': '115312886'}, '2023-09-06': {'1. open': '255.1350', '2. high': '255.3900', '3. low': '245.0600', '4. close': '251.9200', '5. volume': '116959759'}, '2023-09-05': {'1. open': '245.0000', '2. high': '258.0000', '3. low': '244.8600', '4. close': '256.4900', '5. volume': '129469565'}, '2023-09-01': {'1. open': '257.2600', '2. high': '259.0794', '3. low': '242.0100', '4. close': '245.0100', '5. volume': '132541640'}, '2023-08-31': {'1. open': '255.9800', '2. high': '261.1800', '3. low': '255.0500', '4. close': '258.0800', '5. volume': '108861698'}, '2023-08-30': {'1. open': '254.2000', '2. high': '260.5100', '3. low': '250.5900', '4. close': '256.9000', '5. volume': '121988437'}, '2023-08-29': {'1. open': '238.5800', '2. high': '257.4800', '3. low': '237.7700', '4. close': '257.1800', '5. volume': '134047603'}}}

today_date = dt.today()

# Get yesterday and previous day of yesterday dates in format %Y-%m-%d
yesterday_date = get_previous_day_date(today_date)
prv_yesterday_date = get_previous_day_date(dt.strptime(yesterday_date, "%Y-%m-%d"))

# Get closing prices for target dates
yesterday_closing_price = get_close_price(yesterday_date)
prv_yesterday_closing_price = get_close_price(prv_yesterday_date)

# Get the percentage of increase or decrease difference between those two dates
difference_closing_prices = round(float(yesterday_closing_price - prv_yesterday_closing_price), 2)
percentage_closing_prices = difference_closing_prices / yesterday_closing_price * 100

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
if abs(percentage_closing_prices) >= 5:
    news_api_key = os.environ.get("NEWS_API_KEY")
    news_api_parameters = {
        "q": f"{STOCK}",
        "searchIn": "title,description",
        "from": prv_yesterday_date,
        "to": yesterday_date,
        "pageSize": 3,
        "apiKey": news_api_key
    }
    news_api_response = requests.get(url="https://newsapi.org/v2/everything", params=news_api_parameters)
    news_api_response.raise_for_status()
    news_api_data = news_api_response.json()

    # Output json data for tests
    # news_api_data = {'status': 'ok', 'totalResults': 21, 'articles': [{'source': {'id': 'next-big-future', 'name': 'Next Big Future'}, 'author': 'Brian Wang', 'title': 'Lower Iron LFP Battery Prices Will Help Tesla Margins $TSLA', 'description': 'CATL has new rectangular LFP batteries which will be available in 6 months. The Iron LFP EV battery price will be less than $56 per kWh within six months. It is a bigger rectangular battery with each one being like six Tesla 4680 batteries. Tesla also buys Ir…', 'url': 'https://www.nextbigfuture.com/2024/01/lower-iron-lfp-battery-prices-will-help-tesla-margins-tsla.html', 'urlToImage': 'https://nextbigfuture.s3.amazonaws.com/uploads/2024/01/Screen-Shot-2024-01-19-at-9.02.30-PM.jpg', 'publishedAt': '2024-01-20T05:08:09Z', 'content': 'Brian Wang is a Futurist Thought Leader and a popular Science blogger with 1 million readers per month. His blog Nextbigfuture.com is ranked #1 Science News Blog. It covers many disruptive technology… [+593 chars]'}, {'source': {'id': None, 'name': 'Finbold.com'}, 'author': 'Elmaz Sabovic', 'title': 'Tesla (TSLA) stock analysis: Buy, Sell, or Hold in 2024?', 'description': 'After gains of over 60% in the previous year, Tesla (NASDAQ: TSLA) has had a rocky start to 2024. The … Continue reading\nThe post Tesla (TSLA) stock analysis: Buy, Sell, or Hold in 2024? appeared first on Finbold.', 'url': 'https://finbold.com/tesla-tsla-stock-analysis-buy-sell-or-hold-in-2024/', 'urlToImage': 'https://assets.finbold.com/uploads/2024/01/Tesla-TSLA-stock-analysis-Buy-Sell-or-Hold-in-2024.jpg', 'publishedAt': '2024-01-19T09:25:15Z', 'content': 'After gains of over 60% in the previous year, Tesla (NASDAQ: TSLA) has had a rocky start to 2024. The focus has shifted to the long-awaited Q4 earnings report that should be released on January 24.\r\n… [+2994 chars]'}, {'source': {'id': None, 'name': 'Biztoc.com'}, 'author': 'investors.com', 'title': 'Tesla Stock Bull Cuts Price Target As Global EV Momentum Stalls', 'description': 'stock slumping to begin 2024, as the EV giant continues to cut vehicle prices and put pressure on margins, a bull decided to slash his TSLA stock price target Monday. Morgan Stanley analyst Adam Jonas on Monday cut his TSLA price target to 345, down from 380,…', 'url': 'https://biztoc.com/x/91c8277bab6c6822', 'urlToImage': 'https://c.biztoc.com/p/91c8277bab6c6822/s.webp', 'publishedAt': '2024-01-22T13:58:10Z', 'content': 'stock slumping to begin 2024, as the EV giant continues to cut vehicle prices and put pressure on margins, a bull decided to slash his TSLA stock price target Monday.Morgan Stanley analyst Adam Jonas… [+272 chars]'}]}

    articles_list = []
    articles_list = [{"Headline": dict_data["title"], "Brief": dict_data["description"]}
                     for dict_data in news_api_data["articles"]]

    ## STEP 3: Use https://www.twilio.com
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
        msg_body = (f"{STOCK}: {rise_or_fall_sign}{abs(round(percentage_closing_prices, 2))}%\n"
                    f"Headline: {article["Headline"]}.\n"
                    f"Brief: {article["Brief"]}")
        message = client.messages.create(body=msg_body, from_=TWILIO_phone_number, to=your_phone_number)

        print(message.status)

#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

