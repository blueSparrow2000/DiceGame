'''
How to add relics

1. Make a class
2. Add the class name to relic_class_names

'''

from util import *

relic_rarity_color = {'common':'silver', 'rare':(150, 200, 240), 'epic':'yellowgreen', 'special':'violet', 'legendary':'gold', 'myth':'crimson'}


class Relic():
    def __init__(self, class_name="Relic", name="Relic", type = 'regular', rarity = 'myth'):
        global relic_rarity_color
        self.class_name = class_name
        self.name = name
        self.image = load_image("relics/%s"%name)
        self.type = type
        self.rarity = rarity
        self.color = relic_rarity_color[self.rarity]
        self.delete = False

        self.debug = False
        self.scaled_image = pygame.transform.scale(self.image, (50, 50))

    def penetrate_armor(self, damage):
        return False

    def get_discount_factor(self):
        return 1

    def count_relic_with_same_name(self,player, my_name):
        num_of_relics = 0
        for relic in player.relics:
            if relic.name == my_name:
                num_of_relics+= 1
        return num_of_relics

    def fight_every_turn_beginning_effect(self, player):
        if self.debug:
            print("my turn started!")
        pass

    def fight_every_turn_end_effect(self, player, enemies):
        if self.debug:
            print("my turn ended!")
        pass

    def fight_start_effect(self, player, enemies):
        if self.debug:
            print("Fight has started!")
        pass

    def effect_when_first_obtained(self, player, side_effect_off = False):
        if self.debug:
            print("Relic first obtained!",end='')
            if side_effect_off:
                print(": Effect off is turned on!")
            else:
                print()
        pass

    def effect_when_discard(self, player):
        if self.debug:
            print("Relic discarded!")
        pass

    def activate_on_death(self, enemy):
        pass


    def activate_on_kill(self, player, enemy):
        if self.debug:
            print("Detected a kill!")
        pass

    def activate_on_board_reset(self, player, enemy):
        if self.debug:
            print("Board reset!")
        pass

    def activate_on_taking_damage(self, player, enemy, attack_damage):
        if self.debug:
            print("Player got hit by %s with %s damage!" % (enemy.my_name, attack_damage))
        pass

    def activate_when_getting_reward_gold(self, amount):
        if self.debug:
            print("Got reward!")
        return amount

    def ruin_chance_increaser(self):
        if self.debug:
            print("Ruin chance stays the same!")
        return 0

    def relic_spawn_chance_increaser(self):
        if self.debug:
            print("Relic chance stays the same!")
        return 0

    def fix_artifact_number(self):
        return 0

    def curse_chance_decreaser(self):
        return 0

    def skill_requiring_3_skill_tile_reduce_one(self):
        if self.debug:
            print("Relic trying to reduce skill requiring 3 skill tile reduce one")
        return False

    ####################################### In progress feature ... ##############################################

    ##############################################################################################################

    def description(self):
        return "A relic for debugging"

    def draw(self, screen, location, scaled = False):
        if scaled:
            screen.blit(self.scaled_image,
                        self.scaled_image.get_rect(center=location))
        else:
            screen.blit(self.image,
                        self.image.get_rect(center=location))


    def show_ruin_description(self, screen, relic_location, discription_location ,mousepos): #  width // 2, relic_Y_level + 150 # width // 2, relic_Y_level + 177
        if check_inside_button(mousepos, relic_location, button_side_len_half):
            write_text(screen, discription_location[0], discription_location[1], self.name, 20, self.color)
            write_text(screen, discription_location[0], discription_location[1] + 27, self.description(), 16,
                       self.color)



class PoisonBottle(Relic):
    '''
    For poison dart skill
    Increase damage multiplier 3 -> 6
    duration 3 -> 6
    '''
    def __init__(self):
        super().__init__(class_name="PoisonBottle", name="poison bottle",rarity = 'epic')

    def description(self):
        return "Poison dart: damage multiplier 3 -> 6 / duration 3 -> 6"

class PoisonMask(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="PoisonMask", name="poison mask",rarity = 'epic')

    def description(self):
        return "Gas: Double the poison duration"



