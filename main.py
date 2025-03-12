import requests
from twilio.rest import Client


STOCK_NAME = "NVDA"
COMPANY_NAME = "Nvidia"
up_down_symbol = None
account_sid = "place_your_acc_sid"
auth_token = "place_your_token"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_api_key = "place_your_key"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_api_key = "place_your_key"

stock_params = {
    "symbol": STOCK_NAME,
    "function" : "TIME_SERIES_DAILY",
    "apikey" : stock_api_key,
}

stock_response = requests.get(STOCK_ENDPOINT,params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()

close_prices = [float(value['4. close']) for key, value in list(stock_data['Time Series (Daily)'].items())[:2]]

percentage_difference = ((close_prices[0] - close_prices[1]) / close_prices[0]) * 100
print(percentage_difference)

if abs(percentage_difference) >= 1:
    if percentage_difference > 0:
        up_down_symbol = "🔺"
    else:
        up_down_symbol = "🔻"

    news_params = {
        "apiKey" : news_api_key,
        "q" : COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT,params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()['articles']
    articles_list = news_data[:3]

    news_titles = [(value['title'],value['description']) for value in articles_list]

    for i in range(3):

        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            from_="whatsapp:+14155238886",
            body=f"NVDA:{up_down_symbol}{round(percentage_difference)}% \nHeadline:{news_titles[i][0]}\n{news_titles[i][1]}",
            to="whatsapp:place_your_number"
    )
    print(message.status)
