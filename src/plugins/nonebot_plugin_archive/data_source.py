import nonebot
import os
import time


export = nonebot.require("nonebot_plugin_database_connector")
mysql = export.mysql_pool
entries: list = []
current_folder = os.path.dirname(__file__)  # get current folder absolute path
PICTURE_FOLDER = os.path.join(current_folder, 'picture_temp')
global_config = nonebot.get_driver().config


async def fetch_all_entries() -> list:
    global entries
    entries = []
    query = "SELECT creator_id, content, create_time, creator, enabled_groups, keywords, alias, fuzzy_search, is_random, is_private FROM archive WHERE is_latest = true and is_available = true"
    rows = await mysql.fetch_all(query=query)
    for row in rows:
        entries.append({
            'creator_id': row[0],
            'content': row[1],
            'create_time': row[2],
            'creator': row[3],
            'enabled_groups': row[4],
            'keywords': row[5],
            'alias': row[6],
            'fuzzy_search': row[7],
            'is_random': row[8],
            'is_private': row[9]
        })
    return entries


async def insert_new_entry(creator_id: int, content: str, keywords: str, enabled_groups: str, creator: str,
                           alias: str = None, fuzzy_search: bool = False,
                           is_private: bool = False,
                           is_available: bool = True,
                           is_random: bool = False):
    global entries
    if is_private:
        query = "UPDATE archive SET is_latest=false WHERE keywords=:keywords and enabled_groups like :enabled_groups and is_private=true and creator_id=:creator_id"
        data = {
            'keywords': keywords,
            'enabled_groups': f"%{enabled_groups}%",
            'creator_id': str(creator_id)
        }
    else:
        query = "UPDATE archive SET is_latest=false WHERE keywords=:keywords and enabled_groups like :enabled_groups"
        data = {
            'keywords': keywords,
            'enabled_groups': f"%{enabled_groups}%"
        }
    await mysql.execute(query, values=data)
    query = "INSERT INTO archive(creator_id, creator, content, keywords, alias, fuzzy_search, is_private, is_available, enabled_groups, is_random, is_latest, create_time) " \
            "VALUES (:creator_id, :creator, :content, :keywords, :alias, :fuzzy_search, :is_private, :is_available, :enabled_groups, :is_random, :is_latest, :create_time)"
    data = {
        'creator_id': creator_id,
        'creator': creator,
        'content': content,
        'keywords': keywords,
        'alias': alias,
        'fuzzy_search': fuzzy_search,
        'is_private': is_private,
        'is_available': is_available,
        'enabled_groups': enabled_groups,
        'is_random': is_random,
        'is_latest': True,
        'create_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
    }
    await mysql.execute(query, values=data)


async def remove_entry(entry: dict):
    """

    :param entry: entry
    :return:
    """
    # if not group:
    #     query = "UPDATE archive SET is_latest=false WHERE keywords=:keywords and is_latest=true"
    #     data = {
    #         'keywords': keywords
    #     }
    #     await mysql.execute(query, values=data)
    # else:
    if entry['enabled_groups'] != 'all_groups':
        query = "UPDATE archive SET is_available=false WHERE keywords=:keywords and is_latest=true and enabled_groups like :enabled_groups"
        data = {
            'keywords': entry['keywords'],
            'enabled_groups': f"%{entry['enabled_groups']}%"
        }
        await mysql.execute(query, values=data)
    else:
        query = "UPDATE archive SET is_available=false WHERE keywords=:keywords and is_latest=true"
        data = {
            'keywords': entry['keywords']
        }
        await mysql.execute(query, values=data)


"""
async def get_picture(picture_name) -> bytes:
    current_pictures = os.listdir(PICTURE_FOLDER)
    if picture_name in current_pictures:
        with open(os.path.join(PICTURE_FOLDER, picture_name), 'rb') as f:
            file = f.read()
        return file
    else:
        async with httpx.AsyncClient() as client:
            r = await client.get(global_config.Config.picture_server_url)
        with open(os.path.join(PICTURE_FOLDER, picture_name), 'wb') as f:
            f.write(r.content)
        return r.content

"""
