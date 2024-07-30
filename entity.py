'''
Entity is common thing between player and enemy
- draw
- attributes
- buff/debuff effect

> Since buff counts are taken off every end of the turn, self-buffing needs extra duration
Buff/Debuff to enemy: self.buffs['broken will'] = turn duration
> 남에게 부여하는 버프 중에선 다시 내 차례가 돌아올때까지 남아있아야 하는 버프가 있고(toxin/vulnerability 처럼 다시 내턴으로 돌아왔을때 효과가 나타나는 스킬들), 바로 다음 상대턴에 적용되는 버프가 있다.

Buff/Debuff to one self: self.buffs['broken will'] = turn duration + 1

'''
from util import *


target_icon = load_image("icons/targeted")
EID = 0

class Entity():
    def __init__(self,my_name, hp, hpmax, mypos):
        global buff_names, EID
        self.EID = EID
        EID += 1
        self.my_name = my_name
        self.my_type='entity'
        self.image = load_image(my_name)

        self.health = hp
        self.max_health = hpmax
        self.mypos = mypos
        self.health_bar_pos = (self.mypos[0], self.mypos[1] + 40)
        self.icon_x = self.health_bar_pos[0] - 40
        self.icon_y = self.health_bar_pos[1]
        self.absorption_icon_x = self.health_bar_pos[0] - 70
        self.absorption_icon_y = self.health_bar_pos[1]
        self.buff_icon_x = self.health_bar_pos[0] - 40
        self.buff_icon_y = self.health_bar_pos[1] + 30
        self.icon_delta = 30
        self.targeted = False

        self.defence = 0
        self.base_defence = 0
        self.total_defence = self.defence + self.base_defence

        self.thorns = 0 # some enemy may have default thorns
        self.absorption = 0
        self.counter_attack = False
        self.confused = False

        ######## buff & debuffs
        self.buffs = dict()
        for buff in buff_names:
            self.buffs[buff] = 0 #  debuff name: remaining turn duration if exist

        self.reset_buffs()

        ######## relics
        self.relics = []

    def regen(self):
        self.health = min(self.max_health,self.health+self.get_heal_amount())

    def enforeced_regen(self, amount):
        self.health = min(self.max_health,self.health+amount)


    def get_heal_amount(self):
        return

    def reset_state(self): # 상대 변수들. 상대가 공격시 사용되는 변수들. 초기화는 내턴 시작시 수행.
        self.absorption = 0
        self.counter_attack = False

    def get_relic_effects(self):
        pass

    def reset_buffs(self):
        self.can_attack = True
        self.strength_multiplier = 1
        self.strength_deplifier = 1
        self.defence_gain_multiplier = 1
        self.heal_multiplier = 1
        self.poisoned = False
        self.toxined = False
        self.vulnerability_multiplier = 1
        self.confused = False

    def get_attack_multiplier(self):
        return self.strength_multiplier*self.strength_deplifier

    def refresh_my_turn(self):
        self.reset_state() # refresh state variables that activates on other side's turn

        self.get_buff_effect() # get buff effects

        self.get_relic_effects() # get relic effects - 적들도 쓸 수는 있지만 플레이어 위주...

        self.defence = 0  # reset the temporal defence
        self.update_defence()


    def end_my_turn(self): # do something at the end of the turn
        # if poisoned, get damaged
        if (self.poisoned):
            self.health -= 5

        self.update_buffs()  # update buff counts

    def show_hp_attributes(self,screen):
        global buff_icon_container, icon_container
        draw_bar(screen, self.health_bar_pos[0], self.health_bar_pos[1], 64, 15, 100, 'silver')
        draw_bar(screen, self.health_bar_pos[0], self.health_bar_pos[1], 64, 15, 100 * self.health / self.max_health, 'coral')

        write_text(screen, self.health_bar_pos[0], self.health_bar_pos[1], "%d/%d" % (self.health, self.max_health), 15, 'maroon')
        if (self.total_defence > 0):

            screen.blit(icon_container['shield'], icon_container['shield'].get_rect(center=(self.icon_x, self.icon_y)))
            write_text(screen, self.icon_x, self.icon_y, "%d" % (self.total_defence), 15,
                       'deepskyblue')

        # show buff/debuffs
        cnt = 0
        next_row = 0
        for buff_name, buff_duration in self.buffs.items():
            # draw only when buff is on
            if buff_duration > 0 or (buff_name=='toxin' and self.toxined == True) or (buff_name=='vulnerability' and self.vulnerability_multiplier>1): # buff is on when corresponding state is also on # or (
                buff_icon = buff_icon_container[buff_name]
                if cnt > 2:
                    next_row += 1
                    cnt = 0

                if (self.my_type == 'player' and buff_name=='attack immunity'): # for attack immunity, decrement 1
                    buff_duration-=1

                screen.blit(buff_icon,
                            buff_icon.get_rect(center=(self.buff_icon_x + self.icon_delta * cnt, self.buff_icon_y + next_row * self.icon_delta)))
                write_text(screen, self.buff_icon_x + self.icon_delta * cnt + 6, self.buff_icon_y + 6 + next_row * self.icon_delta,
                           "%d" % (buff_duration), 12,
                           'dimgray')
                cnt += 1

        if (self.absorption > 0):
            screen.blit(icon_container['absorption'], icon_container['absorption'].get_rect(center=(self.absorption_icon_x, self.absorption_icon_y)))
            write_text(screen, self.absorption_icon_x, self.absorption_icon_y, "%d" % (self.absorption), 15,
                       'khaki')

    def draw(self,screen):
        screen.blit(self.image, self.image.get_rect(center=self.mypos))
        self.show_hp_attributes(screen)
        if self.targeted:
            screen.blit(target_icon, target_icon.get_rect(center=self.mypos))


    def take_damage(self, damage_temp):
        if (self.buffs['attack immunity']>0): # do not take damage
            print(self.buffs['attack immunity'])
            return 0

        damage = self.vulnerability_multiplier * damage_temp
        counter_attack_damage = damage

        # consider absorption first
        damage = max(0, damage - self.absorption)
        # print(self.my_name,'got damage of',  damage_temp)

        if (self.toxined): # ignores defence
            self.health -= damage
        else:
            partial_damage = damage - self.total_defence
            if partial_damage <0: # fully blocked
                self.total_defence -= damage
                # print('blocked!')
            else:
                self.total_defence = 0
                self.health -= partial_damage
                # print('got hit!')

        if (self.counter_attack):
            return counter_attack_damage
        else:
            return 0

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
                    self.confused = True
                elif buff_name == 'heal ban':
                    self.heal_multiplier = 0
                elif buff_name == 'poison':
                    self.poisoned = True
                elif buff_name == 'toxin':
                    self.toxined = True
                elif buff_name == 'vulnerability':
                    self.vulnerability_multiplier = 2
                elif buff_name == 'attack immunity':
                    pass


    def update_buffs(self):
        for buff_name, buff_duration in self.buffs.items():
            if buff_duration > 0:
                self.buffs[buff_name] = max(0, buff_duration - 1)  # reduce one turn


# buff_name_description_dic = {
# 'confusion':"(player): cannot use secondary planar figure\n(enemies): misses an attack",
# }