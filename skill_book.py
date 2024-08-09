'''
GLOBAL REQUIREMENT FOR SKILL
Note that one needs at least one skill tile to use skill > Checked inside player's 'skill ready'

N 명의 적에게 적용되는 공격은 이미 target_list에 적용이 된 상태다. 스킬을 쓸땐 고려하지 않아도 된다. 리스트 순회만 하면 끝

'''

from util import *
from entity import Entity
from board import Board

class DummyPlayer(Entity):
    def __init__(self):
        super().__init__("dummy_player", 100, 100, (100, mob_Y_level))
        global character_skill_dictionary ,character_tile_dictionary
        self.character_skill_dictionary = character_skill_dictionary
        self.character_tile_dictionary = character_tile_dictionary

        self.char_name = 'Mirinae' # default
        self.skill_book = self.character_skill_dictionary[self.char_name]
        self.char_skills = self.skill_book.character_skills
        self.char_tiles = self.character_tile_dictionary[self.char_name]
        self.board = Board(self.char_tiles, [0,1])
        self.hpmax_for_drawing = character_max_hp[self.char_name]

        self.requirement_location = [width // 2 - 40, requirement_level + 30]
        self.character_info_location = [width // 2,middle_button_Y_level]
        self.tile_info_location = [width // 2, middle_button_Y_level + 60]


        self.char_tiles_list = list(self.char_tiles.keys())
        image_button_tolerance = 25
        image_button_spacing = 10
        self.tile_img_locations = [
            (40 + (2 * image_button_tolerance + image_button_spacing + 20) * i, self.tile_info_location[1]) for i in
            range(len(self.char_tiles_list))]

        self.tile_image_dict = dict()
        for tile_name in self.char_tiles_list:
            self.tile_image_dict[tile_name] = load_image("tiles/%s" % tile_name)

        self.heart = load_image("icons/HP")

    def P(self,num):
        return 2**(num)


    def update_char(self,character): # must be called every time when character selection changes
        self.char_name = character
        self.skill_book = self.character_skill_dictionary[self.char_name]
        self.char_skills = self.skill_book.character_skills
        self.char_tiles = self.character_tile_dictionary[self.char_name]
        self.char_tiles_list = list(self.char_tiles.keys())
        self.hpmax_for_drawing = character_max_hp[self.char_name]

    def count_tile(self, name):
        return 0

    def draw_character(self,screen,mousepos):
        self.draw_skills(screen,mousepos)
        self.draw_tiles(screen)
        self.draw_character_description(screen)


    def draw_skills(self,screen,mousepos):
        for i in range(len(self.char_skills)):
            skill_name = self.char_skills[i]
            self.skill_book.draw_skill(screen, skill_name, i)

        for i in range(len(self.char_skills)):
            if self.skill_book.check_button(mousepos,i):
                _,_,_, self.required_tiles = getattr(self.skill_book, self.char_skills[i] + '_get_requirement')(self)
                self.skill_book.show_requirement_mini_tiles(screen, self.requirement_location, self.char_skills[i],self.required_tiles)
                description = getattr(self.skill_book, "get_detail_%s"%self.char_skills[i])(self)
                write_text_description(screen, width // 2 + 30, text_description_level, description, 15)

    def draw_tiles(self,screen):

        for i in range(len(self.tile_img_locations)):
            tile_name = self.char_tiles_list[i]
            screen.blit(self.tile_image_dict[tile_name],
                        self.tile_image_dict[tile_name].get_rect(center=self.tile_img_locations[i]))
            write_text(screen, self.tile_img_locations[i][0], self.tile_img_locations[i][1] + 40,
                       tile_name, 15)
            # fixed tile
            if self.char_name == 'Mirinae' and i==0:
                write_text(screen, self.tile_img_locations[i][0], self.tile_img_locations[i][1] + 60,
                           "%d + 1" % self.char_tiles[tile_name], 20)

            elif self.char_name == 'Baron' and i==2:
                write_text(screen, self.tile_img_locations[i][0], self.tile_img_locations[i][1] + 60,
                           "%d + 1" % self.char_tiles[tile_name], 20)
            elif self.char_name == 'Riri' and i==1:
                write_text(screen, self.tile_img_locations[i][0], self.tile_img_locations[i][1] + 60,
                           "%d + 1" % self.char_tiles[tile_name], 20)
            else:
                write_text(screen, self.tile_img_locations[i][0], self.tile_img_locations[i][1] + 60,
                           "%d"%self.char_tiles[tile_name], 20)

        #write_text(screen, self.tile_info_location[0], self.tile_info_location[1], "%s"%self.char_tiles, 15)

    def draw_character_description(self,screen):
        write_text(screen, self.character_info_location[0], self.character_info_location[1], self.char_name, 25)
        screen.blit(self.heart,
                    self.heart.get_rect(center=(self.character_info_location[0] + 90, self.character_info_location[1]) ))

        write_text(screen, self.character_info_location[0] + 125, self.character_info_location[1], "%d"%self.hpmax_for_drawing, 20, 'red')










# other variables
learnable_skill_price_dict ={'holy_barrier':20, 'no_op':5,'poison_dart':10,'metastasis':10, 'vaccine':10,'chronic':20 ,'acute':20 ,'gas':20 }



class Skill_Book():
    def __init__(self, book_name, character_skills):
        global learnable_skill_price_dict, mini_tile_icons
        self.my_name = book_name

        self.skill_images = dict()
        # learnable skill names here (only used inside this class)
        self.learnable_skill_list = list(learnable_skill_price_dict.keys())
        for skill_name in self.learnable_skill_list:
            self.skill_images[skill_name] = load_image("skills/learnable_skills/%s" % (skill_name))
        self.character_skills = character_skills
        for skill_name in self.character_skills:
            self.skill_images[skill_name] = load_image("skills/%s/%s" % (self.my_name,skill_name))


        self.image_button_tolerance = 25
        self.button_spacing = 10
        self.button_x = 50
        self.button_y = 560
        self.button_locations = [(self.button_x, self.button_y + (2 * self.image_button_tolerance + self.button_spacing)* i) for i in range(len(self.character_skills))]


        self.mini_tiles = list(tile_names)
        self.mini_tile_icons = mini_tile_icons
        self.minitile_x = width//2
        self.minitile_y = height-40
        self.minitile_spacing = 50
        self.minitile_not_shown = ['Used', 'Empty','Unusable'] # should not show these tiles

    def init_each_fight(self):
        pass

    def draw_skill_on_custom_location(self,screen, skill_name, skill_location):
        screen.blit(self.skill_images[skill_name], self.skill_images[skill_name].get_rect(center=skill_location))

    def draw_skill(self,screen, skill_name, skill_location_index):
        screen.blit(self.skill_images[skill_name], self.skill_images[skill_name].get_rect(center=self.button_locations[skill_location_index]))


    def check_button(self,mousepos,skill_location_index):
        if check_inside_button(mousepos, self.button_locations[skill_location_index], self.image_button_tolerance):
            # print(self.character_skills[i]+" selected")
            return True
        return False

    def show_requirement_mini_tiles(self,screen, location, skill_name, requirement_dict_given = None):
        if not requirement_dict_given:
            return

        required_tile_x, required_tile_y = location
        requirement_spacing = 25

        requirement_dict = requirement_dict_given
        if requirement_dict_given=="create": # create one
            _, _, _,requirement_dict = getattr(self,skill_name +'_get_requirement')(global_dummy_player)

        cnt = 0
        for req_tile_name, req_range in requirement_dict.items():
            content = " %d ~ %d " % req_range

            if not req_range[0]:
                content = "   ~ %d " % req_range[1]
            elif not req_range[1]:
                content = " %d ~   " % req_range[0]

            screen.blit(self.mini_tile_icons[req_tile_name], self.mini_tile_icons[req_tile_name].get_rect(
                center=(required_tile_x , required_tile_y + cnt * requirement_spacing)))
            write_text(screen, required_tile_x + 40, required_tile_y + cnt * requirement_spacing,
                       content, 20)

            cnt += 1

    ''' 
    All the skills that the player can learn goes here
    poison etc.
    
    '''


    def holy_barrier_get_requirement(self,player):
        S = player.count_tile('Skill')
        D = player.count_tile('Defence')
        if (S<3 or D<1):
            return False, 0, False, {'Skill':(3,0),'Defence':(1,0)} # skill_valid, target_nums, is_attack
        return True, 0, False, {'Skill':(3,0),'Defence':(1,0)} # skill_valid, target_nums,is_attack

    def holy_barrier(self,player, target_list):
        sound_effects['playerdeath'].play()
        D = player.count_tile('Defence')
        player.buffs['attack immunity'] += D
    def get_detail_holy_barrier(self,player):
        D = player.count_tile('Defence')
        return "Holy barrier|Summon a shield that blocks any attack  for D = %d times"%D



    def no_op_get_requirement(self,player):
        return True, 0, False, {} # skill_valid, target_nums,is_attack
    def no_op(self,player, target_list):
        sound_effects['hard_hit'].play()
    def get_detail_no_op(self,player):
        return "no op|Just deletes current tiles"


    '''
    poison spells (poison dart relic will increase its power)
    attacks one target
    inflict 
    '''
    def poison_dart_get_requirement(self,player):
        S = player.count_tile('Skill')
        A = player.count_tile('Attack')
        R = player.count_tile('Regen')
        if (S<1 or A>3 or R<1):
            return False, 1, True, {'Skill':(1,0),'Regen':(1,0),'Attack':(0,3)} # skill_valid, target_nums, is_attack
        return True, 1, True, {'Skill':(1,0),'Regen':(1,0),'Attack':(0,3)} # skill_valid, target_nums,is_attack

    def poison_dart(self,player, target_list):
        ### relic effect ###
        duration = 3
        damage_multiplier = 3
        for relic in player.relics:
            if relic.name=="poison bottle": # exists!
                duration = 6
                damage_multiplier = 6

        sound_effects['hit'].play()
        A = player.count_tile('Attack')
        damage = (damage_multiplier*A) * player.get_attack_multiplier()
        for enemy in target_list:
            enemy.buffs['poison'] += duration
            enemy.take_damage(player,damage)

    def get_detail_poison_dart(self,player):
        duration = 3
        damage_multiplier = 3
        for relic in player.relics:
            if relic.name=="poison bottle": # exists!
                duration = 6
                damage_multiplier = 6

        A = player.count_tile('Attack')
        damage = (damage_multiplier*A) * player.get_attack_multiplier()
        return "Poison dart|Attack one target with %d*A = %d damage   and inflict poison for %s turns"%(damage_multiplier,damage, duration)

        #'metastasis': 10, 'vaccine': 10, 'chronic': 20, 'acute': 10, 'gas': 10

    ###########################################################################################################################
    def metastasis_get_requirement(self,player):
        S = player.count_tile('Skill')
        R = player.count_tile('Regen')
        if (S<1 or R<2):
            return False, 3, False, {'Skill':(1,0),'Regen':(2,0)} # skill_valid, target_nums, is_attack
        return True, 3, False, {'Skill':(1,0),'Regen':(2,0)} # skill_valid, target_nums,is_attack

    def metastasis(self,player, target_list):
        sound_effects['water'].play()
        time.sleep(0.1)

        for enemy in target_list:
            remaining_duration = enemy.buffs['poison']
            enemy.buffs['vulnerability'] += remaining_duration
            enemy.buffs['weakness'] += remaining_duration
            enemy.buffs['toxin'] += remaining_duration

    def get_detail_metastasis(self,player):
        return "Metastasis|Apply vulnerability, weakness, toxin to all enemies for the remaining duration  of their poison"
    ###########################################################################################################################


    ###########################################################################################################################
    def vaccine_get_requirement(self, player):
        S = player.count_tile('Skill')
        D = player.count_tile('Defence')
        R = player.count_tile('Regen')
        if (S < 2 or D < 1 or R < 1):
            return False, 0, False, {'Skill': (2, 0), 'Regen': (1, 0),'Defence': (1, 0)}  # skill_valid, target_nums, is_attack
        return True, 0, False, {'Skill': (2, 0), 'Regen': (1, 0),'Defence': (1, 0)}  # skill_valid, target_nums,is_attack

    def vaccine(self, player, target_list):
        sound_effects['bandage'].play()
        time.sleep(0.1)

        duration = player.buffs['poison']
        healamt = max(0 , duration*10)
        player.enforced_regen(healamt)
        player.buffs['poison'] = 0
        player.buffs['toxin'] = 0
        player.buffs['weakness'] = 0
        player.buffs['vulnerability'] = 0
        player.get_buff_effect()

    def get_detail_vaccine(self, player):
        duration = player.buffs['poison']
        return "Vaccine|Instantly recovers (duration of poison) * 10 = %d health and removes poison,     toxin, weakness, vulnerability" % (duration*10)
    ###########################################################################################################################


    ###########################################################################################################################
    def chronic_get_requirement(self, player):
        S = player.count_tile('Skill')
        R = player.count_tile('Regen')
        if (S < 2 or R < 2):
            return False, 1, False, {'Skill': (2, 0), 'Regen': (2, 0)}  # skill_valid, target_nums, is_attack
        return True, 1, False, {'Skill': (2, 0), 'Regen': (2, 0)}  # skill_valid, target_nums,is_attack

    def chronic(self, player, target_list):
        sound_effects['water'].play()
        time.sleep(0.1)
        for enemy in target_list:
            duration = enemy.buffs['poison']
            enemy.buffs['poison'] = 2*(duration) # +1

    def get_detail_chronic(self, player):
        return "Chronic|Doubles the duration of poison applied  to one enemy"
    ###########################################################################################################################


    ###########################################################################################################################
    def acute_get_requirement(self, player):
        '''
        weakness is also applied in damaging, so it is OP skill
        :param player:
        :return:
        '''
        S = player.count_tile('Skill')
        R = player.count_tile('Regen')
        if (S < 3 or R < 1):
            return False, 1, False, {'Skill': (3, 0), 'Regen': (1, 0)}  # skill_valid, target_nums, is_attack
        return True, 1, False, {'Skill': (3, 0), 'Regen': (1, 0)}  # skill_valid, target_nums,is_attack

    def acute(self, player, target_list):
        sound_effects['bell'].play()
        time.sleep(0.1)

        for enemy in target_list:
            duration = enemy.buffs['poison']
            damage = duration * 5
            enemy.take_damage(player, damage, True) # no fight back - this is not considered a normal attack
            enemy.buffs['poison'] = 0 # remove the poison

    def get_detail_acute(self, player):
        return "Acute|Instantly deal poison damage equal to   the remaining duration of the poison    applied to one enemy and removes the    poison"
    ###########################################################################################################################


    ###########################################################################################################################
    def gas_get_requirement(self, player):
        S = player.count_tile('Skill')
        A = player.count_tile('Attack')
        R = player.count_tile('Regen')
        if (S < 1 or A < 1 or R < 1):
            return False, 3, False, {'Skill': (3, 0), 'Regen': (1, 0),'Attack': (1, 0)}  # skill_valid, target_nums, is_attack
        return True, 3, False, {'Skill': (3, 0), 'Regen': (1, 0),'Attack': (1, 0)}  # skill_valid, target_nums,is_attack

    def gas(self, player, target_list):
        ### relic effect ###
        duration = 5
        for relic in player.relics:
            if relic.name=="poison mask": # exists!
                duration *= 2

        sound_effects['shruff'].play()
        time.sleep(0.1)

        for enemy in target_list:
            enemy.buffs['poison'] = duration

            current_pattern = enemy.get_next_move_on_player_turn()
            if current_pattern == 'attack':
                enemy.buffs['broken will'] += 1
            elif current_pattern == 'shield':
                enemy.buffs['toxin'] += 1


    def get_detail_gas(self, player):
        duration = 5
        for relic in player.relics:
            if relic.name=="poison mask": # exists!
                duration *= 2
        return "Gas|Apply poison on all enemies for %d turns, broken will on enemies trying to       attack, and toxin on enemies trying to       defend"%duration
    ###########################################################################################################################




################################# skill book
class Mirinae_skills(Skill_Book):

    def __init__(self):
        super().__init__('Mirinae_skills',['martial_art','head_start','sword_storm','self_defence','Antifragile','Excaliber']) # 'guard_attack'
        # A = player.count_tile('Attack')
        # S = player.count_tile('Skill')
        # D = player.count_tile('Defence')
        # R = player.count_tile('Regen')
        self.antifragile_multiplier = 4

    def init_each_fight(self):# initialize skill book parameters
        self.antifragile_multiplier = 4


    def martial_art_get_requirement(self,player):
        ''' 1
        condition:
        when attack tile < 4

        attack one enemy with damage A * 5
        '''

        S = player.count_tile('Skill')
        A = player.count_tile('Attack')
        if (S<1 or A>3 or A<1):
            return False, 1, True, {'Skill':(1,0),'Attack':(1,3)} # skill_valid, target_nums, is_attack
        return True, 1, True, {'Skill':(1,0),'Attack':(1,3)} # skill_valid, target_nums,is_attack


    def martial_art(self,player, target_list):
        sound_effects['hit'].play()
        A = player.count_tile('Attack')
        damage = (5*A) * player.get_attack_multiplier()
        for enemy in target_list:
            enemy.take_damage(player,damage)

    def get_detail_martial_art(self,player):
        A = player.count_tile('Attack')
        damage = (5*A) * player.get_attack_multiplier()
        return "Martial art|Attack one target with 5*A = %d damage"%damage


    def head_start_get_requirement(self,player):
        ''' 2
        '''
        S = player.count_tile('Skill')
        if (S<1):
            return False, S+1, True, {'Skill':(1,0),}
        return True, S+1, True, {'Skill':(1,0),}

    def head_start(self,player, target_list):
        sound_effects['hit'].play()
        D = player.count_tile('Defence')
        for enemy in target_list:
            enemy.buffs['vulnerability'] += 3
            enemy.total_defence -= 5*D

    def get_detail_head_start(self,player):
        S = player.count_tile('Skill')
        D = player.count_tile('Defence')
        return "Head start|Apply vulnerability to S+1 = %d targets  (3 turns) and removes 5*D = %d defence"%(S+1,D*5)

    def sword_storm_get_requirement(self,player):
        ''' 3

        '''
        S = player.count_tile('Skill')
        if (S<2):
            return False, 3, True, {'Skill':(2,0),}
        return True, 3, True, {'Skill':(2,0),}  # skill_valid, target_nums,is_attack
    def sword_storm(self,player, target_list):
        sound_effects['sword'].play()
        A = player.count_tile('Attack')
        damage = (A*5)  * player.get_attack_multiplier()
        for enemy in target_list:
            enemy.take_damage(player,damage)
    def get_detail_sword_storm(self,player):
        A = player.count_tile('Attack')
        damage = (A*5) * player.get_attack_multiplier()
        return "Sword storm|Attack all targets with A*5 = %d damage"%(damage)


    def self_defence_get_requirement(self,player):
        ''' 4
        다음 턴에 받는 (데미지 - S* 5*(R+D)) 만큼만 받고 그대로 돌려준다. 공격을 안당하면 무효 (R+D=0이면 모든 데미지를 받게됨)
        데미지를 반사 데미지로써 저장해두면 됨. 공격받을때 일부를 반사함 
        absorbtion이라는 파라미터에 임시로 데미지 흡수 함
        #회복 및 방어가 공격으로 전환된다: S*P(R+D)만큼 피해를 준다
        '''
        S = player.count_tile('Skill')
        if (S<2):
            return False, 0, True, {'Skill':(2,0),}
        return True, 0, True, {'Skill':(2,0),}
    def self_defence(self,player, target_list):
        sound_effects['get'].play()
        S = player.count_tile('Skill')
        D = player.count_tile('Defence')
        R = player.count_tile('Regen')
        player.absorption = 5 * S * (R+D)
        player.counter_attack = True

    def get_detail_self_defence(self,player):
        S = player.count_tile('Skill')
        D = player.count_tile('Defence')
        R = player.count_tile('Regen')
        absorption_amt = 5 * S * (R+D)
        return "Self defence|For all the incoming attacks next turn, absorb 5*S*(R+D) = %d damage and reflect each damage back"%(absorption_amt)

    # def guard_attack_get_requirement(self,player):
    #     ''' 5
    #
    #     '''
    #     S = player.count_tile('Skill')
    #     if (S<3):
    #         return False, 0, True, {'Skill':(3,0),'Defence':(1,0)}
    #     return True, 0, True, {'Skill':(3,0),'Defence':(1,0)}
    #
    # def guard_attack(self,player, target_list):
    #     sound_effects['get'].play()
    #     player.board.convert_all_tiles_on_board('Defence', 'Attack')
    #
    # def get_detail_guard_attack(self, player):
    #     return "Guard attack|All defence tiles become attack tiles on current board"

    def Antifragile_get_requirement(self,player):
        ''' 5

        '''
        A = player.count_tile('Attack')
        S = player.count_tile('Skill')
        if (S<3 or A<1):
            return False, 1, True, {'Skill':(3,0),'Attack':(1,0)}
        return True, 1, True, {'Skill':(3,0),'Attack':(1,0)} # skill_valid, target_nums,is_attack

    def Antifragile(self,player, target_list):
        for i in range(4):
            sound_effects['sword'].play()
            time.sleep(0.11)

        A = player.count_tile('Attack')
        damage = player.P(A)  * player.get_attack_multiplier() * self.antifragile_multiplier
        for enemy in target_list:
            enemy.take_damage(player,damage)

        self.antifragile_multiplier *= 2

    def get_detail_Antifragile(self, player):
        A = player.count_tile('Attack')
        damage = player.P(A) * player.get_attack_multiplier() * self.antifragile_multiplier
        return "Antifragile|Damage is doubled with each attack in   game. Current damage: P(A)x%d = %d "%( self.antifragile_multiplier, damage)


    def Excaliber_get_requirement(self,player):
        ''' 6

        '''
        S = player.count_tile('Skill')
        if (S<3):
            return False, 1, True, {'Skill':(3,0)}
        return True, 1, True, {'Skill':(3,0)} # skill_valid, target_nums,is_attack

    def Excaliber(self,player, target_list):
        sound_effects['playerdeath'].play()
        time.sleep(0.1)

        total_A = player.board.consume_all_tiles_on_board('Attack')
        damage = ( 5 * total_A ) * player.get_attack_multiplier()
        for enemy in target_list:
            enemy.take_damage(player,damage)
            enemy.buffs['broken will'] += 1

    def get_detail_Excaliber(self, player):
        total_A = player.board.count_all_tiles_on_board('Attack')
        damage = ( 5 * total_A ) * player.get_attack_multiplier()
        return "Excaliber|Use up all attack tiles in the board and give 5 times the amount of damage =   %d to one enemy and apply 'broken will' for 1 turn"%damage


class Cinavro_skills(Skill_Book):
    def __init__(self):
        super().__init__('Cinavro_skills',['abuse','gacha','flat_betting','bluff','Jackpot','All_in'])
        # A = player.count_tile('Attack')
        # S = player.count_tile('Skill')
        # D = player.count_tile('Defence')
        # R = player.count_tile('Regen')

    def init_each_fight(self):# initialize skill book parameters
        pass

    ###################################### 1 ########################################
    def abuse_get_requirement(self,player):
        S = player.count_tile('Skill')
        if (S<1):
            return False, 0, False, {'Skill':(1,0)}
        return True, 0, False, {'Skill':(1,0)} # skill_valid, target_nums,is_attack
    def abuse(self,player, target_list):
        sound_effects['register'].play()
        time.sleep(0.1)

        player.board.temporarily_replace_a_blank_tile_to("Joker")

    def get_detail_abuse(self, player):
        return "Abuse|Add one Joker tile to the board during  this battle"
    ###############################################################################

    ##################################### 2 #########################################
    def gacha_get_requirement(self,player):
        S = player.count_tile('Skill')
        if (S<1):
            return False, 0, False, {'Skill':(1,0)}
        return True, 0, False, {'Skill':(1,0)} # skill_valid, target_nums,is_attack
    def gacha(self,player, target_list):
        sound_effects['jackpot'].play()
        time.sleep(0.1)

        S = player.count_tile('Skill')
        for i in range(S+2):
            player.board.insert_a_tile_on_board("Joker")

    def get_detail_gacha(self, player):
        S = player.count_tile('Skill')
        return "Gacha|Random S+2 = %d blank tiles on the       current board are converted into Jokers"%S
    ###############################################################################

    ##################################### 3 #########################################
    def flat_betting_get_requirement(self,player):
        S = player.count_tile('Skill')
        if (S<2):
            return False, 0, False, {'Skill':(2,0)}
        return True, 0, False, {'Skill':(2,0)} # skill_valid, target_nums,is_attack
    def flat_betting(self,player, target_list):
        sound_effects['coin_drop'].play()
        time.sleep(0.1)

        player.board.convert_all_tiles_on_board('Used', 'Joker')

    def get_detail_flat_betting(self, player):
        return "Flat betting|Convert all used tiles into Joker tiles"
    ###############################################################################

    #################################### 4 #########################################
    def bluff_get_requirement(self,player):
        S = player.count_tile('Skill')
        if (S<2):
            return False, 1, False, {'Skill':(2,0)}
        return True, 1, False, {'Skill':(2,0)} # skill_valid, target_nums,is_attack
    def bluff(self,player, target_list):
        sound_effects['dash'].play()
        time.sleep(0.1)

        for enemy in target_list:
            enemy.buffs['weakness'] += 1
            enemy.buffs['decay'] += 1
            enemy.buffs['vulnerability'] += 1
    def get_detail_bluff(self, player):
        return "Bluff|Inflict weakness, vulnerability, and    decay on one enemy"
    ###############################################################################

    #################################### 5 #########################################
    def Jackpot_get_requirement(self,player):
        S = player.count_tile('Skill')
        if (S<3):
            return False, 0, False, {'Skill':(3,0)}
        return True, 0, False, {'Skill':(3,0)} # skill_valid, target_nums,is_attack
    def Jackpot(self,player, target_list):
        sound_effects['jackpot'].play()
        time.sleep(0.1)
        player.board.force_reset_next_turn()

    def get_detail_Jackpot(self, player):
        return "Jackpot|Force the board to reset on the next    turn"
    ###############################################################################

    ##################################### 6 #########################################
    def All_in_get_requirement(self,player):
        S = player.count_tile('Skill')
        if (S<3):
            return False, 0, False, {'Skill':(3,0)}
        return True, 0, False, {'Skill':(3,0)} # skill_valid, target_nums,is_attack
    def All_in(self,player, target_list):
        sound_effects['bell'].play()
        time.sleep(0.1)

        all_tile_names = list(tile_name_description_dic.keys())
        for tile_name in all_tile_names:
            if tile_name == 'Unusable':
                continue
            elif tile_name == 'Empty':
                player.board.convert_all_tiles_on_board('Empty', 'Unusable')
            else:
                player.board.convert_all_tiles_on_board(tile_name, 'Joker')

    def get_detail_All_in(self, player):
        return "All in|Convert all tiles into jokers, except   all empty/unusable tiles on the board   become unusable"
    ###############################################################################




class Baron_skills(Skill_Book):
    def __init__(self):
        super().__init__('Baron_skills',['guard','zone','smash','fissure','Mortal_strike','Build'])
        # A = player.count_tile('Attack')
        # S = player.count_tile('Skill')
        # D = player.count_tile('Defence')
        # R = player.count_tile('Regen')
    def init_each_fight(self):# initialize skill book parameters
        pass


    ##############################################################################
    def guard_get_requirement(self,player):
        S = player.count_tile('Skill')
        D = player.count_tile('Defence')
        if (S<1 or D<1):
            return False, 0, False, {'Skill':(1,0), 'Defence':(1,0)}
        return True, 0, False, {'Skill':(1,0), 'Defence':(1,0)} # skill_valid, target_nums,is_attack
    def guard(self,player, target_list):
        sound_effects['block'].play()
        time.sleep(0.1)
        D = player.count_tile('Defence')
        player.get_defence(5 * D)

    def get_detail_guard(self, player):
        D = player.count_tile('Defence')
        return "Guard|Gain defence 5*D = %d"%(D*5)
    ###############################################################################
    ##############################################################################
    def zone_get_requirement(self,player):
        S = player.count_tile('Skill')
        A = player.count_tile('Attack')
        if (S<1 or A<1):
            return False, 0, False, {'Skill':(1,0),'Attack':(1,0) }
        return True, 0, False, {'Skill':(1,0),'Attack':(1,0) } # skill_valid, target_nums,is_attack
    def zone(self,player, target_list):
        sound_effects['item_put_down'].play()
        time.sleep(0.1)
        player.board.convert_all_tiles_on_board('Attack', 'Defence')
        player.board.convert_all_tiles_on_board('Regen', 'Defence')

    def get_detail_zone(self, player):
        return "Zone|Convert all attack and regen tiles on   the board into defence tile"
    ###############################################################################
    ##############################################################################
    def smash_get_requirement(self,player):
        S = player.count_tile('Skill')
        A = player.count_tile('Attack')
        if (S < 2 or A < 1):
            return False, 1, False, {'Skill': (2, 0), 'Attack': (1, 0)}
        return True, 1, False, {'Skill': (2, 0), 'Attack': (1, 0)}  # skill_valid, target_nums,is_attack
    def smash(self,player, target_list):
        sound_effects['hard_hit'].play()
        time.sleep(0.2)
        sound_effects['block'].play()

        gain_shield = 0
        for enemy in target_list:
            gain_shield += enemy.total_defence
            enemy.set_zero_defence()

        player.get_defence(gain_shield)

    def get_detail_smash(self, player):
        return "Smash|Absorb and remove all defense from one  enemy"
    ###############################################################################
    ##############################################################################
    def fissure_get_requirement(self,player): # this is an attack!
        S = player.count_tile('Skill')
        D = player.count_tile('Defence')
        if (S<2 or D<1):
            return False, 0, True, {'Skill':(2,0), 'Defence':(1,0)}
        return True, 0, True, {'Skill':(2,0), 'Defence':(1,0)} # skill_valid, target_nums,is_attack
    def fissure(self,player, target_list):
        for i in range(2):
            sound_effects['block'].play()
            time.sleep(0.15)

        D = player.count_tile('Defence')
        player.get_defence(5 * D)
        player.fissure_flag = True

    def get_detail_fissure(self, player):
        D = player.count_tile('Defence')
        return "Fissure|          Gain defence 5*D = %d          At turn end, if enemies fail to remove  all my defence, the remaining defense is distributed as attack to all enemies   and exhaust all defence"%(D*5)
    ###############################################################################
    ##############################################################################
    def Mortal_strike_get_requirement(self,player):
        S = player.count_tile('Skill')
        if (S<3):
            return False, 0, False, {'Skill':(3,0)}
        return True, 0, False, {'Skill':(3,0)} # skill_valid, target_nums,is_attack
    def Mortal_strike(self,player, target_list):
        sound_effects['shruff'].play()
        time.sleep(0.1)

        player.counter_attack = True

        total_D = player.board.consume_all_tiles_on_board('Defence')
        player.get_defence(total_D * 5)

    def get_detail_Mortal_strike(self, player):
        total_D = player.board.count_all_tiles_on_board('Defence')
        return "Mortal strike|Use up all defence tiles in the board   and gain 5 times the amount of defence =  %d and counterattack all enemy attacks"%(total_D*5)
    ###############################################################################
    ##############################################################################
    def Build_get_requirement(self,player):
        S = player.count_tile('Skill')
        D = player.count_tile('Defence')
        if (S<3 or D<1):
            return False, 0, False, {'Skill':(3,0), 'Defence':(1,0)}
        return True, 0, False, {'Skill':(3,0), 'Defence':(1,0)} # skill_valid, target_nums,is_attack
    def Build(self,player, target_list):
        for i in range(3):
            sound_effects['block'].play()
            time.sleep(0.12)

        D = player.count_tile('Defence')
        player.get_defence(10*D)
        
        # 현재까지 가지고 있는 기본 방어력을 모두 temporal defence로 옮긴다  (기본방어는 0로 만든다)
        volatile_defence = player.defence
        player.temporal_defence += volatile_defence # 이미 가지고 있을수도 있으니
        player.defence = 0

        # 지금부터 얻는 디펜스는 전부 템포랄 디펜스로 전환하도록 해야함 (보드 리셋시 다시 초기화되는 플래그)
        player.all_def_to_temporal_def = True
        # 보드가 리셋될때 템포랄 디펜스도 리셋되고 저 플래그도 리셋됨

    def get_detail_Build(self, player):
        D = player.count_tile('Defence')
        return "Build|Defence stacks until the board reset    Also gain 10*D = %d defence"%(D*10)
    ###############################################################################





class Narin_skills(Skill_Book):
    def __init__(self):
        super().__init__('Narin_skills',[])
        # A = player.count_tile('Attack')
        # S = player.count_tile('Skill')
        # D = player.count_tile('Defence')
        # R = player.count_tile('Regen')
    def init_each_fight(self):# initialize skill book parameters
        pass

class Riri_skills(Skill_Book):
    def __init__(self):
        super().__init__('Riri_skills',[])
        # A = player.count_tile('Attack')
        # S = player.count_tile('Skill')
        # D = player.count_tile('Defence')
        # R = player.count_tile('Regen')
    def init_each_fight(self):# initialize skill book parameters
        pass
class Arisu_skills(Skill_Book):
    def __init__(self):
        super().__init__('Arisu_skills',[])
        # A = player.count_tile('Attack')
        # S = player.count_tile('Skill')
        # D = player.count_tile('Defence')
        # R = player.count_tile('Regen')
    def init_each_fight(self):# initialize skill book parameters
        pass

class Ato_skills(Skill_Book):
    def __init__(self):
        super().__init__('Ato_skills',[]) # ['poison_dart','metastasis' , 'vaccine','chronic' ,'acute' ,'gas' ]
        # A = player.count_tile('Attack')
        # S = player.count_tile('Skill')
        # D = player.count_tile('Defence')
        # R = player.count_tile('Regen')
    def init_each_fight(self):# initialize skill book parameters
        pass
######################### BUILD SKILL BOOK ##########################




character_skill_dictionary = {'Mirinae':Mirinae_skills(),'Cinavro':Cinavro_skills(), 'Narin': Narin_skills(), 'Baron': Baron_skills(), 'Riri': Riri_skills(), 'Arisu': Arisu_skills(), 'Ato': Ato_skills()}
character_tile_dictionary = {'Mirinae':{'Attack':8, 'Regen':0, 'Defence':4, 'Skill':4, 'Joker':0, 'Karma':0},
                             'Cinavro':{'Attack':4, 'Regen':0, 'Defence':4,  'Skill':8, 'Joker':1,'Karma':0},
                             'Baron':{'Attack':2, 'Regen':0, 'Defence':8,  'Skill':6, 'Joker':0,'Karma':0},
                             'Narin':  {'Attack':3, 'Regen':0, 'Defence':3,  'Skill':10, 'Joker':0,'Karma':1},
                             'Riri': {'Attack': 2, 'Regen': 6, 'Defence': 2, 'Skill': 6, 'Joker': 0, 'Karma': 0},
                             'Arisu': {'Attack': 3, 'Regen': 1, 'Defence': 5, 'Skill': 7, 'Joker': 0, 'Karma': 0}, # 타일 수 하나 적은 대신 유물 가지고 시작
                             'Ato': {'Attack': 5, 'Regen': 2, 'Defence': 5, 'Skill': 4, 'Joker': 0, 'Karma': 0}, # 타일 수 하나 적은 대신 돈 많이 가지고 시작 (50원)
                             }
character_max_hp = {'Mirinae':100,'Cinavro':80, 'Narin': 100,'Baron':150, 'Riri':60, 'Arisu':100, 'Ato':100}

learnable_skills = Mirinae_skills() # dummy...


global_dummy_player = DummyPlayer()
