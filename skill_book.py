'''
GLOBAL REQUIREMENT FOR SKILL
Note that one needs at least one skill tile to use skill > Checked inside player's 'skill ready'

N 명의 적에게 적용되는 공격은 이미 target_list에 적용이 된 상태다. 스킬을 쓸땐 고려하지 않아도 된다. 리스트 순회만 하면 끝

'''

from util import *


class Skill_Book():
    def __init__(self, book_name, character_skills):
        self.my_name = book_name

        self.skill_images = dict()
        # learnable skill names here (only used inside this class)
        self.learnable_skill_list = ['poison_dart', 'holy_barrier']
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


    def draw_skill_on_custom_location(self,screen, skill_name, skill_location):
        screen.blit(self.skill_images[skill_name], self.skill_images[skill_name].get_rect(center=skill_location))

    def draw_skill(self,screen, skill_name, skill_location_index):
        screen.blit(self.skill_images[skill_name], self.skill_images[skill_name].get_rect(center=self.button_locations[skill_location_index]))


    def check_button(self,mousepos,skill_location_index):
        if check_inside_button(mousepos, self.button_locations[skill_location_index], self.image_button_tolerance):
            # print(self.character_skills[i]+" selected")
            return True
        return False

    ''' 
    All the skills that the player can learn goes here
    poison etc.
    
    '''

    '''
    poison spell (poison dart relic will increase its power)
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
        sound_effects['hit'].play()
        A = player.count_tile('Attack')
        damage = (3*A) * player.get_attack_multiplier()
        for enemy in target_list:
            enemy.buffs['poison'] = 3
            counter_attack_damage = enemy.take_damage(damage)
            player.health -= counter_attack_damage

    def get_detail_poison_dart(self,player):
        A = player.count_tile('Attack')
        damage = (3*A) * player.get_attack_multiplier()
        return "Poison dart|Attack one target with 3*A = %d damage   and inflict poison for 3 turns"%damage



    def holy_barrier_get_requirement(self,player):
        S = player.count_tile('Skill')
        A = player.count_tile('Attack')
        R = player.count_tile('Regen')
        if (S<3 or A>1 or R<1):
            return False, 0, True, {'Skill':(3,0),'Regen':(1,0),'Attack':(0,1)} # skill_valid, target_nums, is_attack
        return True, 0, True, {'Skill':(3,0),'Regen':(1,0),'Attack':(0,1)} # skill_valid, target_nums,is_attack

    def holy_barrier(self,player, target_list):
        sound_effects['playerdeath'].play()
        player.buffs['attack immunity'] = 2
    def get_detail_holy_barrier(self,player):
        return "Holy barrier|Summon a shield that blocks all attacks once"


################################# skill book
class Mirinae_skills(Skill_Book):

    def __init__(self):
        super().__init__('Mirinae_skills',['martial_art','head_start','sword_storm','self_defence','guard_attack','Excaliber'])
        # A = player.count_tile('Attack')
        # S = player.count_tile('Skill')
        # D = player.count_tile('Defence')
        # R = player.count_tile('Regen')

    def martial_art_get_requirement(self,player):
        ''' 1
        condition:
        when attack tile < 4

        attack one enemy with damage A * 5
        '''

        S = player.count_tile('Skill')
        A = player.count_tile('Attack')
        if (S<1 or A>3):
            return False, 1, True, {'Skill':(1,0),'Attack':(0,3)} # skill_valid, target_nums, is_attack
        return True, 1, True, {'Skill':(1,0),'Attack':(0,3)} # skill_valid, target_nums,is_attack


    def martial_art(self,player, target_list):
        sound_effects['hit'].play()
        A = player.count_tile('Attack')
        damage = (5*A) * player.get_attack_multiplier()
        for enemy in target_list:
            counter_attack_damage = enemy.take_damage(damage)
            player.health -= counter_attack_damage

    def get_detail_martial_art(self,player):
        A = player.count_tile('Attack')
        damage = (5*A) * player.get_attack_multiplier()
        return "Martial art|Attack one target with 5*A = %d damage"%damage


    def head_start_get_requirement(self,player):
        ''' 3


        '''
        S = player.count_tile('Skill')
        if (S<1):
            return False, S+1, True, {'Skill':(1,0),}
        return True, S+1, True, {'Skill':(1,0),}

    def head_start(self,player, target_list):
        sound_effects['hit'].play()
        D = player.count_tile('Defence')
        for enemy in target_list:
            enemy.buffs['vulnerability'] = 3
            enemy.total_defence -= 5*D

    def get_detail_head_start(self,player):
        S = player.count_tile('Skill')
        D = player.count_tile('Defence')
        return "Head start|Apply vulnerability to S+1 = %d targets  (3 turns) and removes 5*D = %d defence"%(S+1,D*5)

    def sword_storm_get_requirement(self,player):
        ''' 2


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
            counter_attack_damage = enemy.take_damage(damage)
            player.health -= counter_attack_damage
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

    def guard_attack_get_requirement(self,player):
        ''' 5

        '''
        S = player.count_tile('Skill')
        if (S<3):
            return False, 0, True, {'Skill':(3,0),'Defence':(1,0)}
        return True, 0, True, {'Skill':(3,0),'Defence':(1,0)}

    def guard_attack(self,player, target_list):
        sound_effects['get'].play()
        player.board.convert_all_tiles_on_board('Defence', 'Attack')

    def get_detail_guard_attack(self, player):
        return "Guard attack|All defence tiles become attack tiles on current board"

    def Excaliber_get_requirement(self,player):
        ''' 6

        '''
        S = player.count_tile('Skill')
        if (S<3):
            return False, 1, True, {'Skill':(3,0)}
        return True, 1, True, {'Skill':(3,0)} # skill_valid, target_nums,is_attack

    def Excaliber(self,player, target_list):
        sound_effects['playerdeath'].play()

        total_A = player.board.consume_all_tiles_on_board('Attack')
        damage = ( 10 * total_A ) * player.get_attack_multiplier()
        for enemy in target_list:
            counter_attack_damage = enemy.take_damage(damage)
            player.health -= counter_attack_damage
            enemy.buffs['broken will'] = 1

    def get_detail_Excaliber(self, player):
        total_A = player.board.count_all_tiles_on_board('Attack')
        damage = ( 10 * total_A ) * player.get_attack_multiplier()
        return "Excaliber|Use up all attack tiles in the board and gives 10 times the amount of damage =  %d to one enemy and apply 'broken will' for 1 turn"%damage


class Cinavro_skills(Skill_Book):
    def __init__(self):
        super().__init__('Cinavro_skills',[])
        # A = player.count_tile('Attack')
        # S = player.count_tile('Skill')
        # D = player.count_tile('Defence')
        # R = player.count_tile('Regen')


class Narin_skills(Skill_Book):
    def __init__(self):
        super().__init__('Narin_skills',[])
        # A = player.count_tile('Attack')
        # S = player.count_tile('Skill')
        # D = player.count_tile('Defence')
        # R = player.count_tile('Regen')

######################### BUILD SKILL BOOK ##########################

character_skill_dictionary = {'Mirinae':Mirinae_skills(),'Cinavro':Cinavro_skills(), 'Narin': Narin_skills()}
character_tile_dictionary = {'Mirinae':{'Attack':8, 'Regen':0, 'Defence':4, 'Skill':4, 'Joker':0, 'Karma':0},
                             'Cinavro':{'Attack':4, 'Regen':0, 'Defence':6,  'Skill':6, 'Joker':1,'Karma':0},
                             'Narin':  {'Attack':4, 'Regen':0, 'Defence':4,  'Skill':8, 'Joker':0,'Karma':1} }

