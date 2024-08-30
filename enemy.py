from entity import *


class Enemy(Entity):
    def __init__(self,my_name, hp, hpmax, attack_damage, pos,attack_pattern,rank,gold_reward=1):
        super().__init__('enemies/'+my_name, hp, hpmax, pos) # mypos is calculated as follows: how many enemy in one fight
        global icons, icon_container, sound_effects
        self.my_name = my_name # override
        self.passive = False
        self.passive_to_aggressive = False

        ####################### enemy only stuffs ############################
        # self.pattern_image = dict()
        # for i in range(len(icons)):
        #     self.pattern_image[i] = icon_container[icons[i]]
        # self.pattern_analyzer = {'attack':2, 'defence':1, 'no op':0,'buff':3, 'unknown':4, 'regen':5} # translates pattern to icon key
        self.pattern_image = icon_container

        self.attack_damage = attack_damage
        self.next_move_loc = (self.mypos[0], self.mypos[1] - 60)

        # attack patterns
        self.current_pattern_idx = 0
        self.pattern = attack_pattern
        self.num_of_patterns = len(self.pattern)

        self.rank = rank

        self.gold = gold_reward

        self.spawn_request = False

        self.turn_count_threshold = 5
        self.turn_count = 0

    def get_description(self): # override
        return None
    def write_description(self, screen, mousepos):
        if check_inside_button(mousepos, self.mypos, self.icon_delta // 2):  # if mouse is pointing to the relic
            description = self.get_description()
            if description:
                write_text(screen, width // 2, turn_text_level + self.icon_delta, description, 17, "white", 'black')

    def passive_behavior(self, player):
        self.turn_count += 1
        if self.passive and (self.passive_to_aggressive or self.turn_count >= self.turn_count_threshold): # change passive to aggresive
            self.passive_to_aggressive = False
            self.passive = False
            self.refresh_my_turn()
            current_pattern = 'no op'
            self.end_my_turn()
            return False
        elif self.passive:         # no op until get attacked
            self.refresh_my_turn()
            current_pattern = 'no op'
            self.end_my_turn()
            return False
        else:# do behave!
            return True


    def take_damage(self, attacker, damage_temp, no_fightback = False): # wake up when taken damage!
        super().take_damage(attacker, damage_temp, no_fightback)
        self.passive_to_aggressive = True

    def draw(self,screen,mousepos): ################# ENEMY EXCLUSIVE
        super().draw(screen,mousepos)
        self.show_next_move(screen,mousepos)
        self.write_description(screen,mousepos)

        if check_inside_button(mousepos, self.mypos, self.icon_delta // 2):
            write_text(screen, self.mypos[0], self.mypos[1], self.my_name, 20, "lightgray", 'black')

    def get_next_move_on_player_turn(self):
        return self.pattern[self.current_pattern_idx]

    def proceed_next_pattern(self):
        # proceed to the next pattern
        self.current_pattern_idx = (self.current_pattern_idx+1)%self.num_of_patterns

    def show_next_move(self,screen,mousepos):
        current_pattern = self.pattern[self.current_pattern_idx]

        # check whether can attack or not
        if current_pattern == 'attack' and (self.buffs['broken will']>0):
            # change to no op
            current_pattern = 'no op'

        if self.passive:
            current_pattern = 'no op'

        # next_move_img = self.pattern_image[self.pattern_analyzer[current_pattern]]
        next_move_img = self.pattern_image[current_pattern]
        screen.blit(next_move_img, next_move_img.get_rect(center=self.next_move_loc))


        description = ""
        if current_pattern == 'attack' or current_pattern == 'lifesteal':
            if isinstance(self.attack_damage, list):
                description = "%d~%d" %(self.attack_damage[0],self.attack_damage[1])
            else:
                if current_pattern == 'attack' and self.my_name=="apostle":
                    # health_proportion = player.health // 4
                    # damage = max(health_proportion, 20)
                    # player.take_damage(self, damage * self.get_attack_multiplier())
                    description = "x/4"
                else:
                    description = "%d"%self.get_current_damage()
        elif current_pattern == 'buff':
            pass
        elif current_pattern == 'regen':
            description = "%d"%self.get_heal_amount()
        elif current_pattern == 'summon':
            description = "+"
        elif current_pattern == 'infiltrate':
            description = ""

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
    def __init__(self, my_name = 'halo', hp=999, hpmax = 999, attack_damage = [64,128], pos = (332,mob_Y_level), attack_pattern = ['unknown', 'buff', 'attack','regen'], rank = 1 ):
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 300)

    def get_description(self): # override
        return "??? "

    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                time.sleep(0.2)
                sound_effects['blast'].play()
                time.sleep(0.1)
                damage = random.randint(self.attack_damage[0], self.attack_damage[1])
                player.take_damage(self, damage*self.get_attack_multiplier())
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
            player.buffs['confusion'] += 1
            player.buffs['vulnerability'] += 1
        elif current_pattern=='regen':
            self.regen()
        elif current_pattern=='unknown':
            player.buffs['broken will'] += 1
        elif current_pattern == 'summon':
            pass

        self.proceed_next_pattern()

        self.end_my_turn()
        time.sleep(0.2)

    def get_heal_amount(self):
        return 15


class Mob(Enemy):
    def __init__(self, my_name = 'mob', hp=20, hpmax = 20, attack_damage = 5, pos = (332,mob_Y_level), attack_pattern = ['shield', 'buff', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 3)

    def behave(self, player, enemy = None):
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
            self.defence += 10
            self.update_defence()
        elif current_pattern=='buff':
            self.buffs['strength'] += 2 # for one turn since it is self buffing
            # self.buffs['attack immunity'] = 2
        elif current_pattern=='regen':
            pass # no op
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass

        self.proceed_next_pattern()
        self.end_my_turn()

class Fragment(Enemy):
    def __init__(self, my_name = 'fragment', hp=16, hpmax = 16, attack_damage = 5, pos = (332,mob_Y_level), attack_pattern = ['no op', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 5)
        self.thorny = True
    def get_description(self): # override
        return "Thorny: inflict half of the damage to attacker"

    def behave(self, player, enemy = None):
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
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass

        self.proceed_next_pattern()
        self.end_my_turn()


class Lenz(Enemy):
    def __init__(self, my_name = 'lenz', hp=30, hpmax = 30, attack_damage = 5, pos = (332,mob_Y_level), attack_pattern = ['no op','summon', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 6)
    def get_description(self): # override
        return "Can duplicate itself"


    def get_spawn_mob_name(self):
        self.spawn_request = False
        return "lenz"

    def behave(self, player, enemy = None):
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
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            self.spawn_request = True


        self.proceed_next_pattern()
        self.end_my_turn()





class Embryo(Enemy):
    def __init__(self, my_name = 'embryo', hp=64, hpmax = 64, attack_damage = 16, pos = (332,mob_Y_level), attack_pattern = ['no op','infiltrate'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 5)


    def behave(self, player, enemy = None):
        ready_to_behave = self.passive_behavior(player)
        if not ready_to_behave:
            return

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
            pass
        elif current_pattern=='regen':
            pass # no op
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate': # place a tile inside the player's tile
            player.board.insert_a_tile_on_board("Proliferation")

        self.proceed_next_pattern()
        self.end_my_turn()




class Mine(Enemy):
    def __init__(self, my_name = 'mine', hp=30, hpmax = 30, attack_damage = 6, pos = (332,mob_Y_level), attack_pattern = ['no op','infiltrate','attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 8)
        self.thorny = True
    def get_description(self): # override
        return "Thorny: inflict half of the damage to attacker"

    def behave(self, player, enemy = None):
        ready_to_behave = self.passive_behavior(player)
        if not ready_to_behave:
            return

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
            pass
        elif current_pattern=='regen':
            pass # no op
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate': # place a tile inside the player's tile
            player.board.insert_a_tile_on_board("Spike")

        self.proceed_next_pattern()
        self.end_my_turn()





##### PRIMARY BOSS ####
class Norm(Enemy):
    def __init__(self, my_name = 'norm', hp=32, hpmax = 32, attack_damage = 16, pos = (332,mob_Y_level), attack_pattern = ['attack', 'shield'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 10)


    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['hard_hit'].play()
                player.take_damage(self,self.get_current_damage())
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1
                # player.buffs['toxin'] = 1
                # player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            self.defence += 16
            self.update_defence()
        elif current_pattern=='buff':
            pass
        elif current_pattern=='regen':
            pass # no op
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass

        self.proceed_next_pattern()
        self.end_my_turn()

class Scout(Enemy):
    def __init__(self, my_name = 'scout', hp=32, hpmax = 32, attack_damage = 8, pos = (332,mob_Y_level), attack_pattern = ['buff', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 10)
        '''
        This mob gets stronger after attacking
        '''

    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['hard_hit'].play()
                player.take_damage(self,self.get_current_damage())
                self.attack_damage += 2
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1

                # player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            pass
        elif current_pattern=='buff':
            player.buffs['vulnerability'] += 1
        elif current_pattern=='regen':
            pass
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass

        self.proceed_next_pattern()
        self.end_my_turn()

class Sentinel(Enemy):
    def __init__(self, my_name = 'sentinel', hp=64, hpmax = 64, attack_damage = 16, pos = (332,mob_Y_level), attack_pattern = ['buff', 'shield', 'attack', 'regen'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 12)


    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['hard_hit'].play()
                player.take_damage(self,self.get_current_damage())
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1

                # player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            sound_effects['block'].play()
            self.defence += 16
            self.update_defence()
            # for entity in enemy:
            #     entity.defence += 16
            #     entity.update_defence()
        elif current_pattern=='buff':
            player.buffs['weakness'] += 1
        elif current_pattern=='regen':
            self.regen()
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass

        self.proceed_next_pattern()
        self.end_my_turn()

    def get_heal_amount(self):
        return 10

class Observer(Enemy):
    def __init__(self, my_name = 'observer', hp=64, hpmax = 64, attack_damage = 12, pos = (332,mob_Y_level), attack_pattern = ['buff',  'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 12)


    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['hard_hit'].play()
                player.take_damage(self,self.get_current_damage())
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1

                # player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            pass
        elif current_pattern=='buff':
            player.buffs['vulnerability'] += 1
        elif current_pattern=='regen':
            pass
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass

        self.proceed_next_pattern()
        self.end_my_turn()



class Carrier(Enemy):
    def __init__(self, my_name = 'carrier', hp=200, hpmax = 200, attack_damage = 20, pos = (332,mob_Y_level), attack_pattern = ['summon','shield', 'healall','attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 100)
        self.base_defence = 4 #
    def get_description(self): # override
        return "Boss: 4 base defence, summons norm"

    def get_spawn_mob_name(self):
        self.spawn_request = False
        return "norm"

    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['lazer'].play()
                player.take_damage(self,self.get_current_damage())
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1
                # player.buffs['toxin'] = 1
                # player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            sound_effects['block'].play()
            self.defence += 100
            self.update_defence()
        elif current_pattern=='buff':
            pass
        elif current_pattern=='healall': # heal all allies
            sound_effects['shruff'].play()
            for entity in enemy:
                entity.enforced_regen(20)
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            self.spawn_request = True


        self.proceed_next_pattern()
        self.end_my_turn()


    def get_heal_amount(self):
        return 20

class Apostle(Enemy):
    def __init__(self, my_name = 'apostle', hp=100, hpmax = 1000, attack_damage = 20, pos = (332,mob_Y_level), attack_pattern = ['no op', 'attack', 'lifesteal'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 25)

    def get_description(self): # override
        return "Deal damage proportional to player's health"

    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='lifesteal':
            if self.can_attack:
                sound_effects['small_hit'].play()
                player.take_damage(self,self.get_current_damage())
                self.enforced_regen(self.attack_damage)

        elif current_pattern == 'attack':
            if self.can_attack:
                sound_effects['playerdeath'].play()
                health_proportion = player.health // 4
                damage = health_proportion #max(health_proportion, 20)
                player.take_damage(self, damage * self.get_attack_multiplier())

        elif current_pattern=='no op':
            player.buffs['vulnerability'] += 1
            pass # no op
        elif current_pattern=='shield':
            pass
        elif current_pattern=='buff':
            pass
        elif current_pattern=='regen':
            pass
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate': # place a tile inside the player's tile
            player.board.insert_a_tile_on_board("Slime")

        self.proceed_next_pattern()
        self.end_my_turn()

class Silent(Enemy):
    def __init__(self, my_name='silent', hp=800, hpmax=800, attack_damage=[32, 64], pos=(332, mob_Y_level),
                 attack_pattern=['shield', 'buff', 'attack', 'infiltrate'], rank=1):  #
        super().__init__(my_name, hp, hpmax, attack_damage, pos, attack_pattern, rank, gold_reward=200)

        self.immune_to_poison = True

    '''
    This mob does not show you what it will do (randomly chosen)
    immune to poison
    '''
    def get_description(self): # override
        return "Boss: Immune to poison / next moves are randomized"
    def behave(self, player, enemy=None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]

        if current_pattern == 'attack':
            if self.can_attack:
                sound_effects['water'].play()
                damage = random.randint(self.attack_damage[0], self.attack_damage[1])
                player.take_damage(self, damage * self.get_attack_multiplier())

        elif current_pattern == 'no op':
            pass  # no op
        elif current_pattern == 'shield':
            self.defence += 32
            self.update_defence()
        elif current_pattern == 'buff':
            player.buffs['weakness'] += 3
            player.buffs['vulnerability'] += 3
            player.buffs['toxin'] += 3
        elif current_pattern == 'regen':
            self.regen()
        elif current_pattern == 'unknown':
            pass  # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate':  # place a tile inside the player's tile
            print("unusable infiltration!")
            for i in range(3):
                player.board.insert_a_tile_on_board("Unusable")

        elif current_pattern == 'poison':
            pass

        # next pattern is randomized
        self.proceed_next_pattern()
        self.end_my_turn()

    def proceed_next_pattern(self):
        # self.current_pattern_idx = (self.current_pattern_idx + 1) % self.num_of_patterns
        self.current_pattern_idx = random.randint(0, len(self.pattern) - 1)  # random pattern

    def get_heal_amount(self):
        return 16

    def show_next_move(self,screen,mousepos):
        if self.health < 200: # phase two
            next_move_img = self.pattern_image['unknown']
            screen.blit(next_move_img, next_move_img.get_rect(center=self.next_move_loc))

            if check_inside_button(mousepos, self.next_move_loc, self.icon_delta // 2):  # if mouse is pointing to the relic
                write_text(screen, width // 2, turn_text_level + self.icon_delta, "what will it do?", 17, "white", 'black')
        else:
            super().show_next_move(screen,mousepos)



class Scalpion(Enemy):
    def __init__(self, my_name = 'scalpion', hp=180, hpmax = 180, attack_damage = [8,16], pos = (332,mob_Y_level), attack_pattern = ['toxin', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 8)
        self.thorny = True
    '''
    This mob does random damage attack
    '''
    def get_description(self): # override
        return "Thorny: inflict half of the damage to attacker"

    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['sword'].play()
                damage = random.randint(self.attack_damage[0], self.attack_damage[1])
                player.take_damage(self, damage*self.get_attack_multiplier())
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1
                # player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            pass
        elif current_pattern=='buff':
            pass
        elif current_pattern=='regen':
            self.regen()
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate': # place a tile inside the player's tile
            pass
        elif current_pattern == 'toxin':
            sound_effects['water'].play()
            player.buffs['toxin'] += 5
        self.proceed_next_pattern()
        self.end_my_turn()

    def get_heal_amount(self):
        return 10



class Snalk(Enemy):
    def __init__(self, my_name = 'snalk', hp=120, hpmax = 120, attack_damage = [4,8], pos = (332,mob_Y_level), attack_pattern = ['poison', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 7)
    '''
    This mob does random damage attack
    '''
    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['sword'].play()
                damage = random.randint(self.attack_damage[0], self.attack_damage[1])
                player.take_damage(self, damage*self.get_attack_multiplier())
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1
                # player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            pass
        elif current_pattern=='buff':
            pass
        elif current_pattern=='regen':
            self.regen()
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate': # place a tile inside the player's tile
            pass
        elif current_pattern == 'poison':
            sound_effects['water'].play()
            player.buffs['poison'] += 5
        self.proceed_next_pattern()
        self.end_my_turn()

    def get_heal_amount(self):
        return 10

class Snider(Enemy):
    def __init__(self, my_name = 'snider', hp=120, hpmax = 120, attack_damage = [4,16], pos = (332,mob_Y_level), attack_pattern = ['buff', 'attack', 'regen'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 7)
    '''
    This mob does random damage attack
    '''
    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['sword'].play()
                damage = random.randint(self.attack_damage[0], self.attack_damage[1])
                player.take_damage(self, damage*self.get_attack_multiplier())
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1
                # player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            pass
        elif current_pattern=='buff':
            sound_effects['water'].play()
            player.buffs['vulnerability'] += 3
            player.buffs['confusion'] += 3
        elif current_pattern=='regen':
            self.regen()
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass

        self.proceed_next_pattern()
        self.end_my_turn()

    def get_heal_amount(self):
        return 10



########################################################################### ruin enemies ###############################################################################
class Stem(Enemy):
    def __init__(self, my_name = 'stem', hp=12, hpmax = 12, attack_damage = 4, pos = (332,mob_Y_level), attack_pattern = ['infiltrate', 'lifesteal'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 1)

    '''
    This mob has life steal equal to its attack damage
    '''
    def get_description(self): # override
        return "A mob that can life steal"

    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='lifesteal':
            if self.can_attack:
                sound_effects['hard_hit'].play()
                player.take_damage(self,self.get_current_damage())
                self.enforced_regen(4)
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1

                # player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            pass
        elif current_pattern=='buff':
            pass
        elif current_pattern=='regen':
            pass
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate': # place a tile inside the player's tile
            player.board.insert_a_tile_on_board("Slime")

        self.proceed_next_pattern()
        self.end_my_turn()

class Golem(Enemy):
    def __init__(self, my_name = 'golem', hp=120, hpmax = 120, attack_damage = 20, pos = (332,mob_Y_level), attack_pattern = ['shield', 'attack', 'regen'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 20)

        self.base_defence = 4 #
    def get_description(self):  # override
        return "has 4 base defence"

    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['hard_hit'].play()
                player.take_damage(self,self.get_current_damage())
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1

                # player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            self.defence += 20
            self.update_defence()
        elif current_pattern=='buff':
            pass
        elif current_pattern=='regen':
            self.regen()
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate': # place a tile inside the player's tile
            sound_effects['water'].play()
            player.board.insert_a_tile_on_board("Slime")

        self.proceed_next_pattern()
        self.end_my_turn()

    def get_heal_amount(self):
        return 20


class Raider(Enemy):
    def __init__(self, my_name = 'raider', hp=80, hpmax = 80, attack_damage = [8,16], pos = (332,mob_Y_level), attack_pattern = ['poison','buff', 'attack', 'regen'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 15)
    '''
    This mob does random damage attack
    '''
    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['sword'].play()
                damage = random.randint(self.attack_damage[0], self.attack_damage[1])
                player.take_damage(self, damage*self.get_attack_multiplier())
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1
                # player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            pass
        elif current_pattern=='buff':
            player.buffs['weakness'] += 1
            player.buffs['vulnerability'] += 1
        elif current_pattern=='regen':
            self.regen()
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate': # place a tile inside the player's tile
            pass
        elif current_pattern == 'poison':
            player.buffs['poison'] += 3
        self.proceed_next_pattern()
        self.end_my_turn()

    def get_heal_amount(self):
        return 10


class Beast(Enemy):
    def __init__(self, my_name = 'beast', hp=24, hpmax = 24, attack_damage = 2, pos = (332,mob_Y_level), attack_pattern = ['attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 2)
        self.passive = True

        '''
        This mob gets stronger after attacking
        '''
    def get_description(self):
        return 'attack increases by 2 each turn after awakened'

    def behave(self, player, enemy = None):
        ready_to_behave = self.passive_behavior(player)
        if not ready_to_behave:
            return

        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['hit'].play()
                player.take_damage(self,self.get_current_damage())
                self.attack_damage += 2
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1
                # player.buffs['toxin'] = 1
                # player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            pass
        elif current_pattern=='buff':
            pass
        elif current_pattern=='regen':
            pass # no op
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate': # place a tile inside the player's tile
            pass

        self.proceed_next_pattern()
        self.end_my_turn()

class Shatter(Enemy):
    def __init__(self, my_name = 'shatter', hp=60, hpmax = 60, attack_damage = 15, pos = (332,mob_Y_level), attack_pattern = ['shield', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 12)
        self.passive = True

        self.base_defence = 2 #
        '''
        This mob gains attack when damaged
        '''

    def get_description(self):  # override
        return "has 2 base defence"

    def take_damage(self, attacker, damage_temp, no_fightback = False): # wake up when taken damage!
        super().take_damage(attacker, damage_temp,no_fightback)

        self.attack_damage += 5

    def behave(self, player, enemy = None):
        ready_to_behave = self.passive_behavior(player)
        if not ready_to_behave:
            return

        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['hard_hit'].play()
                player.take_damage(self,self.get_current_damage())
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1
                # player.buffs['toxin'] = 1
                # player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            self.defence += 10
            self.update_defence()
        elif current_pattern=='buff':
            pass
        elif current_pattern=='regen':
            pass # no op
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate': # place a tile inside the player's tile
            pass

        self.proceed_next_pattern()
        self.end_my_turn()


class Watcher(Enemy):
    def __init__(self, my_name = 'watcher', hp=400, hpmax = 400, attack_damage = 64, pos = (332,mob_Y_level), attack_pattern = ['infiltrate','buff', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 150)
        self.passive = True

        self.base_defence = 8 #
    def get_description(self):  # override
        return "Ruin boss: 8 base defence"
    def behave(self, player, enemy = None):
        ready_to_behave = self.passive_behavior(player)
        if not ready_to_behave:
            return

        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['lazer'].play()
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
            player.buffs['weakness'] += 1
            player.buffs['toxin'] += 1
        elif current_pattern=='regen':
            pass # no op
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate': # place a tile inside the player's tile
            sound_effects['water'].play()
            player.board.insert_a_tile_on_board("Slime")

        self.proceed_next_pattern()
        self.end_my_turn()

########################################################################### ruin enemies ###############################################################################




class Operator(Enemy):
    def __init__(self, my_name = 'operator', hp=150, hpmax = 150, attack_damage = 100, pos = (332,mob_Y_level), attack_pattern = [ 'shield', 'shield', 'shield','no op','attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 20)


    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['lazer'].play()
                player.take_damage(self,self.get_current_damage())
                # player.buffs['broken will'] = 1
                player.buffs['vulnerability'] = 1
                player.buffs['weakness'] = 1
                player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            sound_effects['railgun_reload'].play()
            time.sleep(0.1)
            self.buffs['vulnerability'] = 2
        elif current_pattern=='shield':
            self.defence += 32
            self.update_defence()
        elif current_pattern=='buff':
            pass
        elif current_pattern=='regen':
            pass # no op
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass

        self.proceed_next_pattern()
        self.end_my_turn()



class Guard(Enemy):
    def __init__(self, my_name = 'guard', hp=300, hpmax = 300, attack_damage = 25, pos = (332,mob_Y_level), attack_pattern = [ 'shield', 'shield','attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank, gold_reward = 15)


    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['hard_hit'].play()
                player.take_damage(self,self.get_current_damage())
                # player.buffs['broken will'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            self.defence += 64
            self.update_defence()
        elif current_pattern=='buff':
            pass
        elif current_pattern=='regen':
            pass # no op
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass

        self.proceed_next_pattern()
        self.end_my_turn()


class Ikarus(Enemy):
    def __init__(self, my_name = 'ikarus', hp=100, hpmax = 100, attack_damage = 60, pos = (332,mob_Y_level), attack_pattern = [ 'buff','attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank, gold_reward = 30)
        self.evade_damage_threshold = 30
    def get_description(self):  # override
        return "Evade if damage received is greater than %d"%self.evade_damage_threshold

    def take_damage(self, attacker, damage_temp, no_fightback = False): # wake up when taken damage!
        if damage_temp > self.evade_damage_threshold:
            sound_effects['dash'].play()
            return
        super().take_damage(attacker, damage_temp, no_fightback)

    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['playerdeath'].play()
                player.take_damage(self,self.get_current_damage())
                player.buffs['weakness'] = 2

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            pass
        elif current_pattern=='buff':
            player.buffs['vulnerability'] += 1
        elif current_pattern=='regen':
            pass # no op
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass

        self.proceed_next_pattern()
        self.end_my_turn()



class Wall(Enemy):
    def __init__(self, my_name = 'wall', hp=500, hpmax = 500, attack_damage = 25, pos = (332,mob_Y_level), attack_pattern = [ 'shield', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank, gold_reward = 20)

        self.taking_damage_threshold = 100

    def get_description(self):  # override
        return "Does not take more damage than %d per hit"%self.taking_damage_threshold

    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['hard_hit'].play()
                player.take_damage(self,self.get_current_damage())
                # player.buffs['broken will'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            for i in range(3):
                time.sleep(0.15)
                sound_effects['block'].play()
            self.defence += 999
            self.update_defence()
        elif current_pattern=='buff':
            pass
        elif current_pattern=='regen':
            pass # no op
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass

        self.proceed_next_pattern()
        self.end_my_turn()




################### 진화형 mobs

class Urchin(Enemy):
    def __init__(self, my_name = 'urchin', hp=200, hpmax = 200, attack_damage = 60, pos = (332,mob_Y_level), attack_pattern = ['no op','infiltrate','attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 30)
        self.thorny = True
    def get_description(self): # override
        return "Thorny: inflict half of the damage to attacker"

    def behave(self, player, enemy = None):
        ready_to_behave = self.passive_behavior(player)
        if not ready_to_behave:
            return

        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['hard_hit'].play()
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
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate': # place a tile inside the player's tile
            for i in range(3): # insert 3 spikes at once
                player.board.insert_a_tile_on_board("Spike")

        self.proceed_next_pattern()
        self.end_my_turn()


class Parasite(Enemy):
    def __init__(self, my_name = 'parasite', hp=240, hpmax = 240, attack_damage = 20, pos = (332,mob_Y_level), attack_pattern = ['no op','infiltrate','attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 20)

    def behave(self, player, enemy = None):
        ready_to_behave = self.passive_behavior(player)
        if not ready_to_behave:
            return

        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['water'].play()
                player.take_damage(self,self.get_current_damage())
                # print(self.health)
                player.buffs['weakness'] = 1
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
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate': # place a tile inside the player's tile
            for i in range(2):
                player.board.insert_a_tile_on_board("Proliferation")


        self.proceed_next_pattern()
        self.end_my_turn()









