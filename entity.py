'''
Entity is common thing between player and enemy
- draw
- attributes
- buff/debuff effect

> Since buff counts are taken off every end of the turn, self-buffing needs extra duration
Buff/Debuff to enemy: self.buffs['broken will'] = turn duration
> 남에게 부여하는 버프 중에선 다시 내 차례가 돌아올때까지 남아있아야 하는 버프가 있고(toxin처럼 다시 내턴으로 돌아왔을때 효과가 나타나는 스킬들), 바로 다음 상대턴에 적용되는 버프가 있다.

Buff/Debuff to one self: self.buffs['broken will'] = turn duration + 1

'''


from image_processor import *
import pygame
from util import *

class Entity():
    def __init__(self,my_name, hp, hpmax, mypos):
        global buff_names
        self.image = load_image(my_name)

        self.health = hp
        self.max_health = hpmax
        self.mypos = mypos
        self.health_bar_pos = (self.mypos[0], self.mypos[1] + 40)
        self.icon_x = self.health_bar_pos[0] - 40
        self.icon_y = self.health_bar_pos[1]
        self.buff_icon_x = self.health_bar_pos[0] - 40
        self.buff_icon_y = self.health_bar_pos[1] + 30
        self.icon_delta = 30


        self.defence = 0
        self.base_defence = 10
        self.total_defence = self.defence + self.base_defence

        # buff & debuffs
        self.buffs = dict()
        for buff in buff_names:
            self.buffs[buff] = 0 #  debuff name: remaining turn duration if exist

        self.reset_buffs()

        # test buffs ['decay', 'strength', 'weakness','broken will','confusion','heal ban','poison','toxin']
        # self.buffs['broken will'] = 0

    def reset_buffs(self):
        self.can_attack = True
        self.strength_multiplier = 1
        self.strength_deplifier = 1
        self.defence_gain_multiplier = 1
        self.heal_multiplier = 1
        self.poisoned = False
        self.toxined = False

    def get_attack_multiplier(self):
        return self.strength_multiplier*self.strength_deplifier

    def refresh_my_turn(self):
        self.get_buff_effect() # get buff effects


        # reset the defence
        self.defence = 0
        self.update_defence()

    def end_my_turn(self): # do something at the end of the turn
        # if poisoned, get damaged
        if (self.poisoned):
            self.health -= 5

        self.update_buffs()  # update buff counts

    def show_hp_attributes(self,screen):
        global buff_icon_container
        draw_bar(screen, self.health_bar_pos[0], self.health_bar_pos[1], 64, 15, 100, 'silver')
        draw_bar(screen, self.health_bar_pos[0], self.health_bar_pos[1], 64, 15, 100 * self.health / self.max_health, 'coral')

        write_text(screen, self.health_bar_pos[0], self.health_bar_pos[1], "%d/%d" % (self.health, self.max_health), 15, 'maroon')
        if (self.total_defence > 0):

            screen.blit(shield_icon, shield_icon.get_rect(center=(self.icon_x, self.icon_y)))
            write_text(screen, self.icon_x, self.icon_y, "%d" % (self.total_defence), 15,
                       'deepskyblue')

        # show buff/debuffs
        cnt = 0
        next_row = 0
        for buff_name, buff_duration in self.buffs.items():
            # draw only when buff is on
            if buff_duration > 0 or (buff_name=='toxin' and self.toxined == True): # buff is on when corresponding state is also on # or (
                buff_icon = buff_icon_container[buff_name]
                if cnt > 2:
                    next_row += 1
                    cnt = 0
                screen.blit(buff_icon,
                            buff_icon.get_rect(center=(self.buff_icon_x + self.icon_delta * cnt, self.buff_icon_y + next_row * self.icon_delta)))
                write_text(screen, self.buff_icon_x + self.icon_delta * cnt + 10, self.buff_icon_y + 10 + next_row * self.icon_delta,
                           "%d" % (buff_duration), 15,
                           'gray')
                cnt += 1

    def draw(self,screen):
        screen.blit(self.image, self.image.get_rect(center=self.mypos))
        self.show_hp_attributes(screen)


    def take_damage(self, damage):
        if (self.toxined): # ignores defence
            self.health -= damage
            return

        partial_damage = damage - self.total_defence
        if partial_damage <0: # fully blocked
            self.total_defence -= damage
            # print('blocked!')
            return
        self.total_defence = 0
        self.health -= partial_damage
        # print('got hit!')

    def is_dead(self):
        return self.health <= 0

    def update_defence(self):
        self.total_defence = self.defence + self.base_defence

    def get_buff_effect(self):
        # reset buffs
        self.reset_buffs()
        for buff_name, buff_duration in self.buffs.items():
            if buff_duration > 0:
                if buff_name == 'decay':
                    self.defence_gain_multiplier = 0.5
                elif buff_name == 'strength':
                    self.strength_multiplier = 2
                elif buff_name == 'weakness':
                    self.strength_deplifier = 0.5
                elif buff_name == 'broken will':
                    self.can_attack = False
                elif buff_name == 'confusion':
                    pass
                elif buff_name == 'heal ban':
                    self.heal_multiplier = 0
                elif buff_name == 'poison':
                    self.poisoned = True
                elif buff_name == 'toxin':
                    self.toxined = True

    def update_buffs(self):
        for buff_name, buff_duration in self.buffs.items():
            if buff_duration > 0:
                self.buffs[buff_name] = max(0, buff_duration - 1)  # reduce one turn


# buff_name_description_dic = {
# 'confusion':"(player): cannot use secondary planar figure\n(enemies): misses an attack",
# }