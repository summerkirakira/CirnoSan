from .models import Missile, Shop, Sheet, SearchItem, ComponentData, Paint, QDrive, Weapon, Shield, PowerPlant, Cooler
from typing import Union
from .loader import Loader
import pathlib
import time
from .translation import Translation

from PIL import Image, ImageDraw, ImageFont
import json


class PicDrawer:
    def __init__(self):
        self.font_path: pathlib.Path = pathlib.Path(__file__).parent / "data" / "fonts" / "WeiRuanYaHei.ttf"
        self.font = ImageFont.truetype(str(self.font_path), size=24)
        self.font_big = ImageFont.truetype(str(self.font_path), size=32)
        self.font_bigger = ImageFont.truetype(str(self.font_path), size=48)
        self.width = 1400
        self.draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
        self.watermark_path = pathlib.Path(__file__).parent / "data" / "image" / "watermark.png"

        self.watermark = Image.open(str(self.watermark_path)).convert("RGBA")

    def get_font_render_size(self, text: str, font: ImageFont) -> tuple[int, int]:
        """
        Returns the size of the text rendered with the given font
        :param text: the text
        :param font: the font
        :return: the size of the text rendered with the given font
        """
        box = self.draw.textbbox((0, 0), text=text, font=font)
        return box[2] - box[0], box[3] - box[1]

    @classmethod
    def draw_text(cls, draw: ImageDraw, text: str, x: int, y: int, font: ImageFont, fill=(0, 0, 0)):
        """
        Draws the text with the given font at the given position
        :param fill:
        :param draw: the ImageDraw object
        :param text: the text
        :param x: the x position
        :param y: the y position
        :param font: the font
        :return:
        """
        draw.text((x, y), text, font=font, fill=fill)

    @classmethod
    def add_watermark_png(cls, image: Image, water_mark: Image):
        """
        Adds a watermark to the given image
        :param image: the image
        :param water_mark: the watermark
        :return: the image with the watermark
        """
        image.paste(water_mark, (image.width - water_mark.width, image.height - water_mark.height), water_mark)
        return image

    def draw_sheet(self, sheet: Sheet) -> Image:
        """
        Draws a sheet with the given data
        :param sheet: the sheet
        :return:
        """
        sheet_height = sheet.row_height * len(sheet.columns) + sheet.header_height
        sheet_pic = Image.new('RGB', (sheet.width, sheet_height), (255, 255, 255))
        title_size = self.get_font_render_size(sheet.title, self.font_bigger)
        draw = ImageDraw.Draw(sheet_pic)
        self.draw_text(draw,
                       sheet.title,
                       int((sheet.width - title_size[0]) / 2),
                       -5 + int((sheet.header_height - title_size[1]) / 2),
                       self.font_bigger)
        true_width: int = sheet.width - sheet.margin * 2
        current_row: int = 0
        current_width_position: float = 0
        current_column: int = 0
        for row_position in range(len(sheet.columns)):
            current_color: str = sheet.colors[row_position % len(sheet.colors)]
            draw.rectangle(((0, row_position * sheet.row_height + sheet.header_height),
                            (sheet.width, (row_position + 1) * sheet.row_height + sheet.header_height)),
                           fill=current_color,
                           width=0)

        for column in sheet.columns:
            for word in column.data:
                word_size = self.get_font_render_size(word, self.font)
                self.draw_text(draw,
                               word,
                               int(current_width_position * true_width) + sheet.margin,
                               -5 + sheet.header_height + current_row * sheet.row_height + int((sheet.row_height - word_size[1]) / 2),
                               self.font)
                current_width_position += sheet.width_ratio[current_column]
                current_column += 1
            current_row += 1
            current_width_position = 0
            current_column = 0
        self.add_watermark_png(sheet_pic, self.watermark)
        return sheet_pic


