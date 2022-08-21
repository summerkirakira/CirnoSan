from .models import Missile, Bomb, Shield, Weapon, Cooler, EMP, MiningLaser, Mount, PowerPlant, QDrive, Qed, Utility, Paint, MissileRack, Ship, Shop, ComponentData
import json
import pathlib
from typing import Callable
from .translation import Translation


class Loader:
    def __init__(self):
        self.missile_path = pathlib.Path(__file__).parent / "data" / "missiles.json"
        self.shop_path = pathlib.Path(__file__).parent / "data" / "shops.json"
        self.bomb_path = pathlib.Path(__file__).parent / "data" / "bombs.json"
        self.shield_path = pathlib.Path(__file__).parent / "data" / "shields.json"
        self.weapon_path = pathlib.Path(__file__).parent / "data" / "weapons.json"
        self.cooler_path = pathlib.Path(__file__).parent / "data" / "coolers.json"
        self.emp_path = pathlib.Path(__file__).parent / "data" / "emps.json"
        self.mining_laser_path = pathlib.Path(__file__).parent / "data" / "mining_lasers.json"
        self.mount_path = pathlib.Path(__file__).parent / "data" / "mounts.json"
        self.power_plant_path = pathlib.Path(__file__).parent / "data" / "power_plants.json"
        self.qdrive_path = pathlib.Path(__file__).parent / "data" / "qdrives.json"
        self.qed_path = pathlib.Path(__file__).parent / "data" / "qeds.json"
        self.utility_path = pathlib.Path(__file__).parent / "data" / "utilities.json"
        self.paint_path = pathlib.Path(__file__).parent / "data" / "paints.json"
        self.ship_path = pathlib.Path(__file__).parent / "data" / "ships.json"
        self.missile_rack_path = pathlib.Path(__file__).parent / "data" / "missile_racks.json"

        self.localization_path = pathlib.Path(__file__).parent / "data" / "global.ini"

        self.missiles: list[Missile] = []
        self.shops: list[Shop] = []
        self.bombs: list[Bomb] = []
        self.shields: list[Shield] = []
        self.weapons: list[Weapon] = []
        self.coolers: list[Cooler] = []
        self.emps: list[EMP] = []
        self.mining_lasers: list[MiningLaser] = []
        self.mounts: list[ComponentData] = []
        self.power_plants: list[PowerPlant] = []
        self.qdrives: list[ComponentData] = []
        self.qeds: list[ComponentData] = []
        self.utilities: list[Utility] = []
        self.paints: list[Paint] = []
        self.ships: list[Ship] = []
        self.missile_racks: list[ComponentData] = []

        self.localization = Translation(self.localization_path)

        self.load_all()

    def translate_component(func: Callable[['Loader'], list[ComponentData]], *args, **kwargs) -> Callable[
        ['Loader'], list[ComponentData]]:
        def wrapper(self: 'Loader') -> list[ComponentData]:
            components_list: list[ComponentData] = func(self)
            for component in components_list:
                component.data.chineseNameShort = self.localization.get_item_name_short(component.localName)
                component.data.chineseName = self.localization.get_item_name(component.localName)
                component.data.chineseDescription = self.localization.get_item_description(component.localName)
                if component.data.manufacturerData:
                    component.data.manufacturerData.data.chineseName = self.localization.get_manufacturer_name(
                        component.data.manufacturerData.data.calculatorName,
                        component.data.manufacturerData.data.nameSmall,
                        component.data.chineseDescription)
            return components_list

        return wrapper

    def translate_vehicle(func: Callable[['Loader'], list[ComponentData]], *args, **kwargs) -> Callable[
        ['Loader'], list[ComponentData]]:
        def wrapper(self: 'Loader') -> list[ComponentData]:
            components_list: list[ComponentData] = func(self)
            for component in components_list:
                component.data.chineseNameShort = None
                component.data.chineseName = self.localization.get_vehicle_name(component.localName)
                component.data.chineseDescription = None
                if component.data.manufacturerData:
                    component.data.manufacturerData.data.chineseName = self.localization.get_manufacturer_name(
                        component.data.manufacturerData.data.calculatorName,
                        component.data.manufacturerData.data.nameSmall,
                        component.data.chineseDescription)
            return components_list

        return wrapper


    @translate_component
    def load_missiles(self) -> list[Missile]:
        with open(self.missile_path, "r") as f:
            data = json.load(f)
        return [Missile(**d) for d in data]

    @translate_component
    def load_bombs(self) -> list[Bomb]:
        with open(self.bomb_path, "r") as f:
            data = json.load(f)
        return [Bomb(**d) for d in data]

    @translate_component
    def load_shields(self) -> list[Shield]:
        with open(self.shield_path, "r") as f:
            data = json.load(f)
        for d in data:
            d['data']['itemClass'] = d['data']['class']
        return [Shield(**d) for d in data]

    @translate_component
    def load_coolers(self) -> list[Cooler]:
        with open(self.cooler_path, "r") as f:
            data = json.load(f)
        for d in data:
            d['data']['itemClass'] = d['data']['class']
        return [Cooler(**d) for d in data]

    @translate_component
    def load_weapons(self) -> list[Weapon]:
        with open(self.weapon_path, "r") as f:
            data = json.load(f)
        return [Weapon(**d) for d in data]

    @translate_component
    def load_emps(self) -> list[EMP]:
        with open(self.emp_path, "r") as f:
            data = json.load(f)
        return [EMP(**d) for d in data]

    @translate_component
    def load_mining_lasers(self) -> list[MiningLaser]:
        with open(self.mining_laser_path, "r") as f:
            data = json.load(f)
        return [MiningLaser(**d) for d in data]

    @translate_component
    def load_mounts(self) -> list[Mount]:
        with open(self.mount_path, "r") as f:
            data = json.load(f)
        return [Mount(**d) for d in data]

    @translate_component
    def load_power_plants(self) -> list[PowerPlant]:
        with open(self.power_plant_path, "r") as f:
            data = json.load(f)
        for d in data:
            if 'class' in d['data']:
                d['data']['itemClass'] = d['data']['class']
        return [PowerPlant(**d) for d in data]

    @translate_component
    def load_qdrives(self) -> list[QDrive]:
        with open(self.qdrive_path, "r") as f:
            data = json.load(f)
        for d in data:
            if 'class' in d['data']:
                d['data']['itemClass'] = d['data']['class']
        return [QDrive(**d) for d in data]

    @translate_component
    def load_qeds(self) -> list[Qed]:
        with open(self.qed_path, "r") as f:
            data = json.load(f)
        for d in data:
            if 'class' in d['data']:
                d['data']['itemClass'] = d['data']['class']
        return [Qed(**d) for d in data]

    @translate_component
    def load_utilities(self) -> list[Utility]:
        with open(self.utility_path, "r") as f:
            data = json.load(f)
        return [Utility(**d) for d in data]

    @translate_component
    def load_paints(self) -> list[Paint]:
        with open(self.paint_path, "r") as f:
            data = json.load(f)
        return [Paint(**d) for d in data]

    @translate_vehicle
    def load_ships(self) -> list[Ship]:
        with open(self.ship_path, "r") as f:
            data = json.load(f)
        return [Ship(**d) for d in data]

    @translate_component
    def load_missile_racks(self) -> list[MissileRack]:
        with open(self.missile_rack_path, "r") as f:
            data = json.load(f)
        return [MissileRack(**d) for d in data]

    def load_shops(self) -> list[Shop]:
        with open(self.shop_path, "r") as f:
            data = json.load(f)
        shops: list[Shop] = [Shop(**d) for d in data]
        for shop in shops:
            shop.data.nameChinese = self.localization.get_translation(shop.data.name)
            shop.data.locationChinese = self.localization.get_translation(shop.data.location)
        return shops

    def load_all(self):
        self.weapons = self.load_weapons()
        self.missiles = self.load_missiles()
        self.ships = self.load_ships()
        self.shops = self.load_shops()
        self.bombs = self.load_bombs()
        self.shields = self.load_shields()
        self.coolers = self.load_coolers()
        self.emps = self.load_emps()
        self.mining_lasers = self.load_mining_lasers()
        self.mounts = self.load_mounts()
        self.power_plants = self.load_power_plants()
        self.qdrives = self.load_qdrives()
        self.qeds = self.load_qeds()
        self.utilities = self.load_utilities()
        self.paints = self.load_paints()
        self.missile_racks = self.load_missile_racks()


if __name__ == "__main__":
    loader = Loader()
    with open("test_data.json", "w") as f:
        json.dump(loader.qdrives[1].dict(), f, indent=4, ensure_ascii=False)
    a = 1
