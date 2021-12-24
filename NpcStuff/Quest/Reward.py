import Reader


class Reward:
    def __init__(self, reward_type, value, condition="", element_id="", item_name=""):
        self.rewardType = reward_type

        self.elementId = element_id
        self.itemName = item_name

        self.condition = Reader.parse_condition(condition)
        self.value = value

    def __repr__(self):
        if self.rewardType == "Item":
            return "        " + self.itemName + " [" + str(self.elementId) + "] " \
                   + self.condition + " " + str(self.value) + "\n\r"
        elif self.rewardType.startswith("Flag_"):
            return "        Flag " + str(self.elementId) + " " \
                   + self.condition + " " + str(self.value) + "\n\r"
        else:
            return "        " + self.rewardType + " " + self.condition + " " + str(self.value) + "\n\r"
