'''
How to add relics

1. Make a class
2. Add the class name to relic_class_names

'''

from util import *

relic_rarity_color = {'common':'silver', 'rare':(150, 200, 240), 'epic':'yellowgreen', 'special':'violet', 'legendary':'gold', 'myth':'crimson'}


class Relic():
    def __init__(self, name="Relic", type = 'regular', rarity = 'common'):
        global relic_rarity_color
        self.name = name
        self.image = load_image("relics/%s"%name)
        self.type = type
        self.rarity = rarity
        self.color = relic_rarity_color[self.rarity]
        self.delete = False

        self.debug = False
        self.scaled_image = pygame.transform.scale(self.image, (50, 50))


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

    def effect_when_first_obtained(self, player):
        if self.debug:
            print("Relic first obtained!")
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


    ####################################### In progress... ##############################################
    #####################################################################################################



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
        super().__init__(name="poison bottle",rarity = 'epic')

    def description(self):
        return "Poison dart: damage multiplier 3 -> 6 / duration 3 -> 6"

class SerpentHeart(Relic):
    '''
    Increase max hp by 50
    '''
    def __init__(self):
        super().__init__(name="serpent heart",rarity = 'special')

    def description(self):
        return "Increase max hp by 50"

    def effect_when_first_obtained(self, player):
        player.max_health += 50
        player.enforced_regen(50)


class FearCell(Relic):
    '''
    Recovers 4 hp at the start of each fight
    '''
    def __init__(self):
        super().__init__(name="fear cell",rarity = 'common')
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
        super().__init__(name="stem cell",rarity = 'epic')
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
        super().__init__(name="ancient ration",rarity = 'rare')
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
        super().__init__(name="white cube", type = 'exhaust',rarity = 'myth')

    def description(self):
        return "[Exhaust] Can revive once"

    def activate_on_death(self, player):
        sound_effects['playerdeath'].play()
        player.enforced_regen(player.max_health)
        self.delete = True


class FrenzySkull(Relic):
    '''
    heal by the amount overkilled # 즉 적의 피가 -대로 깎였을때, 그만큼 내가 회복한다는것 (적의 피가 -10이 되고 죽었으면 내가 10을 회복함 etc.)
    should be called whenever enemy is getting deleted
    '''
    def __init__(self):
        super().__init__(name="frenzy skull", rarity = 'legendary')

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
        super().__init__(name="large thorn", rarity = 'legendary')

    def description(self):
        return "Deals half of the damage received"

    def activate_on_taking_damage(self, player, enemy, attack_damage): # called when player got attacked by enemy
        enemy.health -= attack_damage//2


class Thorn(Relic):
    '''
    Deals 5 damage when attacked
    '''
    def __init__(self):
        super().__init__(name="thorn", rarity = 'special')
        self.thorn_damage = 5

    def description(self):
        return "Deals %s damage when attacked"%self.thorn_damage

    def activate_on_taking_damage(self, player, enemy, attack_damage): # called when player got attacked by enemy
        enemy.health -= self.thorn_damage


class Moss(Relic):
    '''
    Better next time!
    '''
    def __init__(self):
        super().__init__(name="moss", rarity = 'common')

    def description(self):
        return "Better luck next time!"

    def relic_spawn_chance_increaser(self):
        return 1 # one percent increase

class GoldenTalisman(Relic):
    '''
    Each has 20% chance of doubling earned gold
    '''
    def __init__(self):
        super().__init__(name="golden talisman", rarity = 'common')
        self.chance = 20

    def description(self):
        return "Each has %d%% chance of doubling earned gold"%self.chance

    def activate_when_getting_reward_gold(self, amount):
        final_amount = amount
        number = random.randrange(1,100)
        if number <= self.chance:
            final_amount = amount*2
        return final_amount

class RuinCompass(Relic):
    '''
    Increase chance of finding a relic in ruins (about 1%)
    Forward compatibility of the moss
    '''
    def __init__(self):
        super().__init__(name="ruin compass", rarity = 'rare')

    def description(self):
        return "Increase the chance of finding a relic in ruins"

    def ruin_chance_increaser(self):  # ruin spawns more often
        return 5

    def relic_spawn_chance_increaser(self):
        return 2


####################################### In progress... ##############################################

'''
Relics of Mirinae
'''

