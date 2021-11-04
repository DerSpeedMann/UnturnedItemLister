class NpcElement:
    def __init__(self):
        self.requirements = []

    def add_requirements(self, requirements):
        self.requirements.extend(requirements)
