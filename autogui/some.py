from time import sleep
from subprocess import run

import pyautogui
import pytesseract
import PIL.ImageOps


OUTPUT_FILE_NAME = 'accounts_data.csv'
APP_TITLE = APP_SHORT_NAME = 'testProject'

NUMBER_LIST = '+0123456789'
pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True


def parse_phone_number(phone_number):
    parsed_number = ''
    for number in phone_number:
        if number in NUMBER_LIST:
            parsed_number += number
    return parsed_number


def press_tabs_with_enter(times=1, enter=True):
    pyautogui.PAUSE = 0.2
    for i in range(times):
        pyautogui.press('tab')

    if enter:
        pyautogui.press('enter')

    pyautogui.PAUSE = 1
    sleep(1)


# telegram mobile app coordinates
burger_position = pyautogui.locateOnScreen("imgs_to_find/telegram_app/burger_img.png")
burger_position = pyautogui.center(burger_position)  # (72, 177)
x_position, y_position = burger_position[0], burger_position[1]

first_account_position = (x_position, y_position + 136)
zoom_btn_position = (x_position + 412, y_position + 167)
phone_number_zoom_position = (x_position + 35, y_position + 89)
phone_number_region = (x_position - 35, y_position + 45, 160, 27)  # x_position - 33
escape_account_list_position = (phone_number_region[0] + 290, phone_number_region[1])
code_zoom_position = (x_position + 31, y_position + 341)
telegram_dialog_position = (x_position, y_position + 63)
code_region = (x_position - 39, y_position + 289, 271, 37)


# telegram.org site coordinates
telegram_core_img_position = pyautogui.locateOnScreen("imgs_to_find/telegram_org/telegram_core_img.png")
telegram_core_img_position = pyautogui.center(telegram_core_img_position)  # (279, 301)

api_id_input_position = (telegram_core_img_position[0] - 151, telegram_core_img_position[1] - 17)  # (128, 284)
api_hash_input_position = (telegram_core_img_position[0] - 151, telegram_core_img_position[1] + 84)  # (128, 385)


# open csv file
csv_file = open(OUTPUT_FILE_NAME, 'ta')


# expecting not-first account active
for i in range(7, 10):

    # get phone number
    pyautogui.click(*burger_position)
    pyautogui.click(first_account_position[0], first_account_position[1] + (47 * i))
    pyautogui.click(*burger_position)
    pyautogui.click(*zoom_btn_position)
    pyautogui.click(*phone_number_zoom_position)

    phone_number_img = pyautogui.screenshot(region=phone_number_region)
    phone_number_img = PIL.ImageOps.invert(phone_number_img)
    phone_number = pytesseract.image_to_string(phone_number_img)
    phone_number = parse_phone_number(phone_number)
    print(phone_number)

    # enter phone number in telegram.org
    pyautogui.click(telegram_core_img_position)
    press_tabs_with_enter(times=1, enter=False)
    pyautogui.typewrite(f'{phone_number}\n', interval=0.05)  # newline is Enter

    # come back to chat list
    pyautogui.click(*zoom_btn_position)
    pyautogui.click(*escape_account_list_position)

    # get login code for telegram.org
    pyautogui.click(*telegram_dialog_position)
    pyautogui.click(*zoom_btn_position)
    pyautogui.click(*code_zoom_position)
    pyautogui.click(*code_zoom_position)

    code_img = pyautogui.screenshot(region=code_region)
    code_img = PIL.ImageOps.invert(code_img)
    code = pytesseract.image_to_string(code_img, lang='eng')[:11]
    print(code)

    # enter code to telegram.org
    pyautogui.click(telegram_core_img_position)
    press_tabs_with_enter(times=2, enter=False)
    pyautogui.typewrite(f'{code}\n', interval=0.05)

    # if code not right
    while pyautogui.locateOnScreen("imgs_to_find/telegram_org/invalid_code_alert.png"):
        press_tabs_with_enter(10)
        press_tabs_with_enter(times=6, enter=False)
        pyautogui.typewrite(f'{phone_number}\n', interval=0.05)  # newline is Enter

        sleep(1)

        code_img = pyautogui.screenshot(region=code_region)
        code_img = PIL.ImageOps.invert(code_img)
        code = pytesseract.image_to_string(code_img, lang='eng')[:11]
        print(code)

        pyautogui.click(telegram_core_img_position)
        press_tabs_with_enter(times=2, enter=False)
        pyautogui.typewrite(f'{code}\n', interval=0.05)

        sleep(1)

    # come back to chat list
    pyautogui.click(*zoom_btn_position)
    pyautogui.click(*burger_position)

    # go to site
    pyautogui.click(telegram_core_img_position)

    # create new application
    press_tabs_with_enter(times=1)
    press_tabs_with_enter(times=6)  # there no enter
    pyautogui.typewrite(f'{APP_TITLE}', interval=0.05)
    press_tabs_with_enter(times=1, enter=False)
    pyautogui.typewrite(f'{APP_SHORT_NAME}', interval=0.05)
    press_tabs_with_enter(times=4)
    sleep(1)

    # get api_id
    pyautogui.click(api_id_input_position, clicks=2)
    api_id = run("xclip -out", capture_output=True, shell=True).stdout.decode('utf-8')

    # get api_hash
    pyautogui.click(api_hash_input_position, clicks=2)
    api_hash = run("xclip -out", capture_output=True, shell=True).stdout.decode('utf-8')

    # loging out (starts with api_hash highlighting)
    press_tabs_with_enter(times=6)
    sleep(1)
    press_tabs_with_enter(times=8)

    # write all important information about account in file
    account_data = f'{phone_number},{api_id},{api_hash}\n'
    csv_file.write(account_data)


csv_file.close()
