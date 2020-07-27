from csv import DictReader

from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest


with open('./info/accounts_data.csv', newline='') as csvfile:
    data_reader = DictReader(csvfile, fieldnames=['id', 'phone_number', 'api_id', 'api_hash'])

    for data_row in data_reader:
        data_row_id, phone_number, api_id, api_hash = data_row.values()
        session = f"sessions/anon_{data_row_id}"

        client = TelegramClient(session, api_id, api_hash)
        client.connect()

        # follow Vipserfbot
        vipserf_chat = client.get_input_entity('t.me/Vipserfbot')
        client.send_message(vipserf_chat, '/start')

        # follow Vipserfkanal
        newvipserf_channel = client.get_input_entity('t.me/NewVipserf')
        client(JoinChannelRequest(newvipserf_channel))

        # follow NewVipserf
        vipserfkanal_channel = client.get_input_entity('t.me/vipserf24')
        client(JoinChannelRequest(vipserfkanal_channel))

        # choose languege in Vipserfbot
        dialog_list = client.get_dialogs()
        for dialog in dialog_list:
            if dialog.title == 'Vipserf':
                tegmo = dialog

        choose_language_message = client.get_messages(tegmo, limit=1)
        choose_language_message[0].click()
