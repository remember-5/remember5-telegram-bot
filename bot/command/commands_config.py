commands_keys = {
    "start": {
        "command": "start",
        "description": "Start the bot"
    },
    "config_path": {
        "command": "config_path",
        "description": "Set config path"
    },
    "help": {
        "command": "help",
        "description": "Get help"
    },
    "settings": {
        "command": "settings",
        "description": "Change settings"
    },
    "reply_keyboard": {
        "command": "reply_keyboard",
        "description": "Send reply keyboard"
    },
    "inline_keyboard": {
        "command": "inline_keyboard",
        "description": "Send inline keyboard"
    },

}

# 直接生成 commands 列表
commands = [{"command": v["command"], "description": v["description"]} for v in commands_keys.values()]