class SerpentHeart(Relic):
    '''
    Increase max hp by 50
    '''
    def __init__(self):
        super().__init__(class_name="SerpentHeart", name="serpent heart",rarity = 'special')

    def description(self):
        return "Increase max hp by 50"

    def effect_when_first_obtained(self, player, side_effect_off = False):
        if side_effect_off:
            return
        player.max_health += 50
        player.enforced_regen(50)
    def effect_when_discard(self, player):
        player.set_max_health(player.max_health - 50)

class FearCell(Relic):
    '''
    Recovers 4 hp at the start of each fight
    '''
    def __init__(self):
        super().__init__(class_name="FearCell", name="fear cell",rarity = 'common')
        self.recover_amount = 4

    def description(self):
        return "Recovers %d hp at the start of each fight"%self.recover_amount

    def fight_start_effect(self, player, enemies):
        player.enforced_regen(self.recover_amount)

class StemCell(Relic):
    '''
    Recovers 2 hp at the beginning of each turn in a battle
    '''
    def __init__(self):
        super().__init__(class_name="StemCell", name="stem cell",rarity = 'epic')
        self.recover_amount = 2

    def description(self):
        return "Recovers %d hp at the start of each turn in a battle"%self.recover_amount

    def fight_every_turn_beginning_effect(self, player):
        player.enforced_regen(self.recover_amount)

class Ration(Relic):
    '''
    Recovers 1 hp at the end of each turn in a battle
    '''
    def __init__(self):
        super().__init__(class_name="Ration", name="ancient ration",rarity = 'rare')
        self.recover_amount = 1

    def description(self):
        return "Recovers %d hp at the end of each turn in a battle"%self.recover_amount

    def fight_every_turn_end_effect(self, player,enemies):
        player.enforced_regen(self.recover_amount)


class WhiteCube(Relic):
    '''
    [Exhaust] Can revive once
    '''
    def __init__(self):
        super().__init__(class_name="WhiteCube", name="white cube", type = 'exhaust',rarity = 'myth')

    def description(self):
        return "[Exhaust] Can revive once"

    def activate_on_death(self, player):
        if player.health <= 0: # activate only when health is below
            sound_effects['playerdeath'].play()
            # player.enforced_regen(player.max_health)
            player.set_health(player.max_health)
            self.delete = True

class BlackCube(Relic):
    '''
    '''
    def __init__(self):
        super().__init__(class_name="BlackCube", name="black cube", rarity = 'myth')

    def description(self):
        return "You can place planar figure on top of used tiles"

    def effect_when_first_obtained(self, player, side_effect_off = False):
        player.board.used_tile_as_empty_tile = True

    def effect_when_discard(self, player): # 이런식의 toggle effect같은 경우, 같은 이름의 유물이 더이상 존재하지 않을떄 토글을 꺼줘야 한다
        relic_num = self.count_relic_with_same_name(player, self.name)
        if relic_num == 1: # 1일때는 나밖에 없을떄
            player.board.used_tile_as_empty_tile = False
        elif relic_num == 0:
            print("ERROR! I exist but not counted")
        else:
            pass

class FrenzySkull(Relic):
    '''
    heal by the amount overkilled # 즉 적의 피가 -대로 깎였을때, 그만큼 내가 회복한다는것 (적의 피가 -10이 되고 죽었으면 내가 10을 회복함 etc.)
    should be called whenever enemy is getting deleted
    '''
    def __init__(self):
        super().__init__(class_name="FrenzySkull", name="frenzy skull", rarity = 'legendary')

    def description(self):
        return "heal by the amount overkilled"

    def activate_on_kill(self, player, enemy):
        # print(enemy.health)
        reverse_heal_amt = abs(enemy.health)
        player.enforced_regen(reverse_heal_amt)


class LargeThorn(Relic):
    '''
    Deals half of the damage received
    '''
    def __init__(self):
        super().__init__(class_name="LargeThorn", name="large thorn", rarity = 'legendary')

    def description(self):
        return "Deals half of the damage received"

    def activate_on_taking_damage(self, player, enemy, attack_damage): # called when player got attacked by enemy
        if enemy is not None:
            enemy.health -= attack_damage//2


