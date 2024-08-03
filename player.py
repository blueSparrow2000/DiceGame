from entity import *
import copy
from skill_book import character_max_hp
from relic import *


class Player(Entity):
    def __init__(self, character_name,character_skills, board): # tile_dict
        global mob_Y_level, sound_effects, tile_names ,requirement_level , joker_transformable_tiles, character_max_hp , mini_tile_icons    # all the other skills should also be contained

        hpmax = character_max_hp[character_name]
        super().__init__(character_name, hpmax, hpmax, (100,mob_Y_level))
        self.my_type = 'player'
        ####################### player only stuffs ############################
        self.current_tile = dict()
        self.board = board

        self.skill_book = character_skills # get a skill book
        self.max_num_of_skills = 6 # number of skills that player can have
        self.current_skills = copy.deepcopy(self.skill_book.character_skills) # at first, player can use all the skills in the character's skill book
        self.temp_current_skills = copy.deepcopy(self.current_skills)
        self.current_skill_idx = -1

        ######################################## buttons
        self.buttons = ['Attack', 'Defence','Regen']
        self.button_images = []
        self.image_button_tolerance = 25
        for button_name in self.buttons:
            self.button_images.append(load_image("tiles/%s" % button_name))
        self.button_spacing = 120
        self.button_x = width//2
        self.button_y = 460
        self.button_locations=[( self.button_x + (i-1)*self.button_spacing, self.button_y) for i in range(len(self.buttons))]

        self.mini_tiles = list(tile_names)
        self.mini_tile_icons = mini_tile_icons
        # for mini_tile in self.mini_tiles:
        #     self.mini_tile_icons[mini_tile] = (load_image("tiles/mini_tile/%s" % mini_tile))
        self.minitile_x = width//2
        self.minitile_y = height-40
        self.minitile_spacing = 50
        self.minitile_size = self.mini_tile_icons['Attack'].get_height()
        self.minitile_not_shown = ['Used', 'Empty','Unusable'] # should not show these tiles

        self.required_tiles = dict()
        self.required_tile_x = width//2 - 40
        self.required_tile_y = requirement_level + 30
        self.requirement_spacing = 25

        ### game variables
        self.current_depth = 0
        self.golds = 10
        self.items=[]
        self.giant_HP_width = 30
        self.giant_HP_pos = [width//2,self.giant_HP_width//2]
        self.killed_enemies = 0
        self.boss_stage = 0
        self.killed_watcher = False

        # transform button attributes
        self.transformable_tiles = joker_transformable_tiles #'Joker' is not transformed into joker
        self.transform_x = width//2 - 40
        self.transform_y = 870
        self.transform_spacing = 50
        self.transform_tolerance = 15
        self.transform_icon_locations = [( self.transform_x + (i-1)*self.transform_spacing,self.transform_y) for i in range(len(self.transformable_tiles))]


        ######################################## buttons
        self.relics = [] # PoisonBottle(),SerpentHeart(), StemCell(), FearCell(), # [PoisonBottle() for i in range(20)]

        self.max_relic_in_a_row = 12
        self.relic_y_start = 95
        self.relic_delta = 30





    ######################################### Relic ################################################

    def pick_up_relic(self, relic_obj):
        self.relics.append(relic_obj)
        relic_obj.effect_when_first_obtained(self)


    ######################################### Relic ################################################
    '''
    Handling Joker tiles
    
    '''
    def transform_tile(self, transformed_tile_name):
        # remove one joker
        safe_delete_dict_one(self.current_tile, 'Joker')
        safe_tile_add_one(self.current_tile, transformed_tile_name)


    def tile_transform_button(self,mousepos):
        if not self.check_exists_in_current_tile('Joker'):
            return

        for i in range(len(self.transformable_tiles)):
            if check_inside_button(mousepos, self.transform_icon_locations[i], self.transform_tolerance):
                current_tile = self.transformable_tiles[i]
                self.transform_tile(current_tile)
                break # get out if done


    def draw_tile_transform_button(self,screen):
        if not self.check_exists_in_current_tile('Joker'):
            return

        write_text(screen, width//2, self.transform_y - 30, "choose a tile", 15, color='darkgoldenrod')

        cnt = 0
        for mini_tile in self.transformable_tiles: # draw transform tiles in order
            screen.blit(self.mini_tile_icons[mini_tile], self.mini_tile_icons[mini_tile].get_rect(center=self.transform_icon_locations[cnt]))
            cnt+=1

    '''
    current(selected) tile functions
    '''
    def show_current_tiles(self, screen, mousepos):
        # background
        draw_bar(screen, width//2, self.minitile_y, 312, 50, 100, (120, 120, 120))
        draw_bar(screen, width//2, self.minitile_y, 300, 38, 100, (150, 150, 150))

        mini_tile_list = []
        for tile_name, amount in self.current_tile.items():
            if tile_name not in self.minitile_not_shown:
                for i in range(amount):
                    mini_tile_list.append(tile_name)

        minitile_numbers = len(mini_tile_list)
        self.minitile_x = width//2 - (minitile_numbers - 1) * (self.minitile_spacing) / 2
        for i in range(minitile_numbers):
            minitile_name = mini_tile_list[i]
            minitile_location = [self.minitile_x + i * self.minitile_spacing, self.minitile_y]
            screen.blit(self.mini_tile_icons[minitile_name], self.mini_tile_icons[minitile_name].get_rect(
                center=minitile_location))

            if check_inside_button(mousepos, minitile_location, self.minitile_size//2): # if mouse is pointing to the relic
                write_text(screen, width//2,self.minitile_y - 32, tile_name_description_dic[minitile_name], 15, "white", 'black')
                write_text(screen, width//2,self.minitile_y - 48, "[ %s tile ]"%minitile_name, 17, "white", 'black')


    def check_exists_in_current_tile(self, tile_name):
        return tile_name in self.current_tile and self.current_tile[tile_name] > 0 # if such tile exists and is having more than one

    '''
    Handling Skills/basic moves 
    
    '''
    def draw_buttons(self, screen): # can click only if current tile exists
        for i in range(len(self.buttons)):
            if not self.check_exists_in_current_tile(self.buttons[i]):
                continue # pass to check next button

            if (self.buttons[i] == 'Attack'):
                if self.can_attack:
                    screen.blit(self.button_images[i], self.button_images[i].get_rect(center=self.button_locations[i]))
                # else draw nothing!
            else:
                screen.blit(self.button_images[i], self.button_images[i].get_rect(center=self.button_locations[i]))

    def check_activate_button(self, mousepos):
        for i in range(len(self.buttons)):
            current_button = self.buttons[i]
            if not self.check_exists_in_current_tile(current_button):
                continue # pass to check next button
            if check_inside_button(mousepos, self.button_locations[i], self.image_button_tolerance):
                if (current_button == 'Attack'):
                    # attack button
                    if self.can_attack:
                        return False, 2, 1  # need to go to next step, step 2, choose one target
                elif (current_button == 'Defence'):
                    # defence button
                    self.defend()
                    return True, 1, 0  # end turn
                elif (current_button == 'Regen'):
                    # regen button
                    self.regen()
                    return True, 1, 0  # end turn

        return False, 1, 0  # process_completed (end player turn right away flag), player_turn_step (currently 1), number_of_targets_to_specify (any is fine. default 1)

    def get_gold(self, amount):
        final_amount = amount
        for relic in self.relics:
            final_amount = relic.activate_when_getting_reward_gold(final_amount)

        self.golds += final_amount
        return final_amount

    def pay_gold(self, amount):
        if self.can_buy(amount):
            self.golds -= amount
            return True

        # print("not enough gold!")
        return False

    def can_buy(self, amount):
        return self.golds >= amount

    def get_drop(self, drop_list):
        self.items.extend(drop_list)


    def update_depth(self, amount):
        if self.reached_max_depth(): # do not update
            return
        self.current_depth -= amount
        if self.current_depth <= MAX_DEPTH:
            self.current_depth = 'LIMIT'

    def reached_max_depth(self):
        return self.current_depth=='LIMIT'

    def check_ruin_boss(self):
        return (not self.killed_watcher) and self.current_depth <= WATCHER_DEPTH

    def check_primary_boss(self):
        return self.boss_stage == 0 and self.current_depth <= PRIMARY_BOSS_DEPTH

    def check_secondary_boss(self):
        return self.boss_stage == 1 and self.current_depth <= SECONDARY_BOSS_DEPTH

    def proceed_next_boss_stage(self):
        self.boss_stage += 1

    def set_max_health(self,max_health):
        self.max_health = max_health
        if self.health > self.max_health:
            self.health = self.max_health

    def draw_player_info_top(self,screen, mousepos):

        draw_bar(screen, self.giant_HP_pos[0], self.giant_HP_pos[1], width, self.giant_HP_width, 100, 'silver')

        draw_health = self.max_health
        if self.max_health<=0:
            draw_health = 1

        draw_bar(screen, self.giant_HP_pos[0], self.giant_HP_pos[1], width, self.giant_HP_width, 100 * self.health / draw_health, 'coral')
        draw_bar(screen, self.giant_HP_pos[0], self.giant_HP_width , width, 5, 100, 'gray')

        write_text(screen, width - 40, self.giant_HP_pos[1], "%d/%d" % (self.health, self.max_health), 20, 'maroon')
        write_text(screen, 80,self.giant_HP_width//2+5, self.my_name,30, darker_gold)

        # depth
        if self.reached_max_depth():
            write_text(screen, width - 60, self.giant_HP_width * 2, " %s " % self.current_depth, 30, 'black')
        else:
            write_text(screen, width - 60,self.giant_HP_width *2, " %3d m"%self.current_depth,30, 'black')

        # gold
        write_text(screen, 60,self.giant_HP_width*2, "Gold %3d g"%self.golds,20, 'gold')

        # relics
        cnt = 0
        next_row = 0
        for relic in self.relics:
            if cnt >= self.max_relic_in_a_row:
                next_row += 1
                cnt = 0
            location = (20 + (self.relic_delta  + 10) * cnt, self.relic_y_start + next_row * (self.relic_delta + 5))
            relic.draw(screen, location)
            if check_inside_button(mousepos, location, self.relic_delta//2): # if mouse is pointing to the relic
                relic_effects = relic.description()
                write_text(screen, width//2, self.relic_y_start - 35, relic_effects, 17, relic.color, 'black')
                write_text(screen, width // 2, self.relic_y_start - 52, relic.name, 20, relic.color, 'black')

            cnt += 1

    def initialize_step_1(self):
        self.required_tiles = dict()

    ############################################################## skill book 공사 ##############################################################
    '''
    Skill change interface

    On mousebutton up, call replace_current_skill
    On the drawing, call draw_skill_to_swap & draw_skill_to_learn
    '''
    def replace_current_skill(self,mousepos,skill_to_learn): # called when clicked
        idx = self.check_skill_button(mousepos)
        if not self.check_valid_skill_index(idx):
            return False

        # replace the skill!
        self.reset_replacement_of_skill()
        self.temp_current_skills[idx] = skill_to_learn # at first, player can use all the skills in the character's skill book

    def draw_skill_to_learn(self,screen, skill_to_learn): # skill_to_learn: string of skill name
        # draw skill to learn
        display_location = [width // 2 , turn_text_level + 30]
        self.skill_book.draw_skill_on_custom_location(screen, skill_to_learn, display_location)
        # else, check whether skill
        skill_detail = getattr(self.skill_book, "get_detail_%s"%skill_to_learn)(self)
        write_text_description(screen, width // 2, turn_text_level + 120, skill_detail, 15, bg_color = None, requirement_shown = True, requirement_pos = [width // 2, turn_text_level + 170] )

    def draw_skill_to_swap(self,screen):
        # draw existing skills
        write_text(screen, self.button_x,self.button_y + 50, "Choose a skill to replace", 20, 'darkgoldenrod')
        self.draw_skills(screen, self.temp_current_skills)

    def check_valid_skill_index(self,idx): # also covers case when idx == -1
        return 0<= idx <= self.max_num_of_skills -1

    def confirm_skill_replacement(self):
        changed_flag = False
        for i in range(len(self.temp_current_skills)):
            if not self.temp_current_skills[i] == self.current_skills[i]:
                changed_flag = True
        self.current_skills = copy.deepcopy(self.temp_current_skills)

        return changed_flag

    def reset_replacement_of_skill(self):
        self.temp_current_skills = copy.deepcopy(self.current_skills)

    def remove_one_skill_from_highest_index(self):
        if self.max_num_of_skills <= 0:
            print("There are no skills left to remove!")
            return
        self.max_num_of_skills -= 1
        self.current_skills = copy.deepcopy(self.current_skills[:self.max_num_of_skills]) # at first, player can use all the skills in the character's skill book
        self.temp_current_skills = copy.deepcopy(self.current_skills)
    '''
    Skill change interface
    '''

    def draw_skills(self,screen, temporary_skill_list = None):
        if temporary_skill_list:
            for i in range(len(temporary_skill_list)):
                skill_name = temporary_skill_list[i]
                self.skill_book.draw_skill(screen, skill_name, i)
        else:
            for i in range(len(self.current_skills)):
                skill_name = self.current_skills[i]
                self.skill_book.draw_skill(screen, skill_name, i)


    def check_skill_button(self,mousepos):
        for i in range(len(self.current_skills)):
            if self.skill_book.check_button(mousepos,i):
                return i # return the index of the clicked skill to use

        # no skills selected
        return -1

    def skill_ready(self, idx): # use the idx'th skill
        # global requirement: Need at least one skill tile to use skill

        # self.can_attack 확인하기. 공격하는 스킬의 경우 can attack일때만 valid하다
        skill_valid, target_nums,is_attack,requirement_dict = getattr(self.skill_book, self.current_skills[idx]+'_get_requirement')(self)

        if skill_valid and ((not is_attack) or (is_attack and self.can_attack)):
            # if valid, change the skill index to idx
            self.current_skill_idx = idx
            return skill_valid,target_nums
        return False,1

    def use_skill(self, target_list): # use the idx'th skill
        # before skill

        getattr(self.skill_book,self.current_skills[self.current_skill_idx])(self,target_list)

        # after skill


    def my_turn_lookahead(self, mousepos): # show details of each skill / basic attacks
        for i in range(len(self.buttons)):
            current_button = self.buttons[i]
            if not self.check_exists_in_current_tile(current_button):
                continue # pass to check next button
            if check_inside_button(mousepos, self.button_locations[i], self.image_button_tolerance):
                if (current_button == 'Attack'):
                    if self.can_attack:
                        self.initialize_step_1()
                        return 'Attack|Attack one target with %d damage'%(self.get_current_damage()) # string content!
                elif (current_button=='Defence'):
                    self.initialize_step_1()
                    return 'Defence|Gain %d temporal defence'%(self.get_defence_gain())
                elif (current_button == 'Regen'):
                    self.initialize_step_1()
                    return 'Regeneration|Heal %d health'%(self.get_heal_amount())

        # else, check whether skill
        for i in range(len(self.current_skills)):
            if self.skill_book.check_button(mousepos,i):
                _,_,_, self.required_tiles = getattr(self.skill_book, self.current_skills[i] + '_get_requirement')(self)
                return getattr(self.skill_book, "get_detail_%s"%self.current_skills[i])(self)

        return None


    ############################################################## skill book 공사 ##############################################################


    def show_required_tiles(self,screen):
        self.skill_book.show_requirement_mini_tiles(screen, (self.required_tile_x, self.required_tile_y), "", requirement_dict_given=self.required_tiles)

        # cnt = 0
        # for req_tile_name,req_range in self.required_tiles.items():
        #     content = " %d ~ %d " % req_range
        #
        #     if not req_range[0]:
        #         content = "   ~ %d "%req_range[1]
        #     elif not req_range[1]:
        #         content = " %d ~   " % req_range[0]
        #
        #     screen.blit(self.mini_tile_icons[req_tile_name], self.mini_tile_icons[req_tile_name].get_rect(center= (self.required_tile_x, self.required_tile_y + cnt * self.requirement_spacing) ))
        #     write_text(screen, self.required_tile_x + 40, self.required_tile_y + cnt * self.requirement_spacing,content , 20)
        #
        #     cnt+=1

    def refresh_my_turn(self):
        super().refresh_my_turn()
        for relic in self.relics:
            relic.fight_every_turn_beginning_effect(self)

    def end_my_turn(self): # do something at the end of the turn
        super().end_my_turn()

        copy_of_current_tile = copy.deepcopy(self.current_tile)
        # SHUFFLE: this is activated when pressed skip button
        self.board.turn_end_check(self, copy_of_current_tile)

        for relic in self.relics:
            relic.fight_every_turn_end_effect(self)

        self.current_skill_idx = -1  # reset this
        self.current_tile = dict()
        time.sleep(0.3)

    def new_fight(self):
        for k,v in self.buffs.items():
            self.buffs[k] = 0 # reset
        # self.defence = 0
        # self.update_defence()
        self.current_tile = dict()
        self.current_skill_idx = -1

        # reset the board
        self.board.new_game()

        for relic in self.relics:
            relic.fight_start_effect(self)


    def on_enemy_death(self, enemy):
        for relic in self.relics:
            relic.activate_on_kill(self, enemy)

        self.killed_enemies += 1


    def push_tile_infos(self,tile_info):
        self.current_tile = tile_info


    def count_tile(self,name):
        for k,v in self.current_tile.items():
            if k==name:
                return v
        #print("ERROR: no such name exists: ", name)
        return 0

    def P(self,num):
        return 2**(num)

    def attack(self, target_list):
        sound_effects['sword'].play()
        for enemy in target_list:
            # enemy.take_damage(100)
            enemy.take_damage(self,self.get_current_damage())
            # enemy.buffs['broken will'] = 1
            # enemy.buffs['strength'] = 1
            # enemy.buffs['poison'] = 1

    def take_damage(self, attacker, damage_temp):
        super().take_damage(attacker, damage_temp)
        # player only stuffs (like relic effects)
        for relic in self.relics:
            relic.activate_on_taking_damage(self, attacker,damage_temp)


    def get_attack_multiplier(self):
        base_multiplier = self.strength_multiplier*self.strength_deplifier
        Chained = self.count_tile('Chained') # chained tile reduces half damage gain
        if Chained:
            base_multiplier = base_multiplier/2

        return base_multiplier

    def get_current_damage(self):
        # count number of attack tiles
        A = self.count_tile('Attack')
        damage = self.P(A)*self.get_attack_multiplier()
        return damage

    def defend(self):
        self.defence += self.get_defence_gain()
        self.update_defence()

    def get_defence_gain(self):
        # count number of defence tiles
        D = self.count_tile('Defence')
        return self.P(D)*self.defence_gain_multiplier

    def get_heal_amount(self):
        # count number of regen tiles
        R = self.count_tile('Regen')
        return self.heal_multiplier*self.P(R)


    def death_check(self):
        if not super().death_check(): # returns False when not dead
            return False

        # on death

        # relic effect from death check
        for relic in self.relics:
            relic.activate_on_death(self)

        self.relics[:] = [relic for relic in self.relics if not relic.delete]
        return True
