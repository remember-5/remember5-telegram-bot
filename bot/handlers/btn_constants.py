# 定义回调前缀
CALLBACK_PREFIX_CONFIG = "setting_"

folder_btn = {
    "create_folder": {
        "text": "➕创建文件夹",
        "callback_data": f"{CALLBACK_PREFIX_CONFIG}create_folder"
    },
    "delete_folder": {
        "text": "➖删除文件夹",
        "callback_data": f"{CALLBACK_PREFIX_CONFIG}delete_folder"
    },
    "show_folder": {
        "text": "📂查看文件夹",
        "callback_data": f"{CALLBACK_PREFIX_CONFIG}show_folder"
    },
}
config_btn = {
    "get_default_path": {
        "text": "查看当前路径",
        "callback_data": f"{CALLBACK_PREFIX_CONFIG}get_default_path"
    },
    "set_default_path": {
        "text": "使用默认路径",
        "callback_data": f"{CALLBACK_PREFIX_CONFIG}set_default_path"
    },
    "input_custom_path": {
        "text": "输入自定义路径",
        "callback_data": f"{CALLBACK_PREFIX_CONFIG}input_custom_path"
    }
}
