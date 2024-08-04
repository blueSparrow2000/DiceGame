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


    def passive_behavior(self, player):
        if self.passive and self.passive_to_aggressive: # change passive to aggresive
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


    def take_damage(self, attacker, damage_temp): # wake up when taken damage!
        super().take_damage(attacker, damage_temp)
        self.passive_to_aggressive = True

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

        if self.passive:
            current_pattern = 'no op'

        # next_move_img = self.pattern_image[self.pattern_analyzer[current_pattern]]
        next_move_img = self.pattern_image[current_pattern]
        screen.blit(next_move_img, next_move_img.get_rect(center=self.next_move_loc))


        description = ""
        if current_pattern == 'attack':
            if isinstance(self.attack_damage, list):
                description = "%d~%d" %(self.attack_damage[0],self.attack_damage[1])
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
    def __init__(self, my_name = 'halo', hp=999, hpmax = 999, attack_damage = 32, pos = (332,mob_Y_level), attack_pattern = ['unknown', 'buff', 'attack','regen'], rank = 1 ):
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 999)

    def behave(self, player, enemy = None):
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
        elif current_pattern=='unknown':
            player.buffs['broken will'] = 1
        elif current_pattern == 'summon':
            pass

        self.proceed_next_pattern()

        self.end_my_turn()
        time.sleep(0.2)

    def get_heal_amount(self):
        return 15


