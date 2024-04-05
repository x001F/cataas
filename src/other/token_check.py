import yaml


def token() -> None:
    with open('src/config/config.yaml', 'r') as f:
        data: dict = yaml.load(f, yaml.FullLoader)
    if data.get('BOT_TOKEN'):
        pass
    else:
        print("Bot can't run without token, get if from @BotFather.")
        bot_token = input('Enter token given by @BotFather: ')
        data['BOT_TOKEN'] = bot_token
        with open('src/config/config.yaml', 'w') as f:
            yaml.dump(data, f)