class Calculator:
    def __init__(self):
        self.loader = Loader()
        self.missiles = self.loader.missiles
        self.shops = self.loader.shops
        self.bombs = self.loader.bombs
        self.shields = self.loader.shields
        self.weapons = self.loader.weapons
        self.coolers = self.loader.coolers
        self.ships = self.loader.ships
        self.mounts = self.loader.mounts
        self.power_plants = self.loader.power_plants
        self.qdrives = self.loader.qdrives
        self.qeds = self.loader.qeds
        self.utilities = self.loader.utilities
        self.paints = self.loader.paints
        self.missile_racks = self.loader.missile_racks
        self.emps = self.loader.emps
        self.drawer = PicDrawer()
        self.register_shop_items()

    def find_item_by_ref(self, ref: str) -> SearchItem:
        results = SearchItem()
        for shop in self.shops:
            for item in shop.data.inventory:
                if item.ref == ref:
                    results.results.append(SearchItem.Result(shop=shop, item=item))
        return results

    def find_item_by_component(self, component: Union[ComponentData, Paint]) -> SearchItem:
        results = SearchItem()
        for shop in self.shops:
            for item in shop.data.inventory:
                if item.ref == component.data.ref:
                    results.results.append(SearchItem.Result(shop=shop, item=item))
                    if not item.item:
                        item.item = component
        return results

    def register_shop_items(self):
        for missile in self.missiles:
            self.find_item_by_component(missile)
        for weapon in self.weapons:
            self.find_item_by_component(weapon)
        for bomb in self.bombs:
            self.find_item_by_component(bomb)
        for shield in self.shields:
            self.find_item_by_component(shield)
        for cooler in self.coolers:
            self.find_item_by_component(cooler)
        for ship in self.ships:
            self.find_item_by_component(ship)
        for mount in self.mounts:
            self.find_item_by_component(mount)
        for power_plant in self.power_plants:
            self.find_item_by_component(power_plant)
        for qdrive in self.qdrives:
            self.find_item_by_component(qdrive)
        for qed in self.qeds:
            self.find_item_by_component(qed)
        for utility in self.utilities:
            self.find_item_by_component(utility)
        for paint in self.paints:
            self.find_item_by_component(paint)
        for missile_rack in self.missile_racks:
            self.find_item_by_component(missile_rack)

    @staticmethod
    def generate_shop_sheet(shop: Shop) -> Sheet:
        data = {
            "title": f"{shop.data.name} ({shop.data.location}) 商品价格表",
            "width": 2000,
            "width_ratio": [0.20, 0.142, 0.142, 0.142, 0.10, 0.142, 0.142],
            "column_size": 7,
            "columns": []
        }
        item_info = {"data": ["中文名", "英文名", "类别", "类型", "等级", "制造商", "价格"]}
        data["columns"].append(item_info)
        for item in shop.data.inventory:
            info_list: dict[str, list[str]] = {"data": []}
            if item.item and isinstance(item.item, ComponentData):
                if item.item.data.chineseName:
                    info_list["data"].append(item.item.data.chineseName)
                else:
                    info_list["data"].append("-")
                if item.item.data.name:
                    info_list["data"].append(item.item.data.name)
                else:
                    info_list["data"].append("-")
                info_list["data"].append(item.item.type)
                if item.item.data.itemClass:
                    info_list["data"].append(f"{item.item.data.itemClass} {item.item.data.grade}")
                else:
                    info_list["data"].append(f"{item.item.data.grade}")
                info_list["data"].append(str(item.item.data.size))
                if item.item.data.manufacturerData.data.chineseName:
                    info_list["data"].append(item.item.data.manufacturerData.data.chineseName)
                elif item.item.data.manufacturerData.data.name:
                    info_list["data"].append(item.item.data.manufacturerData.data.name)
                else:
                    info_list["data"].append("-")
                info_list["data"].append(f"{item.basePrice} aUEC")
                data["columns"].append(info_list)
        return Sheet(**data)

    def generate_shop_item_pic(self, shop: Shop) -> Image:
        sheet = self.generate_shop_sheet(shop)
        return self.drawer.draw_sheet(sheet)

    def get_match_items_by_name(self, name: str, limit: int = 5) -> list[tuple[ComponentData, float]]:
        results: list[tuple[ComponentData, float]] = []
        match_list: list[list[ComponentData]] = [
            self.missiles, self.weapons, self.bombs, self.shields, self.coolers, self.ships, self.mounts,
            self.power_plants, self.qdrives, self.qeds, self.utilities, self.shops
        ]
        for component_list in match_list:
            results += self.get_match_list_by_name(name, component_list)

        results = sorted(results, key=lambda x: x[1], reverse=True)
        return results[:limit]

    @classmethod
    def get_match_list_by_name(cls, name: str, data: list[ComponentData]) -> list[tuple[ComponentData, float]]:
        return [(item, item.get_match_ratio(name)) for item in data]

    def generate_item_type_pic(self, item_list: Union[list[ComponentData], list[Shop]], sort_by: str = "") -> Image:
        if isinstance(item_list[0], Shop):
            item_list = sorted(item_list, key=lambda x: x.data.nameChinese if x.data.nameChinese else x.data.name)
            data = {
                "title": f"星际公民商店信息表({time.strftime('%Y-%m-%d %H:%M:%S')})",
                "width": 2000,
                "width_ratio": [0.25, 0.25, 0.25, 0.25],
                "column_size": 4,
                "columns": []
            }
            data["columns"].append({"data": ["商店名称(英)", "商店名称(中)", "商店地点(英)", "商店地点(中)"]})
            for shop in item_list:
                if not shop.data.nameChinese:
                    shop.data.nameChinese = "-"
                if not shop.data.locationChinese:
                    shop.data.locationChinese = "-"
                data["columns"].append({"data": [shop.data.name, shop.data.nameChinese, shop.data.location, shop.data.locationChinese]})
            return self.drawer.draw_sheet(Sheet(**data))
        elif isinstance(item_list[0], Weapon):
            if sort_by == "":
                item_list = sorted(item_list, key=lambda x: x.data.size)
            elif sort_by == "group":
                item_list = sorted(item_list, key=lambda x: x.data.group)
            data = {
                "title": f"星际公民机炮信息表({time.strftime('%Y-%m-%d %H:%M:%S')})",
                "width": 3000,
                "width_ratio": [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125],
                "column_size": 8,
                "columns": []
            }
            data["columns"].append({"data": ["武器名称(英)", "武器名称(中)", "武器类别", "等级", "射速(s)", "每秒伤害", "弹药量", "射程(m)"]})
            for weapon in item_list:
                info_list: list[str] = [weapon.data.name]
                if weapon.data.chineseName:
                    info_list.append(weapon.data.chineseName)
                else:
                    info_list.append("-")
                group = Translation.get_translation(weapon.data.group)
                if not group:
                    group = "-"
                info_list.append(group)
                info_list.append(str(weapon.data.size))
                info_list.append(str(weapon.data.weapon.fireActions.fireRate))
                info_list.append(str(weapon.data.weapon.damage.alphaMax))
                ammo_count: str = str(weapon.data.ammoContainer.initialAmmoCount) \
                    if weapon.data.ammoContainer.initialAmmoCount != 0 else "∞"
                info_list.append(ammo_count)
                info_list.append(str(round(weapon.data.ammo.data.lifetime * weapon.data.ammo.data.speed)))
                data["columns"].append({"data": info_list})
            return self.drawer.draw_sheet(Sheet(**data))
        elif isinstance(item_list[0], Shield):
            if sort_by == "":
                item_list = sorted(item_list, key=lambda x: x.data.size)
            data = {
                "title": f"星际公民护盾信息表({time.strftime('%Y-%m-%d %H:%M:%S')})",
                "width": 2000,
                "width_ratio": [0.2, 0.2, 0.2, 0.2, 0.2],
                "column_size": 5,
                "columns": []
            }
            data["columns"].append({"data": ["护盾名称(英)", "护盾名称(中)", "等级", "强度", "护盾每秒恢复"]})
            for shield in item_list:
                info_list: list[str] = [shield.data.name]
                if shield.data.chineseName:
                    info_list.append(shield.data.chineseName)
                else:
                    info_list.append("-")
                info_list.append(str(shield.data.size))
                info_list.append(str(shield.data.shield.maxShieldHealth))
                info_list.append(str(shield.data.shield.maxShieldRegen))
                data["columns"].append({"data": info_list})
            return self.drawer.draw_sheet(Sheet(**data))
        elif isinstance(item_list[0], PowerPlant):
            if sort_by == "":
                item_list = sorted(item_list, key=lambda x: x.data.size)
            data = {
                "title": f"星际公民电源信息表({time.strftime('%Y-%m-%d %H:%M:%S')})",
                "width": 1500,
                "width_ratio": [0.25, 0.25, 0.25, 0.25],
                "column_size": 4,
                "columns": []
            }
            data["columns"].append({"data": ["电源名称(英)", "电源名称(中)", "等级", "发电量"]})
            for power_plant in item_list:
                info_list: list[str] = [power_plant.data.name]
                if power_plant.data.chineseName:
                    info_list.append(power_plant.data.chineseName)
                else:
                    info_list.append("-")
                info_list.append(str(power_plant.data.size))
                info_list.append(str(power_plant.data.power.powerDraw))
                data["columns"].append({"data": info_list})
            return self.drawer.draw_sheet(Sheet(**data))
        elif isinstance(item_list[0], Cooler):
            if sort_by == "":
                item_list = sorted(item_list, key=lambda x: x.data.size)
            data = {
                "title": f"星际公民冷却器信息表({time.strftime('%Y-%m-%d %H:%M:%S')})",
                "width": 1500,
                "width_ratio": [0.25, 0.25, 0.25, 0.25],
                "column_size": 4,
                "columns": []
            }
            data["columns"].append({"data": ["冷却器名称(英)", "冷却器名称(中)", "等级", "冷却速率"]})
            for cooler in item_list:
                info_list: list[str] = [cooler.data.name]
                if cooler.data.chineseName:
                    info_list.append(cooler.data.chineseName)
                else:
                    info_list.append("-")
                info_list.append(str(cooler.data.size))
                info_list.append(str(cooler.data.heat.mass))
                data["columns"].append({"data": info_list})
            return self.drawer.draw_sheet(Sheet(**data))
        elif isinstance(item_list[0], Missile):
            if sort_by == "":
                item_list = sorted(item_list, key=lambda x: x.data.size)
            data = {
                "title": f"星际公民导弹信息表({time.strftime('%Y-%m-%d %H:%M:%S')})",
                "width": 1500,
                "width_ratio": [0.2, 0.2, 0.2, 0.2, 0.2],
                "column_size": 5,
                "columns": []
            }
            data["columns"].append({"data": ["导弹名称(英)", "导弹名称(中)", "等级", "追踪类型", "伤害"]})
            for missile in item_list:
                info_list: list[str] = [missile.data.name]
                if missile.data.chineseName:
                    info_list.append(missile.data.chineseName)
                else:
                    info_list.append("-")
                info_list.append(str(missile.data.size))
                info_list.append(Translation.get_translation(missile.data.missile.trackingSignalType))
                info_list.append(str(missile.get_damage()))
                data["columns"].append({"data": info_list})
            return self.drawer.draw_sheet(Sheet(**data))
        elif isinstance(item_list[0], QDrive):
            if sort_by == "":
                item_list = sorted(item_list, key=lambda x: x.data.size)
            data = {
                "title": f"星际公民量子引擎信息表({time.strftime('%Y-%m-%d %H:%M:%S')})",
                "width": 2000,
                "width_ratio": [1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
                "column_size": 6,
                "columns": []
            }
            data["columns"].append({"data": ["量子引擎名称(英)", "量子引擎名称(中)", "定位", "等级", "跃迁速度", "燃料需求"]})
            for q_drive in item_list:
                info_list: list[str] = [q_drive.data.name]
                if q_drive.data.chineseName:
                    info_list.append(q_drive.data.chineseName)
                else:
                    info_list.append("-")
                item_class = f"{Translation.get_translation(q_drive.data.itemClass)} {q_drive.data.grade}"
                info_list.append(item_class)
                info_list.append(str(q_drive.data.size))
                info_list.append(str(q_drive.get_velocity_in_light()))
                info_list.append(str(q_drive.data.qdrive.quantumFuelRequirement))
                data["columns"].append({"data": info_list})
            return self.drawer.draw_sheet(Sheet(**data))


if __name__ == "__main__":
    calculator = Calculator()
    # calculator.generate_shop_item_pic(calculator.shops[16])
    # result = calculator.get_match_items_by_name("磨损", 10)
    # result = calculator.find_item_by_ref("85fd75f8-6c6c-4d3f-839f-988ae7660617")
    # with open("result.json", "w") as f:
    #     json.dump(result.dict(), f, indent=4, ensure_ascii=False)
    # while True:
    #     result = calculator.get_match_items_by_name(input("请输入查询名称："), 10)
    calculator.generate_item_type_pic(calculator.qdrives).show()
