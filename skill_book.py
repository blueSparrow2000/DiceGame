'''
GLOBAL REQUIREMENT FOR SKILL
Note that one needs at least one skill tile to use skill > Checked inside player's 'skill ready'

N 명의 적에게 적용되는 공격은 이미 target_list에 적용이 된 상태다. 스킬을 쓸땐 고려하지 않아도 된다. 리스트 순회만 하면 끝

'''

from util import *

class Skill_Book():
    def __init__(self, book_name, skills):
        self.my_name = book_name
        self.skills = skills
        self.skill_images = []
        self.image_button_tolerance = 25
        self.button_spacing = 10
        self.button_x = 50
        self.button_y = 560
        self.button_locations = [(self.button_x, self.button_y + (2 * self.image_button_tolerance + self.button_spacing)* i) for i in range(len(self.skills))]
        for skill_name in self.skills:
            self.skill_images.append(load_image("character_skills/%s/%s" % (self.my_name,skill_name)))

    def draw(self,screen):
        for i in range(len(self.skill_images)):
            screen.blit(self.skill_images[i], self.skill_images[i].get_rect(center=self.button_locations[i]))


    def check_button(self,mousepos):
        for i in range(len(self.skill_images)):
            if check_inside_button(mousepos, self.button_locations[i], self.image_button_tolerance):
                # print(self.skills[i]+" selected")
                return i # return the index of the clicked skill to use

        # no skills selected
        return -1


