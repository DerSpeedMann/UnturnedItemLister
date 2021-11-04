from NpcStuff.NpcElement import NpcElement
from NpcStuff.Trade.Trade import Trade


class VendorMenu(NpcElement):
    def __init__(self, menu_id: int, menu_name: str, menu_description: str):
        super().__init__()
        self.id: int = menu_id
        self.menuName: str = menu_name
        self.menuDescription: str = menu_description

        self.sortedSellIds: [int] = []
        self.sortedBuyIds: [int] = []
        self.sells: [str, Trade] = {}
        self.buys: [str, Trade] = {}
        self.error_duplicate_sells = False
        self.error_duplicate_buys = False

    def __repr__(self):
        return self.get_print_string()

    def get_print_string(self, buys=True, sells=True, shop_requirements=True,
                         item_requirements=True, item_vendor_name=True) -> str:
        return_string = "    " + self.menuName + " [" + str(self.id) + "]\n\r"
        return_string += "     " + self.menuDescription + "\n\r"
        if shop_requirements and len(self.requirements) >= 1:
            return_string += "    Requires: \n\r"
            for requirement in self.requirements:
                return_string += str(requirement)
        if buys and len(self.buys) >= 1:
            return_string += "    Buying: \n\r"
            if len(self.sortedBuyIds) > 0:
                for item_id in self.sortedBuyIds:
                    return_string += self.buys[item_id].get_print_string(item_requirements, item_vendor_name)
            else:
                for item_id, bought_item in self.buys.items():
                    return_string += str(bought_item)

        if sells and len(self.sells) >= 1:
            return_string += "    Selling: \n\r"
            if len(self.sortedSellIds) > 0:
                for item_id in self.sortedSellIds:
                    return_string += str(self.sells[item_id])
            else:
                for item_id, sold_item in self.sells.items():
                    return_string += str(sold_item)

        return return_string + "\n\r"

    def add_bought_item(self, trade: Trade):
        if trade.itemId in self.buys:
            if self.error_duplicate_buys:
                print("ERR: item " + str(trade.itemName) + " [" + str(trade.itemId) + "] is already bought by trader")
            if trade.itemPrice >= self.buys[trade.itemId].itemPrice:
                return
        self.buys[trade.itemId] = trade

    def add_sold_item(self, trade: Trade):
        if trade.itemId in self.sells:
            if self.error_duplicate_sells:
                print("ERR: item " + str(trade.itemName) + "[" + str(trade.itemId) + "] is already sold by trader")
            if trade.itemPrice <= self.sells[trade.itemId].itemPrice:
                return
        self.sells[trade.itemId] = trade
