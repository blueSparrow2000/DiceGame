from entity import *


class Enemy(Entity):
    def __init__(self,my_name, hp, hpmax, attack_damage, pos,attack_pattern,rank):
        super().__init__('enemies/'+my_name, hp, hpmax, pos) # mypos is calculated as follows: how many enemy in one fight
        global icons, icon_container, sound_effects
        self.my_name = my_name # override

        ####################### enemy only stuffs ############################
        # self.pattern_image = dict()
        # for i in range(len(icons)):
        #     self.pattern_image[i] = icon_container[icons[i]]
        # self.pattern_analyzer = {'attack':2, 'defence':1, 'no op':0,'buff':3, 'unkown':4, 'regen':5} # translates pattern to icon key
        self.pattern_image = icon_container

        self.attack_damage = attack_damage
        self.next_move_loc = (self.mypos[0], self.mypos[1] - 60)

        # attack patterns
        self.current_pattern_idx = 0
        self.pattern = attack_pattern
        self.num_of_patterns = len(self.pattern)

        self.rank = rank

    def draw(self,screen): ################# ENEMY EXCLUSIVE
        super().draw(screen)
        self.show_next_move(screen)

    def proceed_next_pattern(self):
        # proceed to the next pattern
        self.current_pattern_idx = (self.current_pattern_idx+1)%self.num_of_patterns

    def show_next_move(self,screen):
        current_pattern = self.pattern[self.current_pattern_idx]

        # check whether can attack or not
        if current_pattern == 'attack' and (self.buffs['broken will']>0):
            # change to no op
            current_pattern = 'no op'

        # next_move_img = self.pattern_image[self.pattern_analyzer[current_pattern]]
        next_move_img = self.pattern_image[current_pattern]

        screen.blit(next_move_img, next_move_img.get_rect(center=self.next_move_loc))

    def get_current_damage(self):
        return self.attack_damage*self.get_attack_multiplier()

    def get_drop(self):
        return []

    def get_gold(self):
        return 1 # default one gold

class Mob(Enemy):
    def __init__(self, my_name = 'mob', hp=16, hpmax = 16, attack_damage = 5, pos = (332,mob_Y_level), attack_pattern = ['no op', 'buff', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank)

    def behave(self, player):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['hit'].play()
                counter_attack_damage = player.take_damage(self.get_current_damage())
                self.health -= counter_attack_damage
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1
                # player.buffs['toxin'] = 1
                # player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            pass # no op
        elif current_pattern=='buff':
            self.buffs['strength'] = 2 # for one turn since it is self buffing
            # self.buffs['attack immunity'] = 2
        elif current_pattern=='regen':
            pass # no op
        elif current_pattern=='unkown':
            pass # no op

        self.proceed_next_pattern()
        self.end_my_turn()
        time.sleep(0.2)

class Halo(Enemy):
    def __init__(self, my_name = 'halo', hp=999, hpmax = 999, attack_damage = 32, pos = (332,mob_Y_level), attack_pattern = ['unkown', 'buff', 'attack','regen'], rank = 1 ):
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank)

    def behave(self, player):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                time.sleep(0.3)
                sound_effects['hit'].play()
                counter_attack_damage = player.take_damage(self.get_current_damage())
                self.health -= counter_attack_damage
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1
                # player.buffs['toxin'] = 1
                # player.buffs['confusion'] = 1
        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            pass # no op
        elif current_pattern=='buff':
            player.buffs['confusion'] = 1
            player.buffs['vulnerability'] = 1

        elif current_pattern=='regen':
            self.regen()
        elif current_pattern=='unkown':
            player.buffs['broken will'] = 1


        self.proceed_next_pattern()

        self.end_my_turn()
        time.sleep(0.2)

    def get_heal_amount(self):
        return 15
