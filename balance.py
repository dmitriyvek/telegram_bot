from time import sleep
import re

from telethon.sync import TelegramClient


# data_row_id, phone_number, api_id, api_hash = '1', '+79912512348', '1793147', 'fd8e601e1e67066e02c743066d1df749'
# session = f"sessions/anon_{data_row_id}"

# client = TelegramClient(session, api_id, api_hash)
# client.connect()


def get_balance(client):
    dialog_list = client.get_dialogs()
    for dialog in dialog_list:
        if dialog.title == 'Vipserf':
            tegmo = dialog

    client.send_message(tegmo, '📱 Мой кабинет')
    sleep(3)

    account_status_message = client.get_messages(tegmo, limit=1)[0]
    account_status_text = account_status_message.message

    try:
        account_balance = re.search('Основной баланс: (.*)₽', account_status_text).group(1)
    except AttributeError:
        pass

    return account_balance
