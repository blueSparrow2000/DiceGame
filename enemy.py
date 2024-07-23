from entity import *


class Enemy(Entity):
    def __init__(self,my_name, hp, hpmax, attack_damage, pos):
        super().__init__(my_name, hp, hpmax, pos) # mypos is calculated as follows: how many enemy in one fight
        global icons, icon_container, sound_effects
        ####################### enemy only stuffs ############################
        self.pattern_image = dict()
        for i in range(len(icons)):
            self.pattern_image[i] = icon_container[icons[i]]
        #self.pattern_image = {0:icons['no op'], 1:icons['shield'], 2:icons['sword'], 3:icons['buff'], 4:icons['unkown']}
        self.pattern_analyzer = {'attack':2, 'defence':1, 'no op':0,'buff':3, 'unkown':4} # translates pattern to icon key

        self.attack_damage = attack_damage
        self.next_move_loc = (self.mypos[0], self.mypos[1] - 60)


    def draw(self,screen): ################# ENEMY EXCLUSIVE
        super().draw(screen)
        self.show_next_move(screen)

    def show_next_move(self,screen):
        pass

    def get_current_damage(self):
        return self.attack_damage*self.get_attack_multiplier()


class Mob(Enemy):
    def __init__(self, my_name = 'enemies/mob', hp=30, hpmax = 30, attack_damage = 5, pos = (332,300)):
        super().__init__(my_name,hp,hpmax,attack_damage,pos)
        self.current_pattern_idx = 0
        self.pattern = ['attack','no op'] #
        self.num_of_patterns = len(self.pattern)

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
                player.buffs['confusion'] = 1
        elif current_pattern=='no op':
            pass # no op

        self.proceed_next_pattern()

        self.end_my_turn()
        time.sleep(0.2)

    def proceed_next_pattern(self):
        # proceed to the next pattern
        self.current_pattern_idx = (self.current_pattern_idx+1)%self.num_of_patterns

    def show_next_move(self,screen):
        current_pattern = self.pattern[self.current_pattern_idx]

        # check whether can attack or not
        if current_pattern == 'attack' and (self.buffs['broken will']>0): #not self.can_attack
            # change to no op
            current_pattern = 'no op'

        next_move_img = self.pattern_image[self.pattern_analyzer[current_pattern]]
        screen.blit(next_move_img, next_move_img.get_rect(center=self.next_move_loc))

