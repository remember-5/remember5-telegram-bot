commands_keys = {
    "start": {
        "command": "start",
        "description": "Start the bot"
    },
    "settings": {
        "command": "settings",
        "description": "Change settings"
    },
    "help": {
        "command": "help",
        "description": "Get help"
    },
    "reply_keyboard": {
        "command": "reply_keyboard",
        "description": "Send reply keyboard"
    }
}

# 直接生成 commands 列表
commands = [{"command": v["command"], "description": v["description"]} for v in commands_keys.values()]
