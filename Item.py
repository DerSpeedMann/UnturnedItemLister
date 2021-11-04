import Reader


class Item:
    def __init__(self, file_name: str):
        self.fileName: str = file_name
        self.itemName: str = ""
        self.itemDescription: str = ""
        self.itemType: str = ""
        self.id: int = 0
        self.stats: [str, str] = {}

    def __repr__(self):
        return_string = self.itemName + " [" + self.fileName + "]\n\r"
        return_string += "  " + self.itemDescription + "\n\r"
        if self.is_valid_item:
            return_string += "  " + "ID: " + str(self.id) + "\n\r"
            return_string += "  " + "Type: " + str(self.itemType) + "\n\r"

        for stat in self.stats:
            return_string += "  " + stat + ": " + str(self.stats[stat]) + "\n\r"
        return return_string

    def set_item_name(self, item_name: str):
        self.itemName = item_name

    def set_item_desc(self, item_desc: str):
        self.itemDescription = item_desc

    def set_item_type(self, item_type: str):
        self.itemType = item_type

    def set_item_id(self, item_id: str):
        self.id = item_id

    def add_stat(self, stat_name: str, stat_value):
        if Reader.represents_int(stat_value):
            self.stats[stat_name] = int(stat_value)
        elif Reader.represents_float(stat_value):
            self.stats[stat_name] = float(stat_value)
        else:
            self.stats[stat_name] = stat_value

    def get_stat(self, stat_name: str):
        if stat_name in self.stats:
            return self.stats[stat_name]
        return None

    def is_valid_item(self) -> bool:
        if self.id != 0 and self.itemType != "":
            return True
        return False
