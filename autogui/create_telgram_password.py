from time import sleep
import pyautogui


pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

PASSWORD = 'baget'

burger_position = pyautogui.locateOnScreen("imgs_to_find/telegram_app/burger_img.png")
burger_position = back_arrow_btn_position = pyautogui.center(burger_position)  # (72, 177)
x_position = burger_position[0]

first_account_position = starting_drag_position = (x_position, burger_position[1] + 136)
settings_btn_position = (x_position, first_account_position[1] + 252)
privacy_btn_position = (x_position, settings_btn_position[1] + 155)
verification_btn_position = (x_position, privacy_btn_position[1] - 310)
additional_pswd_btn_position = (x_position, verification_btn_position[1] + 165)


def scroll(to):
    pyautogui.moveTo(*starting_drag_position)
    if to == "top":
        pyautogui.dragTo(starting_drag_position[0], starting_drag_position[1] + 437, button='left')
    elif to == "bottom":
        pyautogui.dragTo(starting_drag_position[0], starting_drag_position[1] - 200, button='left')
    elif to == 'left':
        pyautogui.dragTo(starting_drag_position[0] - 30, starting_drag_position[1], button='left')


# expecting not-first account active
for i in range(10):
    pyautogui.click(*burger_position)
    scroll(to='top')
    pyautogui.click(first_account_position[0], first_account_position[1] + (47 * i))
    pyautogui.click(*burger_position)
    scroll(to='bottom')
    pyautogui.click(*settings_btn_position)
    pyautogui.click(*privacy_btn_position)
    pyautogui.click(*verification_btn_position)
    pyautogui.click(*additional_pswd_btn_position)
    pyautogui.typewrite(f'{PASSWORD}', interval=0.05)  # newline is Enter
    pyautogui.typewrite(['enter', 'enter', 'right', 'enter'], interval=0.3)
    sleep(1)

    for j in range(3):
        pyautogui.click(*back_arrow_btn_position)
