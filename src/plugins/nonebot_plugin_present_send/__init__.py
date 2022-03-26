import nonebot
from nonebot import on_startswith
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, GroupMessageEvent, MessageSegment
from nonebot import get_driver
from lxml import etree
from dateutil.parser import parse
import datetime
import httpx
import time
from .data_source import presents, insert_presents_data, get_all_money, get_total_money, present_remove, internal_send_presents, load_presents, PRESENT_PATH
import json
from .config import Config, current_folder, save_config_to_yaml, get_config
import os

global_config = get_driver().config
if not os.path.exists(os.path.join(current_folder, "config.yaml")):
    save_config_to_yaml(Config.Config.default_config)
config: dict = get_config()
player_export = nonebot.export()

present_sender = on_startswith('.礼包', priority=20)
present_register = on_startswith('.申请礼包', priority=20)
present_delete = on_startswith('.移除礼包', priority=20)
send_presents = on_startswith('.发送礼包', priority=20)


def enlist_time_modify(time: str) -> str:
    enlist_time = parse(time)
    return enlist_time.strftime('%y年%m月%d日')


def refresh_data():
    global presents
    with open(PRESENT_PATH, 'r') as f:
        presents = json.loads(f.read())


def count_sent_money(qq_id: str) -> dict:
    total_count = {}
    if qq_id in presents:
        total_count['is_requested'] = True
        send_money = 0
        for sponsor in presents[qq_id]['sponsors']:
            if presents[qq_id]['sponsors'][sponsor]['hasSend']:
                send_money += 50000
        request_time: str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(presents[qq_id]['requestTime']))
        if send_money < 200000:
            total_count['message'] = "呐呐呐～\n申请ID：{}\n申请时间：{}\n申请金额：200000\n已发放：{}({}%)\n请小伙伴耐心等待哦～".format(
                presents[qq_id]['id'],
                request_time,
                send_money, int(
                    send_money / 200000 * 100))
        else:
            total_count['message'] = "呐呐呐～\n申请ID：{}\n申请时间：{}\n申请金额：200000\n已发放：{}({}%)\n礼包已全部发放～快登录游戏看看吧！".format(
                presents[qq_id]['id'],
                request_time,
                send_money, int(
                    send_money / 200000 * 100))
        return total_count


    else:
        total_count['is_requested'] = False
        return total_count


async def get_player(name) -> dict:
    my_headers = {
        'referer': 'https://robertsspaceindustries.com/orgs',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }
    information_lib = {}

    async with httpx.AsyncClient() as client:
        r = await client.get('https://robertsspaceindustries.com/citizens/{}'.format(name.lower()), headers=my_headers)
    root = etree.HTML(r.text)
    information_lib['name'] = \
    root.xpath('//*[@id="public-profile"]/div[2]/div[1]/div/div[1]/div/div[2]/p[1]/strong/text()')[0]
    information_lib['handle_name'] = \
    root.xpath('//*[@id="public-profile"]/div[2]/div[1]/div/div[1]/div/div[2]/p[2]/strong/text()')[0]
    information_lib['enlisted'] = root.xpath('//*[@id="public-profile"]/div[2]/div[2]/div/p[1]/strong/text()')[0]
    information_lib['ranking_data'] = len(root.xpath('//span[@class="active"]'))
    # print(html.text)

    if 'NO MAIN ORG FOUND IN PUBLIC RECORDS' not in r.text:
        information_lib['main_organization_name'] = \
        root.xpath('//*[@id="public-profile"]/div[2]/div[1]/div/div[2]/div/div[2]/p[1]/a/@href')[0].split('/')[-1]
        information_lib['main_organization_sid'] = \
        root.xpath('//*[@id="public-profile"]/div[2]/div[1]/div/div[2]/div/div[2]/p[2]/strong/text()')[0]
        information_lib['organization_rank'] = \
        root.xpath('//*[@id="public-profile"]/div[2]/div[1]/div/div[2]/div/div[2]/p[3]/strong/text()')[0]

    return information_lib


