from aiogram import Bot, Dispatcher, executor, types
import requests
import hmac
import hashlib
import sqlite3

#region Блок 1 Получение курса BTCUSDT с Бинанса
# Замените <API_KEY> и <API_SECRET> своими собственными значениями
api_key = '<API_KEY>'
api_secret = '<API_SECRET>'

# Установите валютную пару, для которой вы хотите получить курс
symbol = 'BTCUSDT'  # Например, пара BTC/USDT

# Формируем URL запроса к API Binance
url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'

# Создаем подпись для аутентификации
timestamp = requests.get('https://api.binance.com/api/v3/time').json()['serverTime']
params = f'symbol={symbol}&timestamp={timestamp}'
signature = hmac.new(api_secret.encode('utf-8'), params.encode('utf-8'), hashlib.sha256).hexdigest()

# Добавляем аутентификационные данные в заголовки запроса
headers = {'X-MBX-APIKEY': api_key}

# Отправляем GET-запрос к API Binance
response = requests.get(url, headers=headers)

# Проверяем успешность запроса и выводим результат
if response.status_code == 200:
    data = response.json()
    price = float(data['price'])
    formatted_price = f'{price:.2f}'
    print(f'Текущий курс {symbol}: {formatted_price}')
else:
    print(f'Ошибка при получении данных. Код ошибки: {response.status_code}')
#endregion

#region Блок 3 Получение курса BTCUSDT с Кракена
def get_bitcoin_price():
    pair = 'XBTUSDT'  # Символ валютної пари Bitcoin до Tether (USDT)
    url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'result' in data and pair in data['result']:
            price_data = data['result'][pair]
            last_price = price_data['c'][0]
            return float(last_price)
        else:
            print("Помилка отримання даних")
    else:
        print("Помилка HTTP-запиту:", response.status_code)


# Приклад використання:
bitcoin_price = get_bitcoin_price()
print(f"Поточний курс Bitcoin до Tether: {bitcoin_price}")
#endregion Получение курса BTCUSDT с Бинанса


#region Блок 2 Телеграм бот
TOKEN_API = '6295953219:AAH1PxkX39gbcFsKV5BszrqvlZ6za9QKSpo'

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

HELP_COMMAND = '''
/help - писька команд
/start - запуск бота'''

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text=f'Binance:   {symbol}: {formatted_price}$ \n ' 
                              f'Kraken:    {symbol}: {bitcoin_price}$')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND)



if __name__ == '__main__':
    executor.start_polling(dp)

#endregion

#region курс всего бинанса
def get_all_coin_prices():
    url = 'https://api.binance.com/api/v3/ticker/price'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        coin_prices = {item['symbol']: item['price'] for item in data if item['symbol'].endswith('USDT')}
        return coin_prices
    else:
        print(f'Ошибка при получении данных. Код ошибки: {response.status_code}')
        return None

#endregion

#region запись бинанса в бд

def create_table(): # Создание таблицы в базе данных, если она не существует
    conn = sqlite3.connect('coin_prices.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            symbol TEXT PRIMARY KEY,
            price TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Запись данных в базу данных
def insert_data(coin_prices):
    conn = sqlite3.connect('coin_prices.db')
    cursor = conn.cursor()

    for symbol, price in coin_prices.items():
        cursor.execute('INSERT OR REPLACE INTO prices (symbol, price) VALUES (?, ?)', (symbol, price))

    conn.commit()
    conn.close()


# Пример использования функций
coin_prices = get_all_coin_prices()
if coin_prices:
    create_table()
    insert_data(coin_prices)
    print('Данные успешно записаны в базу данных.')
else:
    print('Не удалось получить данные.')
#endregion

#def clear_table():
    #conn = sqlite3.connect('coin_prices.db')
   # cursor = conn.cursor()
   # cursor.execute('DELETE FROM prices')
   # conn.commit()
   # conn.close()

# Пример использования функции
#clear_table()
#print('База данных успешно очищена.')