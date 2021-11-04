from NpcStuff.NpcElement import NpcElement
from NpcStuff.Quest.Condition import Condition
from NpcStuff.Quest.Reward import Reward


class Quest(NpcElement):
    def __init__(self, quest_id: int, quest_name="", quest_description=""):
        super().__init__()
        self.id: int = quest_id
        self.questName: str = quest_name
        self.questDescription: str = quest_description
        self.conditions: [Condition] = []
        self.rewards: [Reward] = []

    def __repr__(self):
        return_string = "     " + self.questName + " [" + str(self.id) + "]\n\r"
        return_string += "      " + self.questDescription + "\n\r"
        if len(self.requirements) >= 1:
            return_string += "      Requires: \n\r"
            for requirement in self.requirements:
                return_string += str(requirement)
        if len(self.conditions) >= 1:
            return_string += "       Conditions: \n\r"
            for condition in self.conditions:
                return_string += str(condition)

        if len(self.rewards) >= 1:
            return_string += "       Rewards: \n\r"
            for reward in self.rewards:
                return_string += str(reward)
        return return_string + "\n\r"

    def add_condition(self, condition: Condition):
        self.conditions.append(condition)

    def add_reward(self, reward: Reward):
        self.rewards.append(reward)
