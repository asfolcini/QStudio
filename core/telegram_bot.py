import requests

class Telegram_Message():
    """
        sfl_Maia_Bot
        Using MAIA BOT for sending out messages on telegram group.
    """

    TOKEN   = "6048507085:AAHPWlXXCmasC0r1oLo2OnsnAgyxNleeqpI"
    #CHAT_ID = "-358156383" # STGA Chat Group
    CHAT_ID = "-1001910945256" # Signal CHANNEL


    def __init__(self, token=None, chat_id=None):
        if token != None:
            self.TOKEN = token
        if chat_id != None:
            self.CHAT_ID = chat_id


    def send_message(self, text):
        url = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.CHAT_ID}&text={text}"
        try:
            print(requests.get(url).json())
        except:
            print("[WARNING TelegramBot]: sfl_MAIA_bot cannot send message!")