class Thorn(Relic):
    '''
    Deals 5 damage when attacked
    '''
    def __init__(self):
        super().__init__(class_name="Thorn", name="thorn", rarity = 'special')
        self.thorn_damage = 5

    def description(self):
        return "Deals %s damage when attacked"%self.thorn_damage

    def activate_on_taking_damage(self, player, enemy, attack_damage): # called when player got attacked by enemy
        if enemy is not None:
            enemy.health -= self.thorn_damage


class Moss(Relic):
    '''
    Better next time!
    '''
    def __init__(self):
        super().__init__(class_name="Moss", name="moss", rarity = 'common')

    def description(self):
        return "Better luck next time!"

    def relic_spawn_chance_increaser(self):
        return 1 # one percent increase

class GoldenTalisman(Relic):
    '''
    Each has 20% chance of doubling earned gold
    '''
    def __init__(self):
        super().__init__(class_name="GoldenTalisman", name="golden talisman", rarity = 'common')
        self.chance = 20

    def description(self):
        return "Each has %d%% chance of doubling earned gold"%self.chance

    def activate_when_getting_reward_gold(self, amount):
        final_amount = amount
        number = random.randint(1,100)
        if number <= self.chance:
            final_amount = amount*2
        return final_amount

class RuinCompass(Relic):
    '''
    Increase chance of finding a relic in ruins (about 1%)
    Forward compatibility of the moss
    '''
    def __init__(self):
        super().__init__(class_name="RuinCompass", name="ruin compass", rarity = 'rare')

    def description(self):
        return "Increase the chance of finding a relic in ruins"

    def ruin_chance_increaser(self):  # ruin spawns more often
        return 5

    def relic_spawn_chance_increaser(self):
        return 2



'''
Relics of Mirinae
'''

class Dagger(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="Dagger", name="dagger",rarity = 'special')
        self.damage_per_dagger = 3

    def description(self):
        return "Deals %d damage to closest enemy for each attack tile drawn"%self.damage_per_dagger

    def fight_every_turn_end_effect(self, player,enemies):
        A = player.count_tile('Attack')
        dagger_damage = self.damage_per_dagger * A
        enemies[0].take_damage(player, dagger_damage)

        # for entity in enemies:
        #     entity.take_damage(player, dagger_damage)


class BagOfDagger(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="BagOfDagger", name="bag of dagger",rarity = 'legendary')
        self.damage_per_dagger = 2

    def description(self):
        return "Deals %d damage to all enemies for each attack tile drawn"%self.damage_per_dagger

    def fight_every_turn_end_effect(self, player,enemies):
        A = player.count_tile('Attack')
        dagger_damage = self.damage_per_dagger * A

        for entity in enemies:
            entity.take_damage(player, dagger_damage)



class TiltedScale(Relic):
    '''
    NOTE: You cannot get frenzy skull effect or enemy's thorny effect due to this relic
    '''
    def __init__(self):
        super().__init__(class_name="TiltedScale", name="tilted scale",rarity = 'epic')
        self.tilt_amount = 2

    def description(self):
        return "At the start of battle, all enemies take %d damage"%self.tilt_amount

    def fight_start_effect(self, player,enemies):
        for entity in enemies:
            # entity.take_damage(player, self.tilt_amount, no_fightback=True)
            entity.take_damage(None, self.tilt_amount, no_fightback=True)



class ArcaneBook(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="ArcaneBook", name="arcane book",rarity = 'epic')

    def description(self):
        return "Gain strength on the first turn of each battle"

    def fight_start_effect(self, player, enemies):
        player.buffs['strength'] = 1


class Tombstone(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="Tombstone", name="tombstone",rarity = 'rare')

    def description(self):
        return "On board reset, one empty tile is converted into an attack tile"

    def activate_on_board_reset(self, player, enemy):
        player.board.insert_a_tile_on_board("Attack")

class RecycledSword(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="RecycledSword", name="recycled sword",rarity = 'common')

    def description(self):
        return "Each turn, one used tile is converted into an attack tile"

    def fight_every_turn_end_effect(self, player,enemies):
        player.board.replace_a_tile_on_board("Used", "Attack")

