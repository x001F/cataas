from aiogram import Bot, Dispatcher
from src.storage import Storage
from src.other.token_check import token
import yaml

token()

with open('src/config/config.yaml') as f:
    bot_token = yaml.load(f, yaml.FullLoader).get('BOT_TOKEN')
    bot = Bot(token=bot_token)
    dp = Dispatcher(storage=Storage('./src/config/fsm.db'))
