from Bot.cryptoBot import *
import requests
import telegram.ext as tel
from decouple import Config, RepositoryEnv

env=Config(RepositoryEnv('.env'))

Telegram_API = env.get('TELEGRAM_API')
updater = tel.Updater(Telegram_API, use_context=True)
disp = updater.dispatcher
chat_id = env.get('CHAT_ID')
group_id = env.get('crypto_jonson')

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class TeleBot(metaclass=Singleton):

    def __init__(self):
        disp.add_handler(tel.CommandHandler("start", self.__start))
        disp.add_handler(tel.CommandHandler("help", self.__help))
        disp.add_handler(tel.CommandHandler("about", self.__about))
        # disp.add_handler(tel.CommandHandler("CoinInfo", self.__coin_info))
        #disp.add_handler(tel.CommandHandler("test", self.send_message()))


    def __start(self, update, context):
        update.message.reply_text("Hello this bot is DEMO version which will send you signals about crypto")

    def __help(self, update, context):
        update.message.reply_text("""Commands List:
        \n/start -> Welcome Message\n/about -> info about me\n/CoinInfo -> will give you the O,H,L,C and the vol of the coin you will enter\n\nFor more try to contact -> @Yoni0106""")

    def __about(self, update, context):
        update.message.reply_text("I'm Software Engineer Student who likes to do day trading in crypto")

    def send_message(self, text="TEST"):
        url = f"https://api.telegram.org/bot{Telegram_API}/sendMessage"
        params = {
            "chat_id": chat_id,
            "text": text
        }
        resp = requests.get(url, params=params)

        # Throw an exception if Telegram API fails
        resp.raise_for_status()

        return resp.json()

    def group_meesage(self, message='No message arrived'):
        url = f"https://api.telegram.org/bot{Telegram_API}/sendMessage?chat_id=@{group_id}&text={message}"
        resp = requests.get(url)

        if resp.status_code == 200:
            print("sent message")
        else:
            print("ERROR could not send the message")

    def run(self):
        print("The bot has started !")
        updater.start_polling()



telegram_bot = TeleBot()



