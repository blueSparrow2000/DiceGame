'''
GLOBAL REQUIREMENT FOR SKILL
Note that one needs at least one skill tile to use skill > Checked inside player's 'skill ready'

N 명의 적에게 적용되는 공격은 이미 target_list에 적용이 된 상태다. 스킬을 쓸땐 고려하지 않아도 된다. 리스트 순회만 하면 끝

'''



from music import *


################################# skill book
class Mirinae_skills():
    def __init__(self):
        self.skills = ['martial_art','sword_storm','head_start','self_defence','guard_attack','Excaliber']
        # A = player.count_tile('Attack')
        # S = player.count_tile('Skill')
        # D = player.count_tile('Defence')
        # R = player.count_tile('Regen')

    def martial_art_get_requirement(self,player):
        ''' 1
        condition:
        when attack tile <= 3

        attack one enemy with damage S * (A) * 5
        '''
        A = player.count_tile('Attack')
        if (A>3):
            return False, 1, True  # skill_valid, target_nums, is_attack
        return True, 1, True # skill_valid, target_nums,is_attack
    def martial_art(self,player, target_list):
        sound_effects['hit'].play()
        A = player.count_tile('Attack')
        S = player.count_tile('Skill')
        damage = (5* S * player.P(A)) * player.get_attack_multiplier()
        for enemy in target_list:
            counter_attack_damage = enemy.take_damage(damage)
            player.health -= counter_attack_damage

    def sword_storm_get_requirement(self,player):
        ''' 2
        attacks S+1 enemies with P(A)
        '''

        S = player.count_tile('Skill')
        return True, S+1, True  # skill_valid, target_nums,is_attack
    def sword_storm(self,player, target_list):
        sound_effects['sword'].play()
        A = player.count_tile('Attack')
        damage = player.P(A) * player.get_attack_multiplier()
        for enemy in target_list:
            counter_attack_damage = enemy.take_damage(damage)
            player.health -= counter_attack_damage
    def head_start_get_requirement(self,player):
        ''' 3
        S명의 적에게 취약을 부여하고 D*5만큼 상대의 방어도를 제거한다

        '''
        S = player.count_tile('Skill')
        return True, S, True

    def head_start(self,player, target_list):
        sound_effects['hit'].play()
        D = player.count_tile('Defence')
        for enemy in target_list:
            enemy.buffs['vulnerability'] = 3
            enemy.total_defence -= 5*D

    def self_defence_get_requirement(self,player):
        ''' 4
        다음 턴에 받는 (데미지 - S* 5*(R+D)) 만큼만 받고 그대로 돌려준다. 공격을 안당하면 무효 (R+D=0이면 모든 데미지를 받게됨)
        데미지를 반사 데미지로써 저장해두면 됨. 공격받을때 일부를 반사함 
        absorbtion이라는 파라미터에 임시로 데미지 흡수 함

        #회복 및 방어가 공격으로 전환된다: S*P(R+D)만큼 피해를 준다
        '''
        return True, 1, True
    def self_defence(self,player, target_list):
        S = player.count_tile('Skill')
        D = player.count_tile('Defence')
        R = player.count_tile('Regen')
        player.absorption = 5 * S * (R+D)
        player.counter_attack = True

    def guard_attack_get_requirement(self,player):
        ''' 5
        한 적에게 P(A)*S + P(D) 만큼 데이지를 준다
        '''
        return True, 1, True

    def guard_attack(self,player, target_list):
        sound_effects['sword'].play()
        A = player.count_tile('Attack')
        S = player.count_tile('Skill')
        D = player.count_tile('Defence')

        damage = ( S * player.P(A) + player.P(D) ) * player.get_attack_multiplier()
        for enemy in target_list:
            counter_attack_damage = enemy.take_damage(damage)
            player.health -= counter_attack_damage

    def Excaliber_get_requirement(self,player):
        ''' 6
        condition:
        when attack tile >= 4

        Gives P(A)*5 damage to an enemy
        Gives debuff: broken will for three turns
        '''
        A = player.count_tile('Attack')
        if (A<4):
            return False, 1, True  # skill_valid, target_nums, is_attack
        return True, 1, True # skill_valid, target_nums,is_attack

    def Excaliber(self,player, target_list):
        sound_effects['playerdeath'].play()
        A = player.count_tile('Attack')
        damage = ( 5 * player.P(A) )* player.get_attack_multiplier()
        for enemy in target_list:
            counter_attack_damage = enemy.take_damage(damage)
            player.health -= counter_attack_damage
            enemy.buffs['broken will'] = 3


class Gambler_skills():
    def __init__(self):
        self.skills = []


######################### BUILD SKILL BOOK ##########################
mirinae_skill_book = Mirinae_skills()
gambler_skill_book = Gambler_skills()

character_skill_dictionary = {'Mirinae':mirinae_skill_book,'Gambler':gambler_skill_book}