@present_sender.handle()
async def present(bot: Bot, event: MessageEvent):
    global presents
    load_presents()
    refresh_data()
    if isinstance(event, GroupMessageEvent):
        if event.sender.user_id not in config['sponsor_id']:
            total_send: dict = count_sent_money(str(event.sender.user_id))
            if total_send['is_requested']:
                await bot.send(event, Message(MessageSegment.text(total_send['message'])), at_sender=True)
            else:
                await bot.send(event, Message(MessageSegment.text('嗯...小伙伴貌似没有申请礼包呢...\n试试「.申请礼包 游戏ID」?')), at_sender=True)
        else:
            await_send_list = []
            total_send_money = 0
            for key in presents:
                for sponsors in presents[key]["sponsors"]:
                    if presents[key]["sponsors"][sponsors]["hasSend"]:
                        total_send_money += 50000
                if total_send_money >= 200000:
                    total_send_money = 0
                    continue
                if str(event.sender.user_id) in presents[key]["sponsors"] and not presents[key]["sponsors"][str(event.sender.user_id)]["hasSend"]:
                    await_send_list.append(presents[key]["id"])
                total_send_money = 0
            message = [MessageSegment.text("以下为当前待资助萌新:\n")]
            for i in await_send_list:
                message.append(MessageSegment.text("{}\n".format(i)))
            sponser_total_money, last_send_time = get_total_money(str(event.sender.user_id))
            all_money, all_last_send = get_all_money()
            message.append(MessageSegment.text("\n已发放：{}/{}aUEC, 上次发放：{}".format(sponser_total_money, all_money,
                                                                    time.strftime("%y{}%m{}%d{}", time.localtime(
                                                                        last_send_time)).format('年', '月', '日'))))
            message.append(MessageSegment.text("\n记得在资助完所有当前萌新后使用.发送礼包录入的说～"))
            if await_send_list:
                await bot.send(event, Message(message), at_sender=True)
            else:
                await bot.send(event, Message([MessageSegment.text('么么哒～没有萌新待资助的说～')]))


@present_register.handle()
async def present_request(bot: Bot, event: MessageEvent):
    if isinstance(event, GroupMessageEvent):
        if event.group_id not in config['enabled_groups']:
            await bot.send(event, Message(MessageSegment.text('当前无法申请礼包的说～')), at_sender=True)
            return
        global presents
        load_presents()
        refresh_data()
        from .data_source import presents
        player_id: str = event.get_plaintext().replace('.申请礼包', '').strip()
        player_info = {}
        try:
            player_info = await get_player(player_id)
        except:
            await bot.send(event, Message([MessageSegment.text('诶？\n小伙伴提供的ID貌似有错误呢...\n只有输入正确ID才能 申 请 礼 包 哦～')]))
            return
        message = [
            MessageSegment.text("Name：{}\n".format(player_info['name'])),
            MessageSegment.text('Handle：{}\n'.format(player_info['handle_name']))
        ]
        if 'main_organization_name' in player_info:
            if player_info['main_organization_name']:
                message.append(MessageSegment.text("组织名称：{}\n".format(player_info['main_organization_name'])))
            else:
                message.append(MessageSegment.text("组织名称：[数据删除]\n"))
            if player_info['main_organization_name']:
                message.append(MessageSegment.text(f"组织等级：{player_info['organization_rank']}[lv.{player_info['ranking_data']}]\n"))
            else:
                message.append(MessageSegment.text("组织等级：[数据删除]\n"))
        else:
            message.append(MessageSegment.text('组织：无归属\n'))
        message.append(MessageSegment.text("注册时间：{}\n".format(enlist_time_modify(player_info['enlisted']))))
        enlist_time = parse(player_info['enlisted'])
        if datetime.datetime.now() - enlist_time > datetime.timedelta(days=14):
            message.append(MessageSegment.text("小伙伴的注册时间大于5天了呢～小九也帮不上忙的说..."))
            await bot.send(event, Message(message), at_sender=True)
        else:
            insert_presents_data(event.sender.user_id, player_id)
            message.append(MessageSegment.text("礼包申请成功哟～请小伙伴耐心等待的说～"))
            await bot.send(event, Message(message), at_sender=True)


@present_delete.handle()
async def present_request(bot: Bot, event: MessageEvent):
    if isinstance(event, GroupMessageEvent):
        global presents
        load_presents()
        refresh_data()
        if event.sender.user_id in config['sponsor_id']:
            remove_handle = event.get_plaintext().replace('.移除礼包', '').strip()
            is_remove = present_remove(remove_handle)
            if is_remove:
                await bot.send(event, Message([MessageSegment.text('Master～礼包申请移除成功哦～')]))
            else:
                await bot.send(event, Message([MessageSegment.text('ID貌似有错误的说～')]))


@send_presents.handle()
async def _send_presents(bot: Bot, event: MessageEvent):
    if isinstance(event, GroupMessageEvent):
        global presents
        load_presents()
        refresh_data()
        if event.sender.user_id in config['sponsor_id']:
            internal_send_presents(event.sender.user_id)
            await bot.send(event, Message(MessageSegment.text('礼包发送成功哦～')))
            from .data_source import presents
        else:
            await bot.send(event, Message(MessageSegment.text('欢迎申请成为赞助者的说～')))
