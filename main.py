# !/usr/bin/env python3
import sqlite3
from Reader import Reader

unturnedBundle = 'F:/Program Files (x86)/Steam/SteamApps/common/Unturned/Bundles/Items'

unturnedModFolder = 'F:/Program Files (x86)/Steam/SteamApps/workshop/content/304930/'

russiaPlus = {"Russia+": "2475218356"}

Arid = {"Arid": "2683620106"}

clothes = ["Hat", "Mask", "Vest", "Shirt", "Pants", "Backpack", "Glasses"]
attachments = ["Tactical", "Sight", "Grip", "Barrel", "Magazine"]
weapons = ["Gun", "Melee", "Throwable"]
meds = ["Medical"]
structs = ["Storage", "Barricade"]
vehicles = ["Vehicle"]
npcs = ["NPC", "Vendor", "Quest", "Dialogue"]

ignored_stats = ["//", "Rarity", "GUID", "Useable", "Size_Z", "Size2_",
                 "Blueprint", "Exclude_From_Master_Bundle", "Asset_Bundle_Version", "Master_Bundle_Override"]
ignore_clothe_stats = ignored_stats + ["Beard", "Hair", "Quality_"]
ignore_attachment_stats = ignored_stats + ["Count_", "Tracer", "Use_Auto_Icon_Measurements", "Paintable",
                                           "Holographic"]
ignore_weapon_stats = ignored_stats + ["AttackAudioClip", "Zombie_", "Animal_", "Barricade_", "Structure_", "Vehicle_",
                                       "Resource_", "Object_", "Explosion", "Ammo_"]
ignore_struct_stats = ignored_stats + ["Build", "Range", "Radius", "Offset", "Explosion"]
ignore_med_stats = ignored_stats + []
ignore_vehicle_stats = ignored_stats + []
ignore_npc_stats = ignored_stats + ["Selling ", "Buying ", "Disable_Sorting",
                                    "Backpack", "Shirt", "Pants", "Hat", "Face", "Glasses", "Vest", "Mask",
                                    "Primary", "Secondary",
                                    "Beard", "Hair", "Color_Skin", "Color_Hair", "Pose", ]

# every type is read except the ones set to False
read_types_items_only = {"Grower": True, "Sentry": True, "Tank": True, "Trap": True,
                         "Oil_Pump": True, "Library": True, "Generator": True, "Beacon": True,
                         "Resource": False, "Effect": False, "Cloud": False, "Decal": False,
                         "Large": False, "Medium": False, "Small": False, "Structure": True,
                         "Barricade": True, "Storage": True,

                         "NPC": True, "Vendor": True, "Quest": True, "Dialogue": True, "Spawn": False,
                         "Water": False, "Supply": True, "Food": True, "Refill": False, "Farm": False,

                         "Vehicle_Repair_Tool": True, "Fuel": False, "Tire": False, "Tool": True,
                         "Arrest_Start": False, "Arrest_End": False,
                         "Filter": True, "Detonator": True, "Box": False, "Charge": True,
                         "Compass": True, "Optic": True, "Map": True, "Key": False, "Fisher": True,

                         "Hat": True, "Mask": True, "Glasses": True, "Vest": True, "Backpack": True,
                         "Shirt": True, "Pants": True,

                         "Animal": False, "Vehicle": False,
                         "Gun": True, "Throwable": True, "Melee": True,
                         "Grip": True, "Tactical": True, "Barrel": True, "Sight": True, "Magazine": True,
                         "Medical": True}

# every type is read except the ones set to False
read_types = {"Grower": True, "Sentry": True, "Tank": True, "Trap": True,
                         "Oil_Pump": True, "Library": True, "Generator": True, "Beacon": True,
                         "Resource": False, "Effect": False, "Cloud": False, "Decal": False,
                         "Large": False, "Medium": False, "Small": False, "Structure": True,
                         "Barricade": True, "Storage": True,

                         "NPC": True, "Vendor": True, "Quest": True, "Dialogue": True, "Spawn": False,
                         "Water": False, "Supply": True, "Food": True, "Refill": False, "Farm": False,

                         "Vehicle_Repair_Tool": True, "Fuel": False, "Tire": False, "Tool": True,
                         "Arrest_Start": False, "Arrest_End": False,
                         "Filter": True, "Detonator": True, "Box": False, "Charge": True,
                         "Compass": True, "Optic": True, "Map": True, "Key": False, "Fisher": True,

                         "Hat": True, "Mask": True, "Glasses": True, "Vest": True, "Backpack": True,
                         "Shirt": True, "Pants": True,

                         "Animal": False, "Vehicle": False,
                         "Gun": True, "Throwable": True, "Melee": True,
                         "Grip": True, "Tactical": True, "Barrel": True, "Sight": True, "Magazine": True,
                         "Medical": True}

# every type is printed except the ones set to False
printed_types = {"Grower": False, "Sentry": False, "Tank": False, "Trap": False,
                 "Oil_Pump": False, "Library": False, "Generator": False, "Beacon": False,
                 "Resource": False, "Effect": False, "Cloud": False, "Decal": False,
                 "Large": False, "Medium": False, "Small": False, "Structure": False,
                 "Barricade": False, "Storage": False,

                 "NPC": False, "Vendor": False, "Quest": False, "Dialogue": False,
                 "Spawn": False,
                 "Water": False, "Supply": False, "Food": False, "Refill": False, "Farm": False,

                 "Vehicle_Repair_Tool": False, "Fuel": False, "Tire": False, "Tool": False,
                 "Arrest_Start": False, "Arrest_End": False,
                 "Filter": False, "Detonator": False, "Box": False, "Charge": False,
                 "Compass": False, "Optic": False, "Map": False, "Key": False, "Fisher": False,

                 "Hat": True, "Mask": True, "Glasses": False, "Vest": True, "Backpack": False,
                 "Shirt": False, "Pants": False,

                 "Animal": False, "Vehicle": False,
                 "Gun": True, "Throwable": False, "Melee": False,
                 "Grip": False, "Tactical": False, "Barrel": False, "Sight": False,
                 "Magazine": False,
                 "Medical": False}

