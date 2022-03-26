import json
import os

current_folder = os.path.dirname(__file__)  # get current folder absolute path
SHIP_PIC_PATH = os.path.join(current_folder, 'ship_info_pic')  # resource picture path
ALIAS_PATH = os.path.join(current_folder, 'alias.json')
ship_list = os.listdir(SHIP_PIC_PATH)  # Ship name list initialize
for i in range(len(ship_list)):
    ship_list[i] = ship_list[i].split('.')[0]  # Replace '.jpg' or '.png' in the filenames
with open(ALIAS_PATH, 'r') as f:
    ship_alias = json.loads(f.read())


def pic_locate(name: str) -> str:
    for ship_name in ship_list:
        if ship_name.replace(' ', '').lower() == name.replace(' ', '').lower():
            return ship_name
    return ''