################################# skill book
class Mirinae_skills(Skill_Book):

    def __init__(self):
        super().__init__('Mirinae_skills',['martial_art','sword_storm','head_start','self_defence','guard_attack','Excaliber'])
        # A = player.count_tile('Attack')
        # S = player.count_tile('Skill')
        # D = player.count_tile('Defence')
        # R = player.count_tile('Regen')

    def martial_art_get_requirement(self,player):
        ''' 1
        condition:
        when attack tile < 4

        attack one enemy with damage S * (A) * 5
        '''
        A = player.count_tile('Attack')
        if (A>3):
            return False, 1, True, {'Skill':(1,0),'Attack':(0,3)} # skill_valid, target_nums, is_attack
        return True, 1, True, {'Skill':(1,0),'Attack':(0,3)} # skill_valid, target_nums,is_attack


    def martial_art(self,player, target_list):
        sound_effects['hit'].play()
        A = player.count_tile('Attack')
        S = player.count_tile('Skill')
        damage = (5* S * player.P(A)) * player.get_attack_multiplier()
        for enemy in target_list:
            counter_attack_damage = enemy.take_damage(damage)
            player.health -= counter_attack_damage

    def get_detail_martial_art(self,player):
        A = player.count_tile('Attack')
        S = player.count_tile('Skill')
        damage = (5* S * player.P(A)) * player.get_attack_multiplier()
        return "Martial art|Attack one target with 5*A*S = %d damage"%damage

    def sword_storm_get_requirement(self,player):
        ''' 2
        attacks S+1 enemies with P(A)
        '''

        S = player.count_tile('Skill')
        return True, S+1, True, {'Skill':(1,0),}  # skill_valid, target_nums,is_attack
    def sword_storm(self,player, target_list):
        sound_effects['sword'].play()
        A = player.count_tile('Attack')
        damage = player.P(A) * player.get_attack_multiplier()
        for enemy in target_list:
            counter_attack_damage = enemy.take_damage(damage)
            player.health -= counter_attack_damage
    def get_detail_sword_storm(self,player):
        S = player.count_tile('Skill')
        A = player.count_tile('Attack')
        damage = player.P(A) * player.get_attack_multiplier()
        return "Sword storm|Attack S+1 = %d targets with P(A) = %d    damage"%(S+1,damage)

    def head_start_get_requirement(self,player):
        ''' 3
        S명의 적에게 취약을 부여하고 D*5만큼 상대의 방어도를 제거한다

        '''
        S = player.count_tile('Skill')
        return True, S, True, {'Skill':(2,0),}

    def head_start(self,player, target_list):
        sound_effects['hit'].play()
        D = player.count_tile('Defence')
        for enemy in target_list:
            enemy.buffs['vulnerability'] = 3
            enemy.total_defence -= 5*D

    def get_detail_head_start(self,player):
        S = player.count_tile('Skill')
        D = player.count_tile('Defence')
        return "Head start|Apply vulnerability to S+1 = %d targets  (3 turns) and remove 5*D = %d defence"%(S+1,D*5)

    def self_defence_get_requirement(self,player):
        ''' 4
        다음 턴에 받는 (데미지 - S* 5*(R+D)) 만큼만 받고 그대로 돌려준다. 공격을 안당하면 무효 (R+D=0이면 모든 데미지를 받게됨)
        데미지를 반사 데미지로써 저장해두면 됨. 공격받을때 일부를 반사함 
        absorbtion이라는 파라미터에 임시로 데미지 흡수 함

        #회복 및 방어가 공격으로 전환된다: S*P(R+D)만큼 피해를 준다
        '''
        return True, 1, True, {'Skill':(2,0),}
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
        한 적에게 P(A)*S + P(D) 만큼 데이지를 준다
        '''
        return True, 1, True, {'Skill':(3,0),}

    def guard_attack(self,player, target_list):
        sound_effects['sword'].play()
        A = player.count_tile('Attack')
        S = player.count_tile('Skill')
        D = player.count_tile('Defence')

        damage = ( S * player.P(A) + player.P(D) ) * player.get_attack_multiplier()
        for enemy in target_list:
            counter_attack_damage = enemy.take_damage(damage)
            player.health -= counter_attack_damage

    def get_detail_guard_attack(self, player):
        A = player.count_tile('Attack')
        S = player.count_tile('Skill')
        D = player.count_tile('Defence')

        damage = ( S * player.P(A) + player.P(D) ) * player.get_attack_multiplier()
        return "Guard attack|Attack one target with S*P(A)+P(D) = %d  damage"%damage

    def Excaliber_get_requirement(self,player):
        ''' 6
        condition:
        when attack tile >= 1

        Gives (A+S)*10 damage to an enemy
        Gives debuff: broken will for three turns
        '''
        A = player.count_tile('Attack')
        if (A<1):
            return False, 1, True, {'Skill':(3,0),'Attack':(1,0)} # skill_valid, target_nums, is_attack
        return True, 1, True, {'Skill':(3,0),'Attack':(1,0)} # skill_valid, target_nums,is_attack

    def Excaliber(self,player, target_list):
        sound_effects['playerdeath'].play()
        A = player.count_tile('Attack')
        S = player.count_tile('Skill')
        damage = ( 10 * (A+S) ) * player.get_attack_multiplier()
        for enemy in target_list:
            counter_attack_damage = enemy.take_damage(damage)
            player.health -= counter_attack_damage
            enemy.buffs['broken will'] = 1

    def get_detail_Excaliber(self, player):
        A = player.count_tile('Attack')
        S = player.count_tile('Skill')
        damage = ( 10 * (A+S) ) * player.get_attack_multiplier()
        return "Excaliber|Attack one target with 10*(A+S) = %d    damage and apply 'broken will' for 1    turns"%damage


class Gambler_skills(Skill_Book):
    def __init__(self):
        super().__init__('Gambler_skills',[])
        # A = player.count_tile('Attack')
        # S = player.count_tile('Skill')
        # D = player.count_tile('Defence')
        # R = player.count_tile('Regen')


class Ohm_skills(Skill_Book):
    def __init__(self):
        super().__init__('Gambler_skills',[])
        # A = player.count_tile('Attack')
        # S = player.count_tile('Skill')
        # D = player.count_tile('Defence')
        # R = player.count_tile('Regen')

######################### BUILD SKILL BOOK ##########################
mirinae_skill_book = Mirinae_skills()
gambler_skill_book = Gambler_skills()
ohm_skill_book = Ohm_skills()

character_skill_dictionary = {'Mirinae':mirinae_skill_book,'Gambler':gambler_skill_book, 'Ohm': ohm_skill_book}
character_tile_dictionary = {'Mirinae':{'Attack':6, 'Defence':6, 'Regen':6, 'Skill':6, 'Joker':0, 'Karma':0},'Gambler':{'Attack':4, 'Defence':6, 'Regen':4, 'Skill':10, 'Joker':1,'Karma':0},'Ohm':{'Attack':5, 'Defence':4, 'Regen':5, 'Skill':10, 'Joker':0,'Karma':1} }

