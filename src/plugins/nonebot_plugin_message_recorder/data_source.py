import nonebot
import time

export = nonebot.require("nonebot_plugin_database_connector")
mysql = export.mysql_pool


async def insert_new_row(qq_id: int, bot_id: int, group: int, text_message: str, name: str,
                         permission: str):
    query = 'INSERT INTO qqmessagebackup (bot_id, qq, `group`, text_message, time, name, permission) ' \
            'VALUES (:bot_id, :qq, :group, :text_message, :time, :name, :permission)'
    data = {
        'bot_id': bot_id,
        'qq': qq_id,
        'group': group,
        'text_message': text_message,
        'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
        'name': name,
        'permission': permission.upper()
    }
    await mysql.execute(query, values=data)
