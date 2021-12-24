import Reader


class Condition:
    def __init__(self, condition_type: str, value: str, condition="", element_id=0, item_name=""):
        self.conditionType: str = condition_type

        self.elementId: int = element_id
        self.elementName: str = item_name

        self.condition: str = Reader.parse_condition(condition)
        self.value: str = value

    def __repr__(self):
        if self.conditionType == "Item":
            return "        " + self.elementName + " [" + str(self.elementId) + "] " \
                   + self.condition + " " + str(self.value) + "\n\r"
        elif self.conditionType.startswith("Flag_"):
            return "        Flag " + str(self.elementId) + " " \
                   + self.condition + " " + str(self.value) + "\n\r"
        elif self.conditionType == "Quest":
            return "        Quest: " + self.elementName + " [" + str(self.elementId) + "] " \
                   + self.condition + " " + str(self.value) + "\n\r"
        else:
            return "        " + self.conditionType + " " + self.condition + " " + str(self.value) + "\n\r"
