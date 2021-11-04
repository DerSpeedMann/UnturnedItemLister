import os
import re

from Item import Item
from NpcStuff.NpcElement import NpcElement
from NpcStuff.Quest.Condition import Condition
from NpcStuff.Npc import Npc
from NpcStuff.Quest.Quest import Quest
from NpcStuff.Quest.Reward import Reward
from NpcStuff.Trade.Trade import Trade
from NpcStuff.Trade.VendorMenu import VendorMenu


def remove_tags(data):
    return re.sub(r'<.*?>', '', data)


def parse_stat_value(line):
    strings = line.split()
    if len(strings) >= 2:
        return strings[1]
    return strings[0]


def parse_stat_string(line):
    strings = line.split()
    if len(strings) >= 1:
        return line[len(strings[0]) + 1:-1]
    return "True"


def parse_condition(condition: str):
    switcher = {
        "Equal": "=",
        "Greater_Than_Or_Equal_To": ">=",
        "Smaller_Than_Or_Equal_To": "<=",
        "Greater": ">",
        "Smaller": "<",
        "Not_Equal": "!="
    }
    if condition in switcher:
        return switcher[condition]
    else:
        return switcher["Equal"]


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError or TypeError:
        return False


def represents_float(s):
    try:
        float(s)
        return True
    except ValueError or TypeError:
        return False


def get_stat_function(item: Item, stat: str):
    if item.get_stat(stat) is None:
        return 0
    else:
        return item.get_stat(stat)


