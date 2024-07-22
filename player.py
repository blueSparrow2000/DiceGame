from entity import *


class Player(Entity):
    def __init__(self):
        super().__init__('player', 100, 100, (100,320))
        ####################### player only stuffs ############################
        self.artifacts = []
        self.current_tile = None
        self.current_skill_idx = 0
        self.tile_dict = {'Attack':6, 'Defence':6, 'Regen':6, 'Skill':6}


    def new_fight(self):
        for k,v in self.buffs.items():
            self.buffs[k] = 0 # reset
        self.defence = 0
        self.update_defence()
        self.current_tile = None
        self.current_skill_idx = 0


    def push_tile_infos(self,tile_info):
        self.current_tile = tile_info


    def count_tile(self,name):
        for k,v in self.current_tile.items():
            if k==name:
                return v
        print("ERROR: no such name exists: ", name)
        return False # error

    def P(self,num):
        return 2**(num-1)

    def attack(self, enemy):
        enemy.take_damage(self.get_current_damage())
        enemy.buffs['broken will'] = 1
        enemy.buffs['strength'] = 1
        enemy.buffs['toxin'] = 1

    def get_current_damage(self):
        # count number of attack tiles
        A = self.count_tile('Attack')
        return self.P(A)*self.get_attack_multiplier()

    def defend(self):
        self.defence += self.get_defence_gain()
        self.update_defence()

    def get_defence_gain(self):
        # count number of defence tiles
        D = self.count_tile('Defence')
        return self.P(D)*self.defence_gain_multiplier

    def regen(self):
        self.health = min(self.max_health,self.health+self.get_heal_amount())

    def get_heal_amount(self):
        # count number of regen tiles
        R = self.count_tile('Regen')
        return self.heal_multiplier*self.P(R)

    def skill_ready(self, idx): # use the idx'th skill

        # if valid, change the skill index to idx
        self.current_skill_idx = idx
        return False,True

    def use_skill(self, enemies): # use the idx'th skill
        return True,True