class SwordCatalyst(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="SwordCatalyst", name="sword catalyst",rarity = 'common')

    def description(self):
        return "For each enemy killed, get temporal attack tile"

    def activate_on_kill(self, player, enemy):
        player.board.insert_a_tile_on_board("Attack")


class WarHorn(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="WarHorn", name="war horn",rarity = 'epic')

    def description(self):
        return "If no attack tiles on the board, all empty tiles become attack"

    def fight_every_turn_beginning_effect(self, player):
        A_board = player.board.count_all_tiles_on_board("Attack")
        if A_board<=0:
            sound_effects['horn_high'].play()
            player.board.convert_all_tiles_on_board_immediately("Empty", "Attack")



'''
Relics of Baron
'''

class StrawMat(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="StrawMat", name="straw mat",rarity = 'epic')
        self.shield_per_straw = 4

    def description(self):
        return "Gains %d shield for each defence tile drawn"%self.shield_per_straw

    def fight_every_turn_end_effect(self, player,enemies):
        D = player.count_tile('Defence')
        defence_gain = self.shield_per_straw * D

        player.get_defence(defence_gain)

class Obsidian(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="Obsidian", name="obsidian",rarity = 'rare')

    def description(self):
        return "On board reset, one empty tile is converted into a defence tile"

    def activate_on_board_reset(self, player, enemy):
        player.board.insert_a_tile_on_board("Defence")

class RecycledShield(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="RecycledShield", name="recycled shield",rarity = 'common')

    def description(self):
        return "Each turn, one used tile is converted into a defence tile"

    def fight_every_turn_end_effect(self, player,enemies):
        player.board.replace_a_tile_on_board("Used", "Defence")

class ShieldCatalyst(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="ShieldCatalyst", name="shield catalyst",rarity = 'common')

    def description(self):
        return "For each enemy killed, get temporal defence tile"

    def activate_on_kill(self, player, enemy):
        player.board.insert_a_tile_on_board("Defence")

class BattleShield(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="BattleShield", name="battle shield",rarity = 'rare')
        self.shield_gain = 10

    def description(self):
        return "For each enemy killed, get %d temporal defence"%self.shield_gain

    def activate_on_kill(self, player, enemy):
        player.get_defence(self.shield_gain)



class Paranoia(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="Paranoia", name="paranoia",rarity = 'epic')
        self.shield_gain = 2

    def description(self):
        return "If defense is 0 at turn end, gain %d defense"%self.shield_gain

    def fight_every_turn_end_effect(self, player,enemies):
        if player.defence == 0: # one paranoia will take care of all other paranoias
            for relic in player.relics:
                if relic.name == 'paranoia':
                    player.get_defence(self.shield_gain)

            player.update_defence()

        # if player.defence==0:
        #     player.defence += self.shield_gain
        #     player.update_defence()

class IronPlate(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="IronPlate", name="iron plate",rarity = 'legendary')
        self.base_defence_gain = 4
    def description(self):
        return "Gain %d permanent defence"%self.base_defence_gain

    def effect_when_first_obtained(self, player, side_effect_off = False):
        player.base_defence += self.base_defence_gain
        player.update_defence()
    def effect_when_discard(self, player):
        player.base_defence -= self.base_defence_gain


class Armadillo(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="Armadillo", name="armadillo",rarity = 'rare')
        self.defence_multiplier = 10

    def description(self):
        return "Gain %d*(# of enemies) defence on the first turn"%self.defence_multiplier

    def fight_start_effect(self, player, enemies):
        num_of_enemies = len(enemies)
        player.get_defence(num_of_enemies*self.defence_multiplier)


class Antidote(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="Antidote", name="antidote",rarity = 'legendary')

    def description(self):
        return "Become immune to poison and toxin"

    def effect_when_first_obtained(self, player, side_effect_off = False):
        player.immune_to_toxin = True
        player.immune_to_poison = True
    def effect_when_discard(self, player):
        relic_num = self.count_relic_with_same_name(player, self.name)
        if relic_num == 1: # 1일때는 나밖에 없을떄
            player.immune_to_toxin = False
            player.immune_to_poison = False
        elif relic_num == 0:
            print("ERROR! I exist but not counted")
        else:
            pass