class Reader:
    def __init__(self,
                 unturned_bundle_location: str,
                 ignored_stats_by_item_type: [str, [str]],
                 read_types: [str, bool] = None,
                 items_dict: [str, [int, Item]] = None,
                 npc_dict: [int, Npc] = None):

        if items_dict is None:
            items_dict = {}
        if npc_dict is None:
            npc_dict = {}
        if read_types is None:
            read_types = {}

        self.bundle: str = unturned_bundle_location
        self.ignoredStatNamesByType: [str, bool] = ignored_stats_by_item_type
        self.readTypes: [str, bool] = read_types
        self.itemsDict: [str, [int, Item]] = items_dict
        self.npcDict: [int, Npc] = npc_dict
        self.questDict: [int, Quest] = {}
        self.sortedItemIds: [str, [int]] = {}

        self.ignoredFiles = ["English.dat", "Russian.dat",
                             "Bounds.dat", "Flags.dat", "Lighting.dat", "Navigation_", "Nodes.dat", "Paths.dat",
                             "Objects.dat", "Animals.dat", "Fauna.dat", "Items.dat", "Jars.dat", "Players.dat",
                             "Vehicles.dat", "Zombies.dat", "Details.dat", "Materials.dat", "Resources.dat",
                             "Trees.dat", "Roads.dat", "Buildables.dat", "Trees.dat", "Roads.dat", "Camera.dat",
                             "Level.dat", "Height.dat", "Spawns.dat", "Flags_Data.dat", "Visibility.dat",
                             "Heights.dat", "MasterBundle.dat"]
        self.itemNameFile = "English.dat"
        self.npcClass = "NPC"
        self.vendorClass = "Vendor"
        self.questClass = "Quest"
        self.dialogueClass = "Dialogue"
        self.error_item_name_file = False
        self.error_duplicate_item = False
        self.info_duplicate_quest = False

    def iterate_folders(self, path: str):
        for entry in os.listdir(path):
            new_path = path + '/' + entry
            if os.path.isdir(new_path):
                self.iterate_folders(new_path)
            else:
                self.read_file(path, entry)

    def read_items(self):
        self.iterate_folders(self.bundle)

    def read_file(self, path: str, filename: str):
        if not self.ignore_file(filename):
            # open file
            try:
                os.chdir(path)
                with open(filename, 'rt') as f:
                    data = f.readlines()
                    item_filename = os.path.splitext(filename)[0]
                    new_item = Item(item_filename)

                    # parse file
                    for line in data:
                        if new_item.is_valid_item():

                            # check extra item stats
                            if len(line) > 2:
                                failed = False

                                if new_item.itemType in self.ignoredStatNamesByType:
                                    for ignored_stat_name in self.ignoredStatNamesByType[new_item.itemType]:
                                        if line.startswith(ignored_stat_name):
                                            failed = True
                                            break
                                if not failed:
                                    new_item.add_stat(line.split()[0], parse_stat_value(line))
                            else:
                                continue
                        else:
                            # check main item stats
                            if line.startswith("Type "):
                                new_item.set_item_type(parse_stat_value(line))
                                # skip file if item type is ignored
                                if new_item.itemType in self.readTypes \
                                        and not self.readTypes[new_item.itemType]:
                                    return

                            elif line.startswith("ID "):
                                new_item.set_item_id(parse_stat_value(line))

                self.parse_item_name_and_desc(path, new_item)

                self.insert_item(new_item)

            except (IOError, UnicodeDecodeError):
                print("ERR: Item file " + filename + " could not be opened in: " + path)
            finally:
                f.close()

    def insert_item(self, item: Item):
        # push if item is valid
        if item.is_valid_item():
            if item.itemType in self.itemsDict:
                if item.id in self.itemsDict[item.itemType]:
                    if self.error_duplicate_item:
                        print("ERR: Found duplicate item: "
                              "[ID:" + str(item.id) + " Filename:" + item.fileName +
                              " Itemname:" + item.itemName + "]")
                else:
                    self.itemsDict[item.itemType][item.id] = item
            else:
                self.itemsDict[item.itemType] = {item.id: item}

    def ignore_file(self, filename: str) -> bool:
        if filename.endswith(".dat"):
            for ignored_file in self.ignoredFiles:
                if filename.startswith(ignored_file):
                    return True
            return False
        return True

    def parse_item_name_and_desc(self, path: str, item: Item):
        # open file
        try:
            f = None
            os.chdir(path)
            with open(self.itemNameFile, 'rt') as f:
                data = f.readlines()
                for line in data:
                    if line.startswith("Name "):
                        item.set_item_name(remove_tags(parse_stat_string(line)))
                    if line.startswith("Description "):
                        item.set_item_desc(remove_tags(parse_stat_string(line)))

        except IOError:
            if self.error_item_name_file:
                print("ERR: Item-Name file for " + item.fileName + " could not be opened in: " + path)

        finally:
            if f is not None:
                f.close()

    def parse_npc_dialogues(self):
        if self.npcClass in self.itemsDict:
            for npc_id, npc_item in self.itemsDict[self.npcClass].items():
                parent_dialogues = []
                self.npcDict[npc_id] = Npc(npc_id, npc_item.itemName, npc_item.itemDescription)
                dialogue_id = npc_item.get_stat("Dialogue")
                if dialogue_id is not None:
                    if str(dialogue_id) in self.itemsDict[self.dialogueClass]:
                        self.parse_dialogue_inner(parent_dialogues, npc_id,
                                                  self.itemsDict[self.dialogueClass][str(dialogue_id)])
                    else:
                        print("ERR: Dialogue with ID:" + str(dialogue_id) + " not parsed")
        else:
            print("ERR: Dialogues not parsed")

    def parse_dialogue_inner(self, parent_dialogue_ids: [int], npc_id: int, dialogue_item: Item) -> [NpcElement]:
        dialogue_iterator = 0
        dialogue_elements = []

        while True:
            found_new = False
            last_added = []
            # check for vendor menu
            vendor_id = dialogue_item.get_stat("Response_" + str(dialogue_iterator) + "_Vendor")
            if vendor_id is not None:
                found_new = True
                returned_element = self.parse_vendor(npc_id, int(vendor_id))
                if returned_element is not None:
                    last_added.extend([returned_element])
                    dialogue_elements.extend(last_added)
                else:
                    last_added = []

            # check for quest
            quest_id = dialogue_item.get_stat("Response_" + str(dialogue_iterator) + "_Quest")
            if quest_id is not None:
                found_new = True
                returned_element = self.parse_quest(npc_id, int(quest_id))
                if returned_element is not None:
                    last_added.extend([returned_element])
                    dialogue_elements.extend(last_added)
                else:
                    last_added = []

            # check for dialogue
            dialogue_id = dialogue_item.get_stat("Response_" + str(dialogue_iterator) + "_Dialogue")
            if dialogue_id is not None:
                found_new = True
                is_loop = False
                for parent_dialogue in parent_dialogue_ids:
                    if dialogue_id == parent_dialogue:
                        is_loop = True
                        break
                if not is_loop:
                    if str(dialogue_id) in self.itemsDict[self.dialogueClass]:
                        parent_dialogue_ids.append(dialogue_id)
                        last_added.extend(
                            self.parse_dialogue_inner(
                                parent_dialogue_ids, npc_id,
                                self.itemsDict[self.dialogueClass][str(dialogue_id)]))
                        dialogue_elements.extend(last_added)
                    else:
                        print("ERR: Dialogue with ID:" + str(dialogue_id) + " not parsed")

            # check for conditions
            condition_type = dialogue_item.get_stat("Response_" + str(dialogue_iterator) + "_Condition_0_Type")
            if condition_type is not None:
                found_new = True
                quest_components = ["Response_" + str(dialogue_iterator) + "_Condition_"]
                quest = self.parse_quest_inner(dialogue_item, Quest(0), quest_components)
                for element in last_added:
                    element.add_requirements(quest.conditions)

            # check if any new elements where found
            if not found_new:
                break
            dialogue_iterator += 1
        return dialogue_elements

    def parse_quest(self, npc_id: int, quest_id: int):
        if self.questClass in self.itemsDict and str(quest_id) in self.itemsDict[self.questClass]:
            quest_item = self.itemsDict[self.questClass][str(quest_id)]
            quest = Quest(quest_id, quest_item.itemName, quest_item.itemDescription)

            quest_components = ["Condition_", "Reward_"]
            quest = self.parse_quest_inner(quest_item, quest, quest_components)
            self.npcDict[npc_id].add_quest(quest)
            if quest.id in self.questDict:
                if self.info_duplicate_quest:
                    print("INFO: Quest with ID: " + str(quest.id) + " already parsed")
            else:
                self.questDict[quest.id] = quest
            return quest
        else:
            print("ERR: Quest with ID:" + str(quest_id) + " not parsed or no Quests parsed")
            return None

    def parse_quest_inner(self, quest_item: Item, quest: Quest, quest_components: [str]):

        for trade_type in quest_components:
            iterator = 0
            while True:
                component_type = quest_item.get_stat(trade_type + str(iterator) + "_Type")
                logic = quest_item.get_stat(trade_type + str(iterator) + "_Logic")
                value = quest_item.get_stat(trade_type + str(iterator) + "_Value")
                component_id = quest_item.get_stat(trade_type + str(iterator) + "_ID")
                amount = quest_item.get_stat(trade_type + str(iterator) + "_Amount")
                status = quest_item.get_stat(trade_type + str(iterator) + "_Status")

                component_name = ""
                if component_type is not None:
                    if component_type == "Item":
                        item = self.get_item_by_id(component_id)

                        if item is None:
                            print("ERR: Item with ID: " + str(component_id) + " not parsed")
                        else:
                            component_name = item.itemName

                    if component_type == "Quest":
                        inner_quest_item = self.get_item_by_id(component_id)

                        if inner_quest_item is None:
                                print("ERR: Quest with ID: " + str(component_id) + " not parsed")
                        else:
                            component_name = inner_quest_item.itemName

                    if amount is not None:
                        value = amount
                    if status is not None:
                        value = status
                    if trade_type == quest_components[0]:
                        quest.add_condition(Condition(component_type, value, logic, component_id, component_name))
                    else:
                        quest.add_reward(Reward(component_type, value, logic, component_id, component_name))
                else:
                    break
                iterator += 1

        return quest

    def parse_vendor(self, npc_id: int, vendor_id: int):
        if self.vendorClass in self.itemsDict and str(vendor_id) in self.itemsDict[self.vendorClass]:
            vendor_item = self.itemsDict[self.vendorClass][str(vendor_id)]
            vendor_menu = VendorMenu(vendor_id, vendor_item.itemName, vendor_item.itemDescription)

            trade_types = ["Buying_", "Selling_"]
            for trade_type in trade_types:
                iterator = 0
                while True:
                    item_id = vendor_item.get_stat(trade_type + str(iterator) + "_ID")
                    price = vendor_item.get_stat(trade_type + str(iterator) + "_Cost")
                    condition_type = vendor_item.get_stat(trade_type + str(iterator) + "_Condition_0_Type")

                    if item_id is not None and price is not None:
                        item = self.get_item_by_id(item_id)
                        item_name = ""
                        slot_price = 0.0

                        if item is None:
                            print("ERR: item with ID: " + str(item_id) + " not parsed")
                        else:
                            item_name = item.itemName
                            size_x = item.get_stat("Size_X")
                            size_y = item.get_stat("Size_Y")
                            if size_x is not None and size_y is not None:
                                slot_price = price / (size_x * size_y)

                        trade = Trade(item_id, price, slot_price, item_name)
                        if condition_type is not None:
                            quest_components = [trade_type + str(iterator) + "_Condition_"]
                            quest = self.parse_quest_inner(vendor_item, Quest(0), quest_components)
                            trade.add_requirements(quest.conditions)

                        if trade_type == trade_types[0]:
                            vendor_menu.add_bought_item(trade)
                        else:
                            vendor_menu.add_sold_item(trade)
                    else:
                        break
                    iterator += 1

            self.npcDict[npc_id].add_vendor_menu(vendor_menu)
            return vendor_menu
        else:
            print("ERR: Vendor with ID:" + str(vendor_id) + " not parsed or no Vendors parsed")

    def get_item_by_id(self, item_id: int):
        for item_class in self.itemsDict:
            if str(item_id) in self.itemsDict[item_class]:
                return self.itemsDict[item_class][str(item_id)]
        return None

    def print_sorted_npc_buys(self, reverse=True):
        sorted_trades = []
        for npc_id, npc in self.npcDict.items():
            for menu_id, vendor_menu in npc.vendorMenus.items():
                for trade_id, trade in vendor_menu.buys.items():
                    trade.MenuName = vendor_menu.menuName
                    sorted_trades.append(trade)

        sorted_trades.sort(key=lambda x: x.slotPrice, reverse=reverse)
        print("####################################\n\r"
              "Item Prices per Slot: \n\r"
              "####################################\n\r")
        for trade in sorted_trades:
            print(trade)

    def calc_stat(self, item_classes: [str], new_stat_name: str, stat_names: [str], calculation: {}, all_required=True):

        for item_class in item_classes:
            if item_class in self.itemsDict:
                for item_id, chosen_item in self.itemsDict[item_class].items():

                    result = None
                    for stat_name in stat_names:

                        stat = chosen_item.get_stat(stat_name)
                        if stat is not None:
                            if result is None:
                                result = stat
                            else:
                                result = calculation(result, stat)
                        elif all_required:
                            break

                    if result is not None:
                        chosen_item.add_stat(new_stat_name, result)

    def remove_empty_npcs(self):
        removed_npc_ids = []
        for npc_id, npc in self.npcDict.items():
            if len(npc.vendorMenus) <= 0 and len(npc.quests) <= 0:
                removed_npc_ids.append(npc_id)
        for npc_id in removed_npc_ids:
            self.npcDict.pop(str(npc_id))

    def sort_npc_vendors(self):
        for npc_id, npc in self.npcDict.items():
            npc.sort_traders()

    def sort_items(self, sorted_classes: [str], sorted_stat: str, reverse=False):
        for class_name in sorted_classes:
            if class_name in self.itemsDict:
                if class_name not in self.sortedItemIds:
                    self.sortedItemIds[class_name] = []
                    for item_id in self.itemsDict[class_name]:
                        self.sortedItemIds[class_name].append(item_id)

                self.sortedItemIds[class_name].sort(
                    key=lambda x: get_stat_function(self.itemsDict[class_name][x], sorted_stat), reverse=reverse)

    def remove_items_by_stat(self, classes: [str], stat: str, condition: {}):
        for class_name in classes:
            if class_name in self.itemsDict:
                removed = []
                for item_id in self.itemsDict[class_name]:
                    if stat == "itemName" and condition(self.itemsDict[class_name][item_id].itemName):
                        removed.append(item_id)
                    else:
                        if condition(self.itemsDict[class_name][item_id].get_stat(stat)):
                            removed.append(item_id)

                for item_id in removed:
                    self.itemsDict[class_name].pop(item_id)

    def print_items(self, printed_types: [str, bool]):
        for item_type in self.itemsDict:
            # skip if item type is ignored
            if item_type in printed_types \
                    and not printed_types[item_type]:
                continue
            print("####################################\n\r"
                  + item_type + "\n\r"
                                "####################################\n\r")
            if item_type in self.sortedItemIds:
                for item_id in self.sortedItemIds[item_type]:
                    print(self.itemsDict[item_type][item_id])

            else:
                for item_id, chosen_item in self.itemsDict[item_type].items():
                    print(chosen_item)

    def print_npcs(self, quests=True, buys=True, sells=True, shop_requirements=True,
                   item_requirements=True, item_vendor_name=True):
        print("####################################\n\r"
              "Prepared NPCs\n\r"
              "####################################\n\r")
        for npc_id, npc in self.npcDict.items():
            print(npc.get_print_string(quests, buys, sells, shop_requirements,
                                       item_requirements, item_vendor_name))
