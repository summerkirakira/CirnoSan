import os
import json
import time
from .config import Config

current_folder = os.path.dirname(__file__)  # get current folder absolute path
PRESENT_PATH = os.path.join(current_folder, 'present.json')  # resource picture pat
with open(PRESENT_PATH, 'r') as f:
    presents = json.loads(f.read())


def load_presents():
    global presents
    with open(PRESENT_PATH, 'r') as f:
        presents = json.loads(f.read())


def insert_presents_data(qq_id, handle):
    global presents
    requests_data = {
        "qq": qq_id,
        "id": handle,
        "requestTime": int(time.time()),
        "sponsors": {}
    }
    for i in Config.Config.sponsor_id:
        requests_data["sponsors"][str(i)] = {
            "hasSend": False,
            "sendTime": 0
        }
    with open(PRESENT_PATH, "r") as f:
        old = f.read()
        if old != "":
            old = json.loads(old)
        else:
            old = {}
    if str(qq_id) in old:
        old[str(qq_id)]["id"] = handle
    else:
        old[str(qq_id)] = requests_data
    with open(PRESENT_PATH, "w") as f:
        f.write(json.dumps(old))
    return old



def get_total_money(sponser_id):
    send_money = 0
    last_send_time = 0
    for key in presents:
        if sponser_id in presents[key]["sponsors"]:
            if presents[key]["sponsors"][sponser_id]["hasSend"]:
                send_money += 50000
            if presents[key]["sponsors"][sponser_id]["sendTime"] > last_send_time:
                last_send_time = presents[key]["sponsors"][sponser_id]["sendTime"]
    return send_money, last_send_time


def get_all_money():
    send_money = 0
    last_send_time = 0
    for key in presents:
        for sponser_id in presents[key]["sponsors"]:
            if presents[key]["sponsors"][sponser_id]["hasSend"]:
                send_money += 50000
            if presents[key]["sponsors"][sponser_id]["sendTime"] > last_send_time:
                last_send_time = presents[key]["sponsors"][sponser_id]["sendTime"]
    return send_money, last_send_time


def present_remove(handle) -> bool:
    is_remove = False
    for qq_id in presents:
        if presents[qq_id]['id'] == handle:
            del presents[qq_id]
            is_remove = True
            break
    with open(PRESENT_PATH, 'w') as f:
        f.write(json.dumps(presents))
    return is_remove


def internal_send_presents(sender_id: int):
    global presents
    with open(PRESENT_PATH, "r") as f:
        old = f.read()
        if old != "":
            old = json.loads(old)
        else:
            old = {}
    await_send_list = []
    total_send = 0
    for key in old:
        for sponsors in old[key]["sponsors"]:
            if old[key]["sponsors"][sponsors]["hasSend"]:
                total_send += 50000
        if total_send >= 200000:
            total_send = 0
            continue
        if str(sender_id) in old[key]["sponsors"] and not old[key]["sponsors"][str(sender_id)][
            "hasSend"]:
            old[key]["sponsors"][str(sender_id)] = {
                "hasSend": True,
                "sendTime": int(time.time())
            }
        total_send = 0
    with open(PRESENT_PATH, "w") as f:
        f.write(json.dumps(old))
    presents = old