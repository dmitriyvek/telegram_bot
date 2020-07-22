from time import sleep
from subprocess import run
from csv import DictReader

import pyautogui
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import SessionPasswordNeededError


PASSWORD = 'baget'
pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True


# telegram mobile app coordinates
burger_position = pyautogui.locateOnScreen("autogui/imgs_to_find/telegram_app/burger_img.png")
burger_position = pyautogui.center(burger_position)  # (72, 177)
x_position, y_position = burger_position[0], burger_position[1]

first_account_position = (x_position, y_position + 136)
telegram_dialog_position = (x_position, y_position + 63)
message_with_code_position = (x_position, y_position + 413)
copy_btn_position = (x_position, y_position + 493)


def get_login_code_from_app(account_number):
    '''Get TelethonClient login code from telegram app for given account number'''
    account_number = (account_number - 1) % 10

    # select account
    pyautogui.click(burger_position)
    pyautogui.click(first_account_position[0], first_account_position[1] + (47 * account_number))
    # copy message text
    pyautogui.click(telegram_dialog_position)
    pyautogui.click(message_with_code_position)
    pyautogui.click(copy_btn_position)
    # return to chat list
    pyautogui.click(burger_position)

    # get message from clipboard and parse it to get login code
    message_text = run("xclip -selection clipboard -out", capture_output=True, shell=True).stdout.decode('utf-8')
    login_code = message_text[12:17]

    return login_code


with open('./autogui/accounts_data.csv', newline='') as csvfile:
    data_reader = DictReader(csvfile, fieldnames=['id', 'phone_number', 'api_id', 'api_hash'])

    for data_row in data_reader:
        data_row_id, phone_number, api_id, api_hash = data_row.values()
        session = f"sessions/anon_{data_row_id}"

        client = TelegramClient(session, api_id, api_hash)
        client.connect()

        if not client.is_user_authorized():
            client.send_code_request(phone=phone_number)
            login_code = get_login_code_from_app(int(data_row_id))

            try:
                client.sign_in(phone=phone_number, code=login_code)
            except SessionPasswordNeededError:
                client.sign_in(password=PASSWORD)
