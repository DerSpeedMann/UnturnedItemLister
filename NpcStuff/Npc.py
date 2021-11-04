from NpcStuff.Quest.Quest import Quest
from NpcStuff.Trade.VendorMenu import VendorMenu


class Npc:
    def __init__(self, npc_id: int, name: str, description: str):
        self.id: int = npc_id
        self.name: str = name
        self.description: str = description
        self.vendorMenus: [str, VendorMenu] = {}
        self.quests: [str, Quest] = {}

        self.info_duplicate_vendor_menu = False
        self.info_duplicate_quest = False

    def __repr__(self):
        return self.get_print_string()

    def get_print_string(self, quests=True, buys=True, sells=True, shop_requirements=True,
                         item_requirements=True, item_vendor_name=True) -> str:
        return_string = self.name + "\n\r"
        return_string += "  " + self.description + "\n\r"
        return_string += "  " + "ID: " + str(self.id) + "\n\r"

        if len(self.vendorMenus) >= 1:
            return_string += "   Shops: \n\r"

            for menu_id, vendor_menu in self.vendorMenus.items():
                return_string += vendor_menu.get_print_string(buys, sells, shop_requirements,
                                                              item_requirements, item_vendor_name)

        if quests and len(self.quests) >= 1:
            return_string += "   Quests: \n\r"

            for quest_id, quest in self.quests.items():
                return_string += str(quest)

        return return_string

    def add_vendor_menu(self, menu: VendorMenu):
        if menu.id in self.vendorMenus:
            if self.info_duplicate_vendor_menu:
                print("INFO: Vendor Menu with ID: " + str(menu.id) + " already added to Trader: " + str(self.id))
        else:
            self.vendorMenus[menu.id] = menu

    def add_quest(self, quest: Quest):
        if quest.id in self.quests:
            if self.info_duplicate_quest:
                print("INFO: Quest with ID: " + str(quest.id) + " already added to Trader: " + str(self.id))
        else:
            self.quests[quest.id] = quest

    def sort_traders(self, reverse=True):
        self.sort_buys(reverse)
        self.sort_sells(reverse)

    def sort_buys(self, reverse=True):
        for item_id, vendor_menu in self.vendorMenus.items():
            for trade_id in vendor_menu.buys:
                vendor_menu.sortedBuyIds.append(trade_id)
            vendor_menu.sortedBuyIds.sort(key=lambda x: vendor_menu.buys[x].slotPrice, reverse=reverse)

    def sort_sells(self, reverse=True):
        for item_id, vendor_menu in self.vendorMenus.items():
            for menu_id in vendor_menu.sells:
                vendor_menu.sortedSellIds.append(menu_id)
            vendor_menu.sortedSellIds.sort(key=lambda x: vendor_menu.sells[x].slotPrice, reverse=reverse)
