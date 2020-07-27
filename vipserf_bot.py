from time import sleep
from csv import DictReader

from telethon.sync import TelegramClient

from custom_logging import get_process_logger
from balance import get_balance


REWARD_MESSAGE = 'Для начисления нажмите на кнопку:'
REWARD_ALREADY_TAKEN_MESSAGE = 'Вы уже просматривали этот пост!'
REWARD_NOT_AVAILABLE = 'Задание недоступно!'

process_logger = get_process_logger()
process_logger.info('script started')

try:
    with open('./info/accounts_data.csv', newline='') as csvfile:
        data_reader = DictReader(csvfile, fieldnames=['id', 'phone_number', 'api_id', 'api_hash'])

        while True:

            for data_row in data_reader:
                data_row_id, phone_number, api_id, api_hash = data_row.values()
                session = f"sessions/anon_{data_row_id}"

                client = TelegramClient(session, api_id, api_hash)
                client.connect()

                process_logger.info(f'account_{data_row_id},connected')

                dialogList = client.get_dialogs()
                for dialog in dialogList:
                    if dialog.title == 'Vipserfkanal':
                        tegmo = dialog

                message_list = client.iter_messages(tegmo)
                for message in message_list:
                    if message.message == REWARD_MESSAGE:
                        answer = message.click()

                        if answer.message[:31] == REWARD_ALREADY_TAKEN_MESSAGE or answer.message == REWARD_NOT_AVAILABLE:
                            process_logger.info(
                                f'account_{data_row_id},watch_post,false,message_id:{message.id},message_date:{message.date}')

                        else:
                            process_logger.info(
                                f'account_{data_row_id},watch_post,true,message_id:{message.id},message_date:{message.date}')

                    sleep(1)

                process_logger.info(f'account_{data_row_id},disconnect')

                current_balance = get_balance(client)
                process_logger.info(f'account_{data_row_id},balance:{current_balance}₽')

            sleep(30 * 60)


except KeyboardInterrupt:
    process_logger.info('script finished by keyborad interruption')

else:
    process_logger.info('script finished successfully')
