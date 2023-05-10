import telegram
import requests
import time

# Здесь нужно вставить токен вашего бота, полученный через @BotFather
bot = telegram.Bot(token='YOUR_BOT_TOKEN')

# Здесь нужно вставить свои API-ключи для Ethereum, Binance Smart Chain (BSC) и Arbitrum (ARB)
eth_api_key = 'YOUR_ETH_API_KEY'
bsc_api_key = 'YOUR_BSC_API_KEY'
arb_api_key = 'YOUR_ARB_API_KEY'

# Список адресов кошельков, которые нужно отслеживать
wallet_addresses = []

# Отправляем запрос к API блокчейна для получения списка последних транзакций
def get_transactions(api_key, address):
    api_url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()['result']
    else:
        print('Error: Could not retrieve transactions')
        return []

# Функция для отправки уведомления в чат Telegram
def send_notification(message):
    bot.send_message(chat_id='YOUR_CHAT_ID', text=message)

# Функция для проверки новых транзакций на блокчейне и отправки уведомлений в чат
def check_transactions():
    for address in wallet_addresses:
        transactions = get_transactions(eth_api_key, address) + get_transactions(bsc_api_key, address) + get_transactions(arb_api_key, address)
        for transaction in transactions:
            if transaction['to'].lower() == address.lower():
                message = f'Новая транзакция обнаружена!\n\n' \
                          f'Сумма: {transaction["value"]}\n' \
                          f'Отправитель: {transaction["from"]}\n' \
                          f'Получатель: {transaction["to"]}\n' \
                          f'Хэш транзакции: {transaction["hash"]}\n'
                send_notification(message)

# Функция для добавления нового адреса кошелька в список отслеживаемых
def add_address(address):
    if address not in wallet_addresses:
        wallet_addresses.append(address)
        print(f'{address} has been added to the watchlist')
    else:
        print(f'{address} is already in the watchlist')

# Функция для удаления адреса кошелька из списка отслеживаемых
def remove_address(address):
    if address in wallet_addresses:
        wallet_addresses.remove(address)
        print(f'{address} has been removed from the watchlist')
    else:
        print(f'{address} is not in the watchlist')

# Основной цикл программы
