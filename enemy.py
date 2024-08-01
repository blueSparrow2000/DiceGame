from entity import *


class Enemy(Entity):
    def __init__(self,my_name, hp, hpmax, attack_damage, pos,attack_pattern,rank,gold_reward=1):
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

        self.gold = gold_reward

    def draw(self,screen,mousepos): ################# ENEMY EXCLUSIVE
        super().draw(screen,mousepos)
        self.show_next_move(screen,mousepos)

        if check_inside_button(mousepos, self.mypos, self.icon_delta // 2):  # if mouse is pointing to the relic
            write_text(screen, self.mypos[0], self.mypos[1], self.my_name, 20, "lightgray", 'black')


    def proceed_next_pattern(self):
        # proceed to the next pattern
        self.current_pattern_idx = (self.current_pattern_idx+1)%self.num_of_patterns

    def show_next_move(self,screen,mousepos):
        current_pattern = self.pattern[self.current_pattern_idx]

        # check whether can attack or not
        if current_pattern == 'attack' and (self.buffs['broken will']>0):
            # change to no op
            current_pattern = 'no op'

        # next_move_img = self.pattern_image[self.pattern_analyzer[current_pattern]]
        next_move_img = self.pattern_image[current_pattern]
        screen.blit(next_move_img, next_move_img.get_rect(center=self.next_move_loc))


        description = ""
        if current_pattern == 'attack':
            description = "%d"%self.get_current_damage()
        elif current_pattern == 'buff':
            pass
        elif current_pattern == 'regen':
            description = "%d"%self.get_heal_amount()


        if description:
            write_text(screen, self.next_move_loc[0]+8, self.next_move_loc[1]+8, description, 15, "black")


        if check_inside_button(mousepos, self.next_move_loc, self.icon_delta // 2):  # if mouse is pointing to the relic
            description = ""
            if current_pattern == 'no op':
                description = "does nothing"
            else:
                description = "It will try to %s" % current_pattern

            write_text(screen, width // 2, turn_text_level + self.icon_delta, description, 17, "white", 'black')

    def get_current_damage(self):
        return self.attack_damage*self.get_attack_multiplier()

    def get_drop(self):
        return []

    def get_gold(self):
        return self.gold # default one gold




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
                player.take_damage(self,self.get_current_damage())
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


class Mob(Enemy):
    def __init__(self, my_name = 'mob', hp=20, hpmax = 20, attack_damage = 5, pos = (332,mob_Y_level), attack_pattern = ['no op', 'buff', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 1)

    def behave(self, player):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['hit'].play()
                player.take_damage(self,self.get_current_damage())
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

class Fragment(Enemy):
    def __init__(self, my_name = 'fragment', hp=16, hpmax = 16, attack_damage = 5, pos = (332,mob_Y_level), attack_pattern = ['no op', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 2)
        self.thorny = True

    def behave(self, player):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['sword'].play()
                player.take_damage(self,self.get_current_damage())
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
            pass
        elif current_pattern=='regen':
            pass # no op
        elif current_pattern=='unkown':
            pass # no op

        self.proceed_next_pattern()
        self.end_my_turn()


