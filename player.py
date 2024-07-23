from entity import *


class Player(Entity):
    def __init__(self, character_name,character_skills): # tile_dict
        global mob_Y_level, sound_effects, tile_names ,requirement_level# all the other skills should also be contained
        super().__init__(character_name, 100, 100, (100,mob_Y_level))
        ####################### player only stuffs ############################
        self.current_tile = dict()
        self.current_skill_idx = -1
        self.tile_dict = {'Attack':6, 'Defence':6, 'Regen':6, 'Skill':6} ########## this should be given as input for multi characters
        self.skill_book = character_skills

        ######################################## buttons
        self.buttons = ['Attack', 'Defence','Regen']
        self.button_images = []
        self.image_button_tolerance = 25
        for button_name in self.buttons:
            self.button_images.append(load_image("%s" % button_name))
        self.button_spacing = 120
        self.button_x = 240
        self.button_y = 460
        self.button_locations=[( self.button_x + (i-1)*self.button_spacing, self.button_y) for i in range(len(self.buttons))]

        self.mini_tiles = list(tile_names)
        self.mini_tile_icons = dict()
        for mini_tile in self.mini_tiles:
            self.mini_tile_icons[mini_tile] = (load_image("icons/mini_tile/%s" % mini_tile))
        self.minitile_x = 240
        self.minitile_y = 920
        self.minitile_spacing = 50
        self.minitile_not_shown = ['Used', 'Empty','Unusable'] # should not show these tiles

        self.required_tiles = dict()
        self.required_tile_x = 200
        self.required_tile_y = requirement_level + 30
        self.requirement_spacing = 25

    def initialize_step_1(self):
        self.required_tiles = dict()

    def my_turn_lookahead(self, mousepos): # show details of each skill / basic attacks
        for i in range(len(self.buttons)):
            current_button = self.buttons[i]
            if check_inside_button(mousepos, self.button_locations[i], self.image_button_tolerance):
                if (current_button == 'Attack'):
                    if self.can_attack:
                        self.required_tiles = dict()
                        return 'Attack|Attack one target with {} damage'.format(self.get_current_damage()) # string content!
                elif (current_button=='Defence'):
                    self.required_tiles = dict()
                    return 'Defence|Gain {} temporal defence'.format(self.get_defence_gain())
                elif (current_button == 'Regen'):
                    self.required_tiles = dict()
                    return 'Regeneration|Heal {} health'.format(self.get_heal_amount())

        # else, check whether skill
        for i in range(len(self.skill_book.skill_images)):
            if check_inside_button(mousepos, self.skill_book.button_locations[i], self.skill_book.image_button_tolerance):
                _,_,_, self.required_tiles = getattr(self.skill_book, self.skill_book.skills[
                    i] + '_get_requirement')(self)

                return getattr(self.skill_book, "get_detail_%s"%self.skill_book.skills[i])(self)

        return None

    def show_required_tiles(self,screen):
        cnt = 0
        for req_tile_name,req_range in self.required_tiles.items():
            content = " %d ~ %d " % req_range

            if not req_range[0]:
                content = "   ~ %d "%req_range[1]
            elif not req_range[1]:
                content = " %d ~   " % req_range[0]

            screen.blit(self.mini_tile_icons[req_tile_name], self.mini_tile_icons[req_tile_name].get_rect(center= (self.required_tile_x, self.required_tile_y + cnt * self.requirement_spacing) ))
            write_text(screen, self.required_tile_x + 40, self.required_tile_y + cnt * self.requirement_spacing,content , 20)

            cnt+=1


    def show_current_tiles(self,screen):
        mini_tile_list = []
        for tile_name, amount in self.current_tile.items():
            if tile_name not in self.minitile_not_shown:
                for i in range(amount):
                    mini_tile_list.append(tile_name)

        minitile_numbers = len(mini_tile_list)
        self.minitile_x = 240 - (minitile_numbers - 1) * (self.minitile_spacing) / 2
        for i in range(minitile_numbers):
            screen.blit(self.mini_tile_icons[mini_tile_list[i]], self.mini_tile_icons[mini_tile_list[i]].get_rect(center= (self.minitile_x + i * self.minitile_spacing, self.minitile_y) ))

    def draw_buttons(self,screen):
        for i in range(len(self.buttons)):
            if (self.buttons[i]=='Attack'):
                if self.can_attack:
                    screen.blit(self.button_images[i], self.button_images[i].get_rect(center=self.button_locations[i]))
                # else draw nothing!
            else:
                screen.blit(self.button_images[i], self.button_images[i].get_rect(center=self.button_locations[i]))

    def check_activate_button(self,mousepos):
        for i in range(len(self.buttons)):
            current_button = self.buttons[i]
            if check_inside_button(mousepos, self.button_locations[i], self.image_button_tolerance):
                if (current_button == 'Attack'):
                    # attack button
                    if self.can_attack:
                        return False, 2, 1 # need to go to next step, step 2, choose one target
                elif (current_button=='Defence'):
                    # defence button
                    self.defend()
                    return True, 1,0 # end turn
                elif (current_button == 'Regen'):
                    # regen button
                    self.regen()
                    return True, 1, 0 # end turn


        return False,1 ,0 #process_completed (end player turn right away flag), player_turn_step (currently 1), number_of_targets_to_specify (any is fine. default 1)


    def end_my_turn(self): # do something at the end of the turn
        super().end_my_turn()
        self.current_skill_idx = -1 # reset this
        self.current_tile = dict()


    def new_fight(self):
        for k,v in self.buffs.items():
            self.buffs[k] = 0 # reset
        self.defence = 0
        self.update_defence()
        self.current_tile = dict()
        self.current_skill_idx = -1


    def push_tile_infos(self,tile_info):
        self.current_tile = tile_info


    def count_tile(self,name):
        for k,v in self.current_tile.items():
            if k==name:
                return v
        #print("ERROR: no such name exists: ", name)
        return 0

    def P(self,num):
        return 2**(num-1)

    def attack(self, target_list):
        sound_effects['sword'].play()
        for enemy in target_list:
            # enemy.take_damage(100)
            counter_attack_damage = enemy.take_damage(self.get_current_damage())
            self.health -= counter_attack_damage
            # enemy.buffs['broken will'] = 1
            # enemy.buffs['strength'] = 1
            # enemy.buffs['poison'] = 1

    def get_current_damage(self):
        # count number of attack tiles
        A = self.count_tile('Attack')
        return self.P(A)*self.get_attack_multiplier()

    def defend(self):
        self.defence += self.get_defence_gain()
        self.update_defence()

    def get_defence_gain(self):
        # count number of defence tiles
        D = self.count_tile('Defence')
        return self.P(D)*self.defence_gain_multiplier

    def regen(self):
        self.health = min(self.max_health,self.health+self.get_heal_amount())

    def get_heal_amount(self):
        # count number of regen tiles
        R = self.count_tile('Regen')
        return self.heal_multiplier*self.P(R)

    def skill_ready(self, idx): # use the idx'th skill
        # global requirement: Need at least one skill tile to use skill
        S = self.count_tile('Skill')
        if ( S <= idx//2 ): # check skill requirement
            return False, 1

        # self.can_attack 확인하기. 공격하는 스킬의 경우 can attack일때만 valid하다
        skill_valid, target_nums,is_attack,_ = getattr(self.skill_book, self.skill_book.skills[idx]+'_get_requirement')(self)
        if skill_valid and ((not is_attack) or (is_attack and self.can_attack)):
            # if valid, change the skill index to idx
            self.current_skill_idx = idx
            return skill_valid,target_nums
        return False,1

    def use_skill(self, target_list): # use the idx'th skill
        # before skill

        getattr(self.skill_book,self.skill_book.skills[self.current_skill_idx])(self,target_list)

        # after skill



