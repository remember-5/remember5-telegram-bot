import requests


def set_bot_commands(bot_token: str, commands: list):
    """
    设置 Bot 的快捷命令。
    """
    url = f"https://api.telegram.org/bot{bot_token}/setMyCommands"
    payload = {
        "commands": commands
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Bot commands set successfully!")
    else:
        print(f"Failed to set bot commands: {response.text}")
