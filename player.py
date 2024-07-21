from image_processor import *
import pygame
from image_processor import *
from util import *

class Player():
    def __init__(self):
        self.tile_dict = {'Attack':6, 'Defence':6, 'Regen':6, 'Skill':6}
        self.max_health = 100
        self.health = self.max_health
        self.image = load_image('player')
        self.mypos = (100,400)
        self.current_tile = None
        self.current_skill_idx = 0
        self.artifacts = []
        self.defence = 0
        self.base_defence = 0
        self.total_defence = self.defence + self.base_defence

        # debuffs
        self.debuffs = {'weakness':0, 'armor_gain_less':0}# debuff name: remaining turn duration if exist



    def new_fight(self):
        for k,v in self.debuffs.items():
            self.debuffs[k] = 0 # reduce one turn
            # apply the effect
        self.defence = 0
        self.total_defence = self.defence + self.base_defence
        self.current_tile = None
        self.current_skill_idx = 0

    def take_damage(self, damage):
        partial_damage = damage - self.total_defence
        if partial_damage <0: # fully blocked
            self.total_defence -= damage
            return
        self.total_defence = 0
        self.health -= partial_damage

    def refresh_my_turn(self):
        for k,v in self.debuffs.items():
            self.debuffs[k] = max(0, v-1) # reduce one turn
            # apply the effect

        # reset the defence
        self.defence = 0
        self.total_defence = self.defence + self.base_defence


    def draw(self,screen):
        screen.blit(self.image, self.image.get_rect(center=self.mypos))
        draw_bar(screen, self.mypos[0], self.mypos[1] - 60, 64, 10, 100, 'gray')
        draw_bar(screen, self.mypos[0], self.mypos[1] - 60, 64, 10, 100*self.health/self.max_health, 'RED')

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
        # count number of attack tiles
        A = self.count_tile('Attack')
        enemy.get_damage(self.P(A))

    def defend(self):
        # count number of defence tiles
        D = self.count_tile('Defence')
        self.defence += self.P(D)

    def regen(self):
        # count number of regen tiles
        R = self.count_tile('Regen')
        self.health = min(self.max_health,self.health+self.P(R))


    def skill(self, idx): # use the idx'th skill

        # if valid, change the skill index to idx
        self.current_skill_idx = idx
        return False,True

    def use_skill(self, enemies): # use the idx'th skill
        return True,True