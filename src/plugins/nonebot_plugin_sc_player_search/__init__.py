from nonebot import get_driver, Bot, on_message
from nonebot.adapters.onebot.v11 import Bot, Event, Message, GroupMessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.params import State
import httpx
from .data_source import current_folder
from lxml import etree
from nonebot.rule import Rule
from nonebot.typing import T_State
from .config import Config
from dateutil.parser import parse
from PIL import Image, ImageDraw, ImageFont
import os
import json
import qrcode
import datetime

global_config = get_driver().config
config = Config(**global_config.dict())


SRC_URI = os.path.join(current_folder, 'src')


def transparent_back(image):
    img = image.convert('RGBA')
    L, H = img.size
    color_0 = (102, 204, 255, 255)
    for h in range(H):
        for l in range(L):
            dot = (l, h)
            color_1 = img.getpixel(dot)
            if color_1 == color_0:
                color_1 = color_1[:-1] + (0,)
                img.putpixel(dot, color_1)
    return img


def circle_corner(img, radii):
    """
    圆角处理
    :param img: 源图象。
    :param radii: 半径，如：30。
    :return: 返回一个圆角处理后的图象。
    """

    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形

    # 原图
    img = img.convert("RGBA")
    w, h = img.size

    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
    # alpha.show()

    img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
    return img


def enlist_time_modify(time: str) -> str:
    enlist_time = parse(time)
    return enlist_time.strftime('%Y年%m月%d日')


def get_number(name):
    if not os.path.exists(os.path.join(SRC_URI, 'number_dict.json')):
        number_dict = {name: 0}
        with open(os.path.join(SRC_URI, 'number_dict.json'), 'w') as f:
            f.write(json.dumps(number_dict))
        return 0

    else:
        with open(os.path.join(SRC_URI, 'number_dict.json'), 'r') as f:
            number_dict = json.loads(f.read())
        if name in number_dict:
            return number_dict[name]
        else:
            current_number = len(number_dict)
            number_dict[name] = current_number
            with open(os.path.join(SRC_URI, 'number_dict.json'), 'w') as f:
                f.write(json.dumps(number_dict))
            return current_number


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
    root.xpath('//*[@id="public-profile"]/div[2]/div[1]/div/div[1]/div/div[2]/p[1]/strong/text()')[0].__str__()
    information_lib['handle_name'] = \
    root.xpath('//*[@id="public-profile"]/div[2]/div[1]/div/div[1]/div/div[2]/p[2]/strong/text()')[0].__str__()
    information_lib['enlisted'] = enlist_time_modify(root.xpath('//*[@id="public-profile"]/div[2]/div[2]/div/p[1]/strong/text()')[0].__str__())
    information_lib['ranking_data'] = len(root.xpath('//span[@class="active"]'))

    if 'NO MAIN ORG FOUND IN PUBLIC RECORDS' not in r.text:
        information_lib['main_organization_name'] = \
        root.xpath('//*[@id="public-profile"]/div[2]/div[1]/div/div[2]/div/div[2]/p[1]/a/text()')[0].__str__()
        information_lib['main_organization_sid'] = \
        root.xpath('//*[@id="public-profile"]/div[2]/div[1]/div/div[2]/div/div[2]/p[2]/strong/text()')[0].__str__()
        information_lib['organization_rank'] = \
        root.xpath('//*[@id="public-profile"]/div[2]/div[1]/div/div[2]/div/div[2]/p[3]/strong/text()')[0].__str__()

    avater_url = root.xpath('//*[@id="public-profile"]/div[2]/div[1]/div/div[1]/div/div[1]/img')[0].attrib['src']
    location = root.xpath('//*[@id="public-profile"]/div[2]/div[2]/div/p[2]/strong/text()')[0]
    information_lib['avatar_url'] = 'https://robertsspaceindustries.com' + avater_url
    information_lib['location'] = location.__str__().replace(' ', '').replace('\n', '').replace(',', ', ').replace(', Jilin', '')
    information_lib['number'] = get_number(information_lib['handle_name'].lower())
    return information_lib


