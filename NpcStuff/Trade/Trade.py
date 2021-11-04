from NpcStuff.NpcElement import NpcElement


class Trade(NpcElement):
    def __init__(self, item_id: int, item_price="", slot_price=0.0, item_name=""):
        super().__init__()
        self.itemId: int = item_id
        self.itemPrice: int = item_price
        self.slotPrice: int = slot_price
        self.menuName: str = ""
        self.itemName: str = item_name

    def __repr__(self):
        return self.get_print_string()

    def get_print_string(self, item_requirements=True, item_vendor_name=True) -> str:
        return_string = "      " + self.itemName + " [" + str(self.itemId) + "]\n\r"
        return_string += "       Price     : " + str(self.itemPrice) + "\n\r"
        return_string += "       Slot Price: " + str(self.slotPrice) + "\n\r"
        if item_requirements and len(self.requirements) >= 1:
            return_string += "       Requires: \n\r"
            for requirement in self.requirements:
                return_string += str(requirement)
        if item_vendor_name and self.menuName != "":
            return_string += "       Vendor Menu: [" + self.menuName + "]"
        return return_string