ignored_stats_by_item_type = {
    clothes[0]: ignore_clothe_stats,
    clothes[1]: ignore_clothe_stats,
    clothes[2]: ignore_clothe_stats,
    clothes[3]: ignore_clothe_stats,
    clothes[4]: ignore_clothe_stats,
    clothes[5]: ignore_clothe_stats,
    clothes[6]: ignore_clothe_stats,
    attachments[0]: ignore_attachment_stats,
    attachments[1]: ignore_attachment_stats,
    attachments[2]: ignore_attachment_stats,
    attachments[3]: ignore_attachment_stats,
    attachments[4]: ignore_attachment_stats,
    weapons[0]: ignore_weapon_stats,
    weapons[1]: ignore_weapon_stats,
    weapons[2]: ignore_weapon_stats,
    meds[0]: ignore_med_stats,
    structs[0]: ignore_struct_stats,
    structs[1]: ignore_struct_stats,
    vehicles[0]: ignore_vehicle_stats,
    npcs[0]: ignore_npc_stats,
    npcs[1]: ignore_npc_stats,
    npcs[2]: ignore_npc_stats,
    npcs[3]: ignore_npc_stats
}


def load_items(mods=None, items_dict=None):
    if items_dict is None:
        items_dict = {}
    if mods is None:
        mods = {}

    if len(mods) >= 1:
        for mod in list(mods.values()):
            bundle = unturnedModFolder + mod
            reader = Reader(bundle, ignored_stats_by_item_type, read_types_items_only, items_dict)
            reader.read_items()
    else:
        reader = Reader(unturnedBundle, ignored_stats_by_item_type, read_types_items_only, items_dict)
        reader.read_items()


def sort_items(reader):
    reader.calc_stat(["Vest", "Shirt", "Pants", "Backpack"], "Space", ["Width", "Height"], lambda x, y: x * y, True)

    reader.sort_items(clothes, "Armor_Explosion")
    reader.sort_items(clothes, "Space", True)
    reader.sort_items(clothes, "Armor")

    reader.sort_items([attachments[1]], "Zoom")

    reader.sort_items([attachments[2]], "Recoil_X")
    reader.sort_items([attachments[2]], "Recoil_Y")

    reader.sort_items([weapons[1]], "Range", True)
    reader.sort_items([weapons[1]], "Player_Damage", True)

    reader.calc_stat(structs, "Space", ["Storage_X", "Storage_Y"], lambda x, y: x * y, True)

    reader.sort_items(structs, "Health", True)
    reader.sort_items(structs, "Space", True)


def list_items(mods=None, items_dict=None, reader=None):
    if items_dict is None:
        items_dict = {}
    if mods is None:
        mods = {}

    if len(mods) >= 1:
        for mod in list(mods.values()):
            bundle = unturnedModFolder + mod
            reader = Reader(bundle, ignored_stats_by_item_type, read_types, items_dict)
            reader.read_items()
    else:
        reader = Reader(unturnedBundle, ignored_stats_by_item_type, read_types, items_dict)
        reader.read_items()

    reader.remove_items_by_stat(["Throwable"], "Player_Damage", lambda x: x is None)  # removes Throwable with no damage
    reader.remove_items_by_stat(["Hat", "Mask", "Vest", "Pants", "Shirt"], "Armor", lambda x: x is None)  # removes Clothing with no armor
    reader.remove_items_by_stat(["Quest"], "itemName", lambda x: x == "")  # removes quests with no name

    reader.parse_npc_dialogues()

    reader.remove_empty_npcs()
    reader.sort_npc_vendors()

    sort_items(reader)
    reader.print_items(printed_types)

    reader.print_npcs(quests=True, buys=True, sells=True, shop_requirements=True,
                      item_requirements=True, item_vendor_name=True)
    # reader.print_sorted_npc_buys()


def create_table(fields):
    conn = sqlite3.connect('your_database.db')
    c = conn.cursor()

    # Define common fields
    common_fields = "ID INTEGER PRIMARY KEY, CommonField1 TEXT NOT NULL, CommonField2 INTEGER NOT NULL"

    # Define optional fields dynamically based on input
    optional_fields = ", ".join([f"{field} TEXT" for field in fields])

    # Create table with common and optional fields
    c.execute(f"CREATE TABLE YourTable ({common_fields}, {optional_fields})")

    conn.commit()
    conn.close()

# Example usage
fields_to_add = ['OptionalField1', 'OptionalField2']
create_table(fields_to_add)

# TODO: Implement spawn_tables
# TODO: Implement script to see all quest required to unlock all traders (find quest with flag reward)
# TODO: Check quest falgs not printing correctly
# TODO: Implement commands to allow printing needed category on demand

global_items_dict = {}
# list_items(wykletyMods)

# load items from main game
# load_items({}, global_items_dict)
# load item bundles
# load_items(fenixItemBundles, global_items_dict)
# load_items(russiaPlus, global_items_dict)

# list_items(russiaPlus, global_items_dict)

load_items(Arid, global_items_dict)
list_items(Arid, global_items_dict)