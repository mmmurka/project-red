import requests

def get_all_coin_prices_to_tether():
    url = 'https://api.huobi.pro/market/tickers'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        coin_prices = {}
        for ticker in data['data']:
            symbol = ticker['symbol']
            if symbol.endswith(' usdt'):
                price = ticker['close']
                coin_prices[symbol] = price

        return coin_prices
    else:
        print(f'Ошибка при получении данных. Код ошибки: {response.status_code}')
        return None

# Пример использования функции
all_prices = get_all_coin_prices_to_tether()
if all_prices:
    for symbol, price in all_prices.items():
        print(f'Текущий курс {symbol}: {price}')