class Dagger(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(name="dagger",rarity = 'special')
        self.damage_per_dagger = 1

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
        super().__init__(name="bag of dagger",rarity = 'legendary')
        self.damage_per_dagger = 1

    def description(self):
        return "Deals %d damage to all enemies for each attack tile drawn"%self.damage_per_dagger

    def fight_every_turn_end_effect(self, player,enemies):
        A = player.count_tile('Attack')
        dagger_damage = self.damage_per_dagger * A

        for entity in enemies:
            entity.take_damage(player, dagger_damage)



class TiltedScale(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(name="tilted scale",rarity = 'epic')
        self.tilt_amount = 5

    def description(self):
        return "At the start of battle, all enemies take %d damage"%self.tilt_amount

    def fight_start_effect(self, player,enemies):
        for entity in enemies:
            entity.take_damage(player, self.tilt_amount)



class ArcaneBook(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(name="arcane book",rarity = 'rare')

    def description(self):
        return "Gain strength on the first turn of each battle"

    def fight_start_effect(self, player, enemies):
        player.buffs['strength'] = 1


class Tombstone(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(name="tombstone",rarity = 'common')

    def description(self):
        return "On board reset, one empty tile is converted into an attack tile"

    def activate_on_board_reset(self, player, enemy):
        player.board.insert_a_tile_on_board("Attack")

class RecycledSword(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(name="recycled sword",rarity = 'rare')

    def description(self):
        return ""

    def fight_every_turn_beginning_effect(self, player):
        player.enforced_regen(self.recover_amount)

    def fight_every_turn_end_effect(self, player,enemies):
        if self.debug:
            print("my turn ended!")
        pass

    def fight_start_effect(self, player, enemies):
        if self.debug:
            print("Fight has started!")
        pass

    def effect_when_first_obtained(self, player):
        if self.debug:
            print("Relic first obtained!")
        pass

    def activate_on_death(self, enemy):
        pass


    def activate_on_kill(self, player, enemy):
        if self.debug:
            print("Detected a kill!")
        pass


    def activate_on_taking_damage(self, player, enemy, attack_damage):
        if self.debug:
            print("Player got hit by %s with %s damage!" % (enemy.my_name, attack_damage))
        pass

    def activate_when_getting_reward_gold(self, amount):
        if self.debug:
            print("Got reward!")
        return amount

class SwordCatalyst(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(name="sword catalyst",rarity = 'common')

    def description(self):
        return ""

    def fight_every_turn_beginning_effect(self, player):
        player.enforced_regen(self.recover_amount)

    def fight_every_turn_end_effect(self, player,enemies):
        if self.debug:
            print("my turn ended!")
        pass

    def fight_start_effect(self, player, enemies):
        if self.debug:
            print("Fight has started!")
        pass

    def effect_when_first_obtained(self, player):
        if self.debug:
            print("Relic first obtained!")
        pass

    def activate_on_death(self, enemy):
        pass


    def activate_on_kill(self, player, enemy):
        if self.debug:
            print("Detected a kill!")
        pass


    def activate_on_taking_damage(self, player, enemy, attack_damage):
        if self.debug:
            print("Player got hit by %s with %s damage!" % (enemy.my_name, attack_damage))
        pass

    def activate_when_getting_reward_gold(self, amount):
        if self.debug:
            print("Got reward!")
        return amount

class WarHorn(Relic):
    '''

    '''
    def __init__(self):
        super().__init__(name="war horn",rarity = 'legendary')

    def description(self):
        return ""

    def fight_every_turn_beginning_effect(self, player):
        player.enforced_regen(self.recover_amount)

    def fight_every_turn_end_effect(self, player,enemies):
        if self.debug:
            print("my turn ended!")
        pass

    def fight_start_effect(self, player, enemies):
        if self.debug:
            print("Fight has started!")
        pass

    def effect_when_first_obtained(self, player):
        if self.debug:
            print("Relic first obtained!")
        pass

    def activate_on_death(self, enemy):
        pass


    def activate_on_kill(self, player, enemy):
        if self.debug:
            print("Detected a kill!")
        pass


    def activate_on_taking_damage(self, player, enemy, attack_damage):
        if self.debug:
            print("Player got hit by %s with %s damage!" % (enemy.my_name, attack_damage))
        pass

    def activate_when_getting_reward_gold(self, amount):
        if self.debug:
            print("Got reward!")
        return amount


relic_class_names = ['Tombstone','ArcaneBook','TiltedScale','BagOfDagger', 'Dagger', 'PoisonBottle','Thorn' , 'LargeThorn', 'FrenzySkull', 'WhiteCube', 'Ration' , 'StemCell','FearCell' ,'SerpentHeart' , 'Moss', 'GoldenTalisman']