class Mob(Enemy):
    def __init__(self, my_name = 'mob', hp=20, hpmax = 20, attack_damage = 5, pos = (332,mob_Y_level), attack_pattern = ['shield', 'buff', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 1)

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
            self.buffs['strength'] = 2 # for one turn since it is self buffing
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
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 2)
        self.thorny = True

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
    def __init__(self, my_name = 'lenz', hp=30, hpmax = 30, attack_damage = 3, pos = (332,mob_Y_level), attack_pattern = ['no op','summon', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 2)


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
    def __init__(self, my_name = 'embryo', hp=16, hpmax = 16, attack_damage = 3, pos = (332,mob_Y_level), attack_pattern = ['no op','infiltrate'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 3)

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
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 4)

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
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 6)


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
            player.buffs['vulnerability'] = 1
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
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 10)


    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='hard_hit':
            if self.can_attack:
                sound_effects['sword'].play()
                player.take_damage(self,self.get_current_damage())
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1

                # player.buffs['confusion'] = 1

        elif current_pattern=='no op':
            pass # no op
        elif current_pattern=='shield':
            for entity in enemy:
                entity.defence += 16
                entity.update_defence()
        elif current_pattern=='buff':
            player.buffs['weakness'] = 1
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
    def __init__(self, my_name = 'observer', hp=64, hpmax = 64, attack_damage = 32, pos = (332,mob_Y_level), attack_pattern = ['buff',  'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 10)


    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='hard_hit':
            if self.can_attack:
                sound_effects['sword'].play()
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
            player.buffs['vulnerability'] = 1
        elif current_pattern=='regen':
            pass
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass

        self.proceed_next_pattern()
        self.end_my_turn()



class Carrier(Enemy):
    def __init__(self, my_name = 'carrier', hp=200, hpmax = 200, attack_damage = 20, pos = (332,mob_Y_level), attack_pattern = ['summon','shield', 'regen','attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 50)


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
            self.defence += 100
            self.update_defence()
        elif current_pattern=='buff':
            pass
        elif current_pattern=='regen': # heal all allies
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


############################################### ruin enemies #############################################################
class Stem(Enemy):
    def __init__(self, my_name = 'stem', hp=12, hpmax = 12, attack_damage = 6, pos = (332,mob_Y_level), attack_pattern = ['infiltrate', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 1)

    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['hard_hit'].play()
                player.take_damage(self,self.get_current_damage())
                self.enforced_regen(6)
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
    def __init__(self, my_name = 'golem', hp=50, hpmax = 50, attack_damage = 20, pos = (332,mob_Y_level), attack_pattern = ['shield', 'attack', 'regen'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 15)

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
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 10)
    '''
    This mob does random damage attack
    '''
    def behave(self, player, enemy = None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]
        if current_pattern=='attack':
            if self.can_attack:
                sound_effects['sword'].play()
                damage = random.randrange(self.attack_damage[0], self.attack_damage[1])
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
            player.buffs['weakness'] = 1
            player.buffs['vulnerability'] = 1
        elif current_pattern=='regen':
            self.regen()
        elif current_pattern=='unknown':
            pass # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate': # place a tile inside the player's tile
            pass
        elif current_pattern == 'poison':
            player.buffs['poison'] = 3
        self.proceed_next_pattern()
        self.end_my_turn()

    def get_heal_amount(self):
        return 10


class Beast(Enemy):
    def __init__(self, my_name = 'beast', hp=32, hpmax = 32, attack_damage = 6, pos = (332,mob_Y_level), attack_pattern = ['attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 2)
        self.passive = True

        '''
        This mob gets stronger after attacking
        '''
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
    def __init__(self, my_name = 'shatter', hp=100, hpmax = 100, attack_damage = 15, pos = (332,mob_Y_level), attack_pattern = ['shield', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 12)
        self.passive = True
        '''
        This mob gains attack when damaged
        '''
    def take_damage(self, attacker, damage_temp): # wake up when taken damage!
        super().take_damage(attacker, damage_temp)

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
    def __init__(self, my_name = 'watcher', hp=300, hpmax = 300, attack_damage = 20, pos = (332,mob_Y_level), attack_pattern = ['infiltrate','buff', 'attack'] , rank = 1 ): #
        super().__init__(my_name,hp,hpmax,attack_damage,pos,attack_pattern, rank,gold_reward = 50)
        self.passive = True

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
            player.buffs['weakness'] = 1
            player.buffs['toxin'] = 1
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


class Silent(Enemy):
    def __init__(self, my_name='silent', hp=500, hpmax=500, attack_damage=[32, 64], pos=(332, mob_Y_level),
                 attack_pattern=['shield', 'buff', 'attack', 'regen'], rank=1):  #
        super().__init__(my_name, hp, hpmax, attack_damage, pos, attack_pattern, rank, gold_reward=100)

    '''
    This mob does not show you what it will do (randomly chosen)
    '''

    def behave(self, player, enemy=None):
        self.refresh_my_turn()

        current_pattern = self.pattern[self.current_pattern_idx]

        if current_pattern == 'attack':
            if self.can_attack:
                sound_effects['water'].play()
                damage = random.randrange(self.attack_damage[0], self.attack_damage[1])
                player.take_damage(self, damage * self.get_attack_multiplier())
                # print(self.health)
                # player.buffs['broken will'] = 1
                # player.buffs['strength'] = 1
                # player.buffs['confusion'] = 1

        elif current_pattern == 'no op':
            pass  # no op
        elif current_pattern == 'shield':
            self.defence += 32
            self.update_defence()
        elif current_pattern == 'buff':
            player.buffs['weakness'] = 3
            player.buffs['vulnerability'] = 3
            player.buffs['toxin'] = 3
        elif current_pattern == 'regen':
            self.regen()
        elif current_pattern == 'unknown':
            pass  # no op
        elif current_pattern == 'summon':
            pass
        elif current_pattern == 'infiltrate':  # place a tile inside the player's tile
            pass
        elif current_pattern == 'poison':
            pass

        # next pattern is randomized
        self.proceed_next_pattern()
        self.end_my_turn()

    def proceed_next_pattern(self):
        # self.current_pattern_idx = (self.current_pattern_idx + 1) % self.num_of_patterns
        self.current_pattern_idx = random.randrange(0, len(self.pattern) - 1)  # random pattern
    def get_heal_amount(self):
        return 16

    def show_next_move(self,screen,mousepos):
        if self.health < 250: # phase two
            next_move_img = self.pattern_image['unknown']
            screen.blit(next_move_img, next_move_img.get_rect(center=self.next_move_loc))

            if check_inside_button(mousepos, self.next_move_loc, self.icon_delta // 2):  # if mouse is pointing to the relic
                write_text(screen, width // 2, turn_text_level + self.icon_delta, "what will it do?", 17, "white", 'black')
        else:
            super().show_next_move(screen,mousepos)

