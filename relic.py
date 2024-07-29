from util import *

class Relic():
    def __init__(self, name="Relic"):
        self.name = name

    def passive_effect(self):
        pass

    def active_effect(self):
        pass


class PoisonBottle(Relic):
    '''
    Increase damage & duration of poison dart skill
    '''
    def __init__(self):
        super().__init__(name="poison bottle")
















