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

        self.defence = 0 # 한 턴만 유지도는 방어도
        self.temporal_defence = 0 # 여러턴 유지되는 방어도. 깨지면 복구되지 않음 (언제 리셋되는지는 플레이어냐, 적이냐에 따라 다름. 적은 보통 리셋 안되는 방어도)
        self.base_defence = 0 # 기본적으로 깨져도 계속 복구되는 방어도. 방어구 같은 개념)
        self.base_defence_for_turn = self.base_defence # 매 턴 보호할 수 있는 최대량으로, self.base_defence만큼으로 시작해서 공격 받을때마다 줄어드는 량이다 / 내 턴으로 리프레시할때 다시 base defence로 리셋됨
        self.total_defence = self.defence + self.temporal_defence + self.base_defence_for_turn

        self.thorny = False # some enemy may have default thorns
        self.absorption = 0
        self.counter_attack = False
        self.confused = False

        # immunities
        self.immune_to_poison = False
        self.immune_to_toxin = False
        self.immune_to_weakness = False

        ######## buff & debuffs
        self.buffs = dict()
        for buff in buff_names:
            self.buffs[buff] = 0 #  debuff name: remaining turn duration if exist

        ####################
        self.can_attack = True
        self.strength_multiplier = 1
        self.strength_deplifier = 1
        self.defence_gain_multiplier = 1
        self.heal_multiplier = 1
        self.poisoned = False
        self.toxined = False
        self.vulnerability_multiplier = 1
        self.confused = False
        ####################
        self.reset_buffs()

        ######## relics
        self.relics = []


    def set_zero_defence(self):
        self.defence = 0
        self.temporal_defence = 0
        self.base_defence_for_turn = 0
        self.update_defence()


    def set_max_health(self,max_health):
        self.max_health = max_health
        if self.health > self.max_health:
            self.health = self.max_health

    def regen(self):
        self.health = min(self.max_health,self.health+self.get_heal_amount())

    def enforced_regen(self, amount):
        self.health = min(self.max_health,self.health+amount)


    def get_heal_amount(self):
        return 0

    def reset_state(self): # 상대 변수들. 상대가 공격시 사용되는 변수들. 초기화는 내턴 시작시 수행.
        self.absorption = 0
        self.counter_attack = False

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

        self.defence = 0  # reset the defence
        self.base_defence_for_turn = self.base_defence # reset base defence
        self.update_defence()


    def end_my_turn(self, others = None): # do something at the end of the turn
        # if poisoned, get damaged
        if (self.poisoned) and (not self.immune_to_poison):
            self.health -= 5

        self.update_buffs()  # update buff counts

    def show_hp_attributes(self,screen,mousepos):
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

                # if (self.my_type == 'player' and buff_name=='attack immunity'): # for attack immunity, decrement 1
                #     buff_duration-=1
                location = [self.buff_icon_x + self.icon_delta * cnt, self.buff_icon_y + next_row * self.icon_delta]
                screen.blit(buff_icon,
                            buff_icon.get_rect(center=location))
                write_text(screen, location[0] + 6,location[1] + 6, "%d" % (buff_duration), 12, 'dimgray')

                if check_inside_button(mousepos, location, self.icon_delta // 2):  # if mouse is pointing to the relic
                    description = buff_name_description_dic[buff_name]
                    write_text(screen, width // 2, turn_text_level + self.icon_delta, description, 17, "white", 'black')
                cnt += 1

        if (self.absorption > 0):
            screen.blit(icon_container['absorption'], icon_container['absorption'].get_rect(center=(self.absorption_icon_x, self.absorption_icon_y)))
            write_text(screen, self.absorption_icon_x, self.absorption_icon_y, "%d" % (self.absorption), 15,
                       'khaki')

    def draw(self,screen, mousepos):
        screen.blit(self.image, self.image.get_rect(center=self.mypos))
        self.show_hp_attributes(screen, mousepos)
        if self.targeted:
            screen.blit(target_icon, target_icon.get_rect(center=self.mypos))

    def death_check(self):
        if self.health > 0:
            return False # not dead
        # otherwise, do what child classes will do
        return True

    def take_damage(self, attacker, damage_temp, no_fightback = False):
        if (self.buffs['attack immunity']>0): # do not take damage
            print(self.buffs['attack immunity'])
            self.buffs['attack immunity'] -= 1 # discount one
            return 0

        damage = self.vulnerability_multiplier * damage_temp
        counter_attack_damage = damage
        # consider absorption first
        damage = max(0, damage - self.absorption)
        # print(self.my_name,'got damage of',  damage_temp)

        if (self.toxined and (not self.immune_to_toxin)): # ignores defence
            self.health -= damage
        else:
            partial_damage = damage - self.total_defence
            if partial_damage < 0: # can be fully blocked
                sound_effects['block'].play()
                ################################# defence algorithm #####################################
                # self.base_defence_for_turn은 매 턴 시작시 self.base_defence값으로 초기화됨
                # self.defence는 매턴 시작시 0으로 초기화됨
                # self.temporal_defence는 매 턴마다 사라지는 방어도가 아님! 누적되는 방어도

                D1 = damage - self.base_defence_for_turn
                if D1 <= 0:
                    self.base_defence_for_turn = self.base_defence_for_turn - damage
                else: # base defence 뚫림
                    self.base_defence_for_turn = 0
                    D2 = D1 - self.defence
                    if D2 <= 0:
                        self.defence = self.defence - D1
                    else: # defence 뚫림
                        self.defence = 0
                        self.temporal_defence = self.temporal_defence - D2  # temporal defence를 소진함, 근데 토탈 디펜스가 더 컸으니 다 막을 수 있음

                self.update_defence()
                ################################# defence algorithm #####################################
                # print('blocked!')
            else:
                if self.total_defence > 0: # if there were shield but it broke
                    sound_effects['break'].play()
                self.defence = 0
                self.temporal_defence = 0
                self.total_defence = 0
                self.health -= partial_damage
                # print('got hit!')

        if not self.death_check():
        ############### here is only reachable if I am not dead ##########
            if attacker is not None and (not no_fightback):
                if (self.counter_attack): # do a counter attack
                    attacker.health -= counter_attack_damage # immediately damages enemies
                elif self.thorny:
                    attacker.health -= damage_temp // 2  # take half of damage back

    def is_dead(self):
        return self.health <= 0

    def update_defence(self):
        self.total_defence = self.defence + self.temporal_defence + self.base_defence_for_turn

    def get_buff_effect(self, enforced = True):
        if enforced:
            # reset buffs
            self.reset_buffs()
        for buff_name, buff_duration in self.buffs.items():
            if buff_duration > 0:
                if buff_name == 'decay':
                    self.defence_gain_multiplier = 0.5
                elif buff_name == 'strength':
                    self.strength_multiplier = 2
                elif buff_name == 'weakness':
                    if not self.immune_to_weakness:
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
                if buff_name == 'attack immunity': # does not decay
                    continue
                self.buffs[buff_name] = max(0, buff_duration - 1)  # reduce one turn


# buff_name_description_dic = {
# 'confusion':"(player): cannot use secondary planar figure\n(enemies): misses an attack",
# }