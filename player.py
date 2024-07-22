from entity import *


class Player(Entity):
    def __init__(self, character_name,character_skills):
        global mob_Y_level, sound_effects# all the other skills should also be contained
        super().__init__(character_name, 100, 100, (100,mob_Y_level))
        ####################### player only stuffs ############################
        self.current_tile = None
        self.current_skill_idx = -1
        self.tile_dict = {'Attack':6, 'Defence':6, 'Regen':6, 'Skill':6}
        self.skill_book = character_skills

    def end_my_turn(self): # do something at the end of the turn
        super().end_my_turn()
        self.current_skill_idx = -1 # reset this
        self.current_tile = None

    def new_fight(self):
        for k,v in self.buffs.items():
            self.buffs[k] = 0 # reset
        self.defence = 0
        self.update_defence()
        self.current_tile = None
        self.current_skill_idx = -1


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

    def attack(self, target_list):
        sound_effects['sword'].play()
        for enemy in target_list:
            counter_attack_damage = enemy.take_damage(self.get_current_damage())
            self.health -= counter_attack_damage
            # enemy.buffs['broken will'] = 1
            # enemy.buffs['strength'] = 1
            # enemy.buffs['poison'] = 1

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
        # global requirement: Need at least one skill tile to use skill
        S =self.count_tile('Skill')
        if (S<=0):
            return False, 1


        # self.can_attack 확인하기. 공격하는 스킬의 경우 can attack일때만 valid하다
        skill_valid, target_nums,is_attack = getattr(self.skill_book, self.skill_book.skills[idx]+'_get_requirement')(self)
        if skill_valid and ((not is_attack) or (is_attack and self.can_attack)):
            # if valid, change the skill index to idx
            self.current_skill_idx = idx
            return skill_valid,target_nums
        return False,1

    def use_skill(self, target_list): # use the idx'th skill
        # before skill

        getattr(self.skill_book,self.skill_book.skills[self.current_skill_idx])(self,target_list)

        # after skill