class Oil(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="Oil", name="oil",rarity = 'special')

    def description(self):
        return "Become immune to weakness"

    def effect_when_first_obtained(self, player, side_effect_off = False):
        player.immune_to_weakness = True
    def effect_when_discard(self, player):
        relic_num = self.count_relic_with_same_name(player, self.name)
        if relic_num == 1: # 1일때는 나밖에 없을떄
            player.immune_to_weakness = False
        elif relic_num == 0:
            print("ERROR! I exist but not counted")
        else:
            pass



class Encyclopedia(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="Encyclopedia", name="encyclopedia",rarity = 'legendary')
        self.decrease_rate = 5

    def description(self):
        return "Reduces the maximum health of all enemies by %d%%"%self.decrease_rate

    def fight_start_effect(self, player, enemies):
        for entity in enemies:
            entity.set_max_health(round(entity.max_health*(1 - self.decrease_rate/100)))

class Candle(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="Candle", name="candle",rarity = 'special')
        self.percent_point = 40

    def description(self):
        return "decrease chance of getting cursed on the altar by %d%%p"%self.percent_point

    def curse_chance_decreaser(self):
        return 50

class Equipment(Relic):
    '''

    '''

    def __init__(self):
        super().__init__(class_name="Equipment", name="equipment", rarity='legendary')

    def description(self):
        return "There are always 3 artifact options in the ruins"

    def fix_artifact_number(self):
        return 3

class GoldenClover(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(class_name="GoldenClover", name="golden clover",rarity = 'legendary')

    def description(self):
        return "Each turn, one used tile is converted into a joker tile"

    def fight_every_turn_end_effect(self, player,enemies):
        player.board.replace_a_tile_on_board("Used", "Joker")

class YellowCube(Relic):
    '''

    '''

    def __init__(self):
        super().__init__(class_name="YellowCube", name="yellow cube", rarity='myth')

    def description(self):
        return "All prices in the shop are half off per yellow cube"


    def get_discount_factor(self):
        return 2

class BlueCube(Relic):
    '''

    '''

    def __init__(self):
        super().__init__(class_name="BlueCube", name="blue cube", rarity='myth')
        self.damage_threshold = 100
    def description(self):
        return "Do not take damage more than %d per hit"%self.damage_threshold

    def effect_when_first_obtained(self, player, side_effect_off = False):
        player.taking_damage_threshold = self.damage_threshold

    def effect_when_discard(self, player): # 이런식의 toggle effect같은 경우, 같은 이름의 유물이 더이상 존재하지 않을떄 토글을 꺼줘야 한다
        relic_num = self.count_relic_with_same_name(player, self.name)
        if relic_num == 1: # 1일때는 나밖에 없을떄
            player.taking_damage_threshold = -1
        elif relic_num == 0:
            print("ERROR! I exist but not counted")
        else:
            pass

class RedCube(Relic):
    '''

    '''

    def __init__(self):
        super().__init__(class_name="RedCube", name="red cube", rarity='myth')

    def description(self):
        return "Reduce the cost of skills with 3 required skill tiles by 1"

    def skill_requiring_3_skill_tile_reduce_one(self):
        return True



####################################### In progress... ##############################################



class Rapier(Relic):
    '''

    '''

    def __init__(self):
        super().__init__(class_name="Rapier", name="rapier", rarity='rare')
        self.damage_threshold = 10

    def description(self):
        return "Penetrates enemy's armor if damage is less than %d"%self.damage_threshold

    def penetrate_armor(self, damage):
        if damage < self.damage_threshold:
            return True
        return False


relic_class_names = ['BlueCube','RedCube','YellowCube','BlackCube','GoldenClover','PoisonMask','Equipment','Candle', 'Encyclopedia', 'Antidote', 'Oil','StrawMat','Obsidian','RecycledShield','ShieldCatalyst','BattleShield','Paranoia','IronPlate','Armadillo','WarHorn','SwordCatalyst','RecycledSword','Tombstone','ArcaneBook','TiltedScale','BagOfDagger', 'Dagger', 'PoisonBottle','Thorn' , 'LargeThorn', 'FrenzySkull', 'WhiteCube', 'Ration' , 'StemCell','FearCell' ,'SerpentHeart' , 'Moss', 'GoldenTalisman']










