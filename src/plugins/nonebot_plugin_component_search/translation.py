from pathlib import Path
from typing import Dict, Optional


class Translation:
    translations: Dict[str, str] = {
        "WeaponGun": "武器",
        "Gun": "机炮",
        "laser cannon": "激光加农炮",
        "plasma cannon": "电浆加农炮",
        "distortion scattergun": "畸变霰弹炮",
        "ballistic gatling": "实弹加特林",
        "laser repeater": "能量速射炮",
        "ballistic cannon": "实弹加农炮",
        "laser scattergun": "激光霰弹炮",
        "distortion repeater": "畸变速射炮",
        "rocket pod": "火箭炮",
        "tachyon cannon": "快子加农炮",
        "ballistic scattergun": "实弹霰弹炮",
        "CrossSection": "横截面制导",
        "Infrared": "红外制导",
        "Electromagnetic": "电磁制导",
        "ballistic repeater": "实弹速射炮",
        "distortion cannon": "畸变加农炮",


        # shop names
        "Area18": "18区",
        "Astro Armada": "天文舰队",
        "Cargo Offices": "货物办公室",
        "CenterMass": "中心质量",
        "New Babbage": "新巴贝奇",
        "Orison": "奥里森",
        "Cousin Crows": "乌鸦表哥订制工艺",
        "Crusader Showroom": "十字军展厅",
        "Grim HEX": "海盗站",
        "Port Olisar": "奥丽莎空间站",
        "Dumper's Depot": "倾卸者仓库",
        "Lorville": "罗威尔",
        "New Deal": "全新交易",
        "Omega Pro": "欧米伽Pro",
        "Platinum Bay": "白金湾",
        "ARC L1": "弧L1",
        "ARC L2": "弧L2",
        "ARC L3": "弧L3",
        "ARC L4": "弧L4",
        "ARC L5": "弧L5",
        "Bajini Point": "巴吉尼点",
        "CRU L1": "十L1",
        "CRU L2": "十L2",
        "CRU L3": "十L3",
        "CRU L4": "十L4",
        "CRU L5": "十L5",
        "Everus Harbor": "埃弗勒斯空间站",
        "HUR L2": "赫L2",
        "HUR L3": "赫L3",
        "HUR L4": "赫L4",
        "HUR L5": "赫L5",
        "Port Tressler": "特雷斯勒空间站",
        "Refinery Store": "精炼商店",
        "MIC L1": "微L1",
        "MIC L2": "微L2",
        "MIC L3": "微L3",
        "Regal Luxury": "王权奢华租赁",
        "Ship Weapons Shop": "船舶武器店",
        "Shubin Interstellar Services": "舒宾星际",
        "Tammany & Sons": "坦姆尼父子",
        "Traveler Rentals": "旅行者租赁",
        'Vantage Rentals': "优越租赁",
        'HD Showcase': 'HD展厅',

        # class names
        "Industrial": "工业",
        "Civilian": "平民",
        "Competition": "竞赛",
        "Military": "军事",
        "Stealth": "隐身",
        "": "-"
    }

    def __init__(self, path: Path):
        """
        Initializes the class with the path to the file
        :param path:
        """
        self.path: Path = path
        if not self.path.exists():
            print(f'{self.path} does not exist')
            raise FileNotFoundError
        self.data: Dict[str, str] = {}
        self.read()

    def read(self):
        """
        Reads the file and stores the data in a dictionary
        :return:
        """
        with self.path.open('r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                self.data[key] = value

    def get_item_name(self, name: str) -> Optional[str]:
        if 'emp' in name and 'emp_device' not in name:
            name = '_'.join(name.split('_')[:-1])
        if 'rpod' in name:
            name_list: list[str] = name.split('_')
            name_list[0], name_list[2] = name_list[2], name_list[0]
            name = '_'.join(name_list)
        if 'emp_device' in name:
            name_list: list[str] = name.split('_')
            del name_list[1]
            name = '_'.join(name_list)
        for key in self.data:
            if f"item_name_{name}" == key.lower():
                return self.data[key]
            if f"item_name{name}" == key.lower():
                return self.data[key]
            if f"item_{name}" == key.lower():
                return self.data[key]
            if key.lower().startswith(f"item_name_{name}_"):
                return self.data[key]
            if key.lower().startswith(f"item_name{name}_"):
                return self.data[key]
        return None

    def get_item_name_short(self, name: str) -> Optional[str]:
        if 'emp' in name and 'emp_device' not in name:
            name = '_'.join(name.split('_')[:-1])
        if 'rpod' in name:
            name_list: list[str] = name.split('_')
            name_list[0], name_list[2] = name_list[2], name_list[0]
            name = '_'.join(name_list)
        if 'emp_device' in name:
            name_list: list[str] = name.split('_')
            del name_list[1]
            name = '_'.join(name_list)
        for key in self.data:
            if f"item_name_{name}_short" == key.lower():
                return self.data[key]
            if f"item_name{name}_short" == key.lower():
                return self.data[key]
            if f"item_{name}_short" == key.lower():
                return self.data[key]
            if key.lower().startswith(f"item_name_{name}_") and key.lower().endswith('_short'):
                return self.data[key]
            if key.lower().startswith(f"item_name{name}_") and key.lower().endswith('_short'):
                return self.data[key]
        return None

    def get_item_description(self, name: str) -> Optional[str]:
        if 'emp' in name and 'emp_device' not in name:
            name = '_'.join(name.split('_')[:-1])
        if 'rpod' in name:
            name_list: list[str] = name.split('_')
            name_list[0], name_list[2] = name_list[2], name_list[0]
            name = '_'.join(name_list)
        if 'emp_device' in name:
            name_list: list[str] = name.split('_')
            del name_list[1]
            name = '_'.join(name_list)
        for key in self.data:
            if f"item_desc_{name}" == key.lower():
                return self.data[key]
            if f"item_desc{name}" == key.lower():
                return self.data[key]
            if f"item_{name}_desc" == key.lower():
                return self.data[key]
            if key.lower().startswith(f"item_desc_{name}_"):
                return self.data[key]
            if key.lower().startswith(f"item_desc{name}_"):
                return self.data[key]
        return None

    def get_vehicle_name(self, name: str) -> Optional[str]:
        for key in self.data:
            if f"vehicle_name_{name}" == key.lower():
                return self.data[key]
            if f"vehicle_name{name}" == key.lower():
                return self.data[key]
        return None

    def get_vehicle_name_short(self, name: str) -> Optional[str]:
        for key in self.data:
            if f"vehicle_name_{name}_short" == key.lower():
                return self.data[key]
            if f"vehicle_name{name}_short" == key.lower():
                return self.data[key]
        return None

    def get_vehicle_description(self, name: str) -> Optional[str]:
        for key in self.data:
            if f"vehicle_desc_{name}" == key.lower():
                return self.data[key]
            if f"vehicle_desc{name}" == key.lower():
                return self.data[key]
        return None

    def get_manufacturer_name(self, name: str, short_name: str, description: Optional[str]) -> Optional[str]:
        for key in self.data:
            if f"manufacturer_name_{name}".lower() == key.lower():
                return self.data[key]
            if f"manufacturer_name{name}".lower() == key.lower():
                return self.data[key]
            if f"manufacturer_name_{short_name}".lower() == key.lower():
                return self.data[key]
            if f"manufacturer_name{short_name}".lower() == key.lower():
                return self.data[key]
        try:
            if description and '制造商' in description:
                chinese_name: Optional[str] = description.split('\\n')[0].strip().replace('制造商：', '')
                if '(' in chinese_name:
                    chinese_name = chinese_name.split('(')[0].strip()
                return chinese_name
        except Exception as e:
            print(e)

        return None

    @classmethod
    def get_translation(cls, name: str) -> Optional[str]:
        if name in cls.translations:
            return cls.translations[name]
        return None