async def card_maker(info_lib):
    my_headers = {
        'referer': 'https://robertsspaceindustries.com/orgs',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
    }
    async with httpx.AsyncClient() as client:
        avatar = await client.get(info_lib['avatar_url'], headers=my_headers)
    with open(os.path.join(SRC_URI, f'temp_{info_lib["handle_name"]}'), 'wb') as f:
        f.write(avatar.content)
    card = Image.open(os.path.join(SRC_URI, 'card_background.png')).convert('RGBA')
    user_avatar = Image.open(os.path.join(SRC_URI, f'temp_{info_lib["handle_name"]}')).convert('RGBA')
    user_avatar_width = int(card.height / 3)
    user_avatar = user_avatar.resize((user_avatar_width, user_avatar_width))
    user_avatar = circle_corner(user_avatar, 20)

    card.paste(user_avatar, (200, user_avatar_width, 200 + user_avatar_width, 2*user_avatar_width), user_avatar)

    font_color = '#c3ab94'
    handle_font = ImageFont.truetype(os.path.join(SRC_URI, 'WeiRuanYaHei-1.ttf'), 75)
    info_font = ImageFont.truetype(os.path.join(SRC_URI, 'WeiRuanYaHei-1.ttf'), 30)
    number_font = ImageFont.truetype(os.path.join(SRC_URI, 'WeiRuanYaHei-1.ttf'), 40)
    draw = ImageDraw.Draw(card)
    sc_icon = Image.open(os.path.join(SRC_URI, 'sc_icon.png'))
    # sc_icon = sc_icon.resize(int(sc_icon.width * 0.6), int(sc_icon.height * 0.6))

    card.paste(sc_icon, (1200, 0, 1200 + sc_icon.width, 0 + sc_icon.height), sc_icon)
    draw.text((50, 50), text=f'NO.{100000 + info_lib["number"]}', fill=font_color, font=number_font)
    draw.line((320 + user_avatar_width, user_avatar_width + 40, 320 + user_avatar_width, 2 * user_avatar_width - 40), width=5, fill=font_color)
    draw.text((440 + user_avatar_width, 220), font=handle_font, fill=font_color, text=info_lib['handle_name'])
    if "organization_rank" not in info_lib:
        draw.text((440 + user_avatar_width, 320), font=info_font, fill=font_color,
                  text='公民')
        draw.text((440 + user_avatar_width, 400), font=info_font, fill=font_color,
                  text='无归属舰队')
        draw.text((440 + user_avatar_width, 440), font=info_font, fill=font_color,
                  text='雇佣兵')
    elif '  ' in info_lib["organization_rank"]:
        draw.text((440 + user_avatar_width, 320), font=info_font, fill=font_color,
                  text='██████████████')
        draw.text((440 + user_avatar_width, 400), font=info_font, fill=font_color,
                  text='██████')
        draw.text((440 + user_avatar_width, 440), font=info_font, fill=font_color,
                  text='██████')
    else:
        draw.text((440 + user_avatar_width, 320), font=info_font, fill=font_color, text=f'{info_lib["organization_rank"]}[LV.{info_lib["ranking_data"]}]')
        draw.text((440 + user_avatar_width, 400), font=info_font, fill=font_color, text=info_lib['main_organization_name'])
        draw.text((440 + user_avatar_width, 440), font=info_font, fill=font_color, text=info_lib['main_organization_sid'])
    draw.text((440 + user_avatar_width, 520), font=info_font, fill=font_color, text='入伍时间')
    draw.text((440 + user_avatar_width, 560), font=info_font, fill=font_color, text=info_lib['enlisted'])
    draw.text((440 + user_avatar_width, 630), font=info_font, fill=font_color, text='注册地点')
    draw.text((440 + user_avatar_width, 670), font=info_font, fill=font_color, text=info_lib['location'])



    info_url = f'https://robertsspaceindustries.com/citizens/{info_lib["handle_name"]}'

    qr = qrcode.QRCode(
            version=3,
            box_size=10,
            border=1)
    qr.add_data(info_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=font_color, back_color=(102, 204, 255, 255))
    qr_img = transparent_back(qr_img)
    qr_img = qr_img.resize((170, 170))

    card.paste(qr_img, (1325, 670, 1325 + qr_img.width, 670 + qr_img.height), qr_img)
    card = circle_corner(card, 40)
    if not os.path.exists(os.path.join(current_folder, 'cards')):
        os.mkdir(os.path.join(current_folder, 'cards'))
    card.save(os.path.join(current_folder, 'cards', f'{info_lib["handle_name"]}.png'))
    return os.path.join(current_folder, 'cards', f'{info_lib["handle_name"]}.png')


def alias_command(message: str, allow_key: list, start_search: bool):
    enabled_command_starter = global_config.enabled_command_starter
    if not message:
        return None
    if start_search and message[0] not in enabled_command_starter:
        return None
    if message:
        if message[0] in enabled_command_starter:
            message = message[1:].strip()
        for key in allow_key:
            if message.startswith(key):
                return message.replace(key, '')
        return None
    else:
        return None


def is_search_player() -> Rule:
    async def _is_search_player(bot: Bot, event: Event, state: T_State=State()) -> bool:
        command = event.get_plaintext()
        handle = alias_command(command, Config.Config.allow_search_player_key, True)
        if handle:
            state['handle'] = handle.strip()
            return True
        else:
            return False
    return Rule(_is_search_player)


search_player = on_message(rule=is_search_player(), priority=20)


@search_player.handle()
async def _search_player(bot: Bot, event: Event, state: T_State=State()):
    try:
        player_info = await get_player(state['handle'])
    except Exception:
        await bot.send(event, Message(MessageSegment.text('诶？\n小伙伴提供的ID貌似有错误呢...')))
        return

    card_uri = await card_maker(player_info)
    with open(card_uri, 'rb') as f:
        await bot.send(event, Message(MessageSegment.image(f.read())))

    if isinstance(event, GroupMessageEvent):
        await bot.call_api('send_group_msg', message=f'[CQ:poke,qq={event.sender.user_id}]', group_id=event.group_id)

