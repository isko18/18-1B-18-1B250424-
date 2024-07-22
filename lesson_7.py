import schedule
import time 
import requests

def test():
    print("Hello Geeks")
    print(time.ctime())

def get_btc_price():
    print("======BTC======")
    url = 'https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    response = requests.get(url=url).json()
    # print(response)
    price = response.get('price')
    
    """" Стоимость биткоина на текущее время: {}, цена: {} """
    print(f'Стоимость биткоина на текущее время: {time.ctime()}, цена: {price}')
    
# schedule.every(5).seconds.do(test)
# schedule.every(1).minutes.do(test)
# schedule.every().day.at("15:32").do(test)
# schedule.every().monday.at("15:34").do(test)
# schedule.every().day.at("15:36", 'Europe/Amsterdam').do(test)
# schedule.every(2).hour.at(":37").do(test)
schedule.every(1).seconds.do(get_btc_price)



while True:
    schedule.run_pending()