from util import *

relic_rarity_color = {'common':'silver', 'rare':(150, 200, 240), 'epic':'yellowgreen', 'legendary':'gold', 'special':'violet', 'cursed':'crimson'}

class Relic():
    def __init__(self, name="Relic", type = 'regular', rarity = 'common'):
        global relic_rarity_color
        self.name = name
        self.image = load_image("relics/%s"%name)
        self.debug = False
        self.type = type
        self.rarity = rarity
        self.color = relic_rarity_color[self.rarity]
        self.delete = False

    def fight_every_turn_beginning_effect(self, player):
        if self.debug:
            print("my turn started!")
        pass

    def fight_every_turn_end_effect(self, player):
        if self.debug:
            print("my turn ended!")
        pass

    def fight_start_effect(self, player):
        if self.debug:
            print("Fight has started!")
        pass

    def effect_when_first_obtained(self, player):
        if self.debug:
            print("Relic first obtained!")
        pass

    ####################################### In progress... ##############################################
    def activate_on_death(self, player):
        pass

    #####################################################################################################
    def description(self):
        return "A relic for debugging"

    def draw(self, screen, location):
        screen.blit(self.image,
                    self.image.get_rect(center=location))

class PoisonBottle(Relic):
    '''
    For poison dart skill
    Increase damage multiplier 3 -> 5
    duration 3 -> 5
    '''
    def __init__(self):
        super().__init__(name="poison bottle",rarity = 'rare')

    def description(self):
        return "Poison dart: damage multiplier 3 -> 5 / duration 3 -> 5"

class SerpentHeart(Relic):
    '''
    Increase max hp by 50
    '''
    def __init__(self):
        super().__init__(name="serpent heart",rarity = 'epic')

    def description(self):
        return "Increase max hp by 50"

    def effect_when_first_obtained(self, player):
        player.max_health += 50
        player.enforeced_regen(50)


class FearCell(Relic):
    '''
    Recovers 5 hp at the start of each fight
    '''
    def __init__(self):
        super().__init__(name="fear cell",rarity = 'common')

    def description(self):
        return "Recovers 5 hp at the start of each fight"

    def fight_start_effect(self, player):
        player.enforeced_regen(5)

class StemCell(Relic):
    '''
    Recovers 2 hp at the beginning of each turn in a battle
    '''
    def __init__(self):
        super().__init__(name="stem cell",rarity = 'rare')

    def description(self):
        return "Recovers 2 hp at the start of each turn in a battle"

    def fight_every_turn_beginning_effect(self, player):
        player.enforeced_regen(2)

class Ration(Relic):
    '''
    Recovers 2 hp at the end of each turn in a battle
    '''
    def __init__(self):
        super().__init__(name="ancient ration",rarity = 'rare')

    def description(self):
        return "Recovers 2 hp at the end of each turn in a battle"

    def fight_every_turn_end_effect(self, player):
        player.enforeced_regen(2)


####################################### In progress... ##############################################
class WhiteCube(Relic):
    '''
    [Exhaust] Can revive once
    '''
    def __init__(self):
        super().__init__(name="white cube", type = 'exhaust',rarity = 'legendary')

    def description(self):
        return "[Exhaust] Can revive once"

    def activate_on_death(self, player):
        sound_effects['playerdeath'].play()
        player.enforeced_regen(player.max_health)
        self.delete = True



class FrenzySkull(Relic):
    '''
    heal by the amount an owner overkilled # 즉 적의 피가 -대로 깎였을때, 그만큼 내가 회복한다는것 (적의 피가 -10이 되고 죽었으면 내가 10을 회복함 etc.)
    should be called whenever enemy is getting deleted
    '''
    def __init__(self):
        super().__init__(name="frenzy skull", rarity = 'special')

    def description(self):
        return "heal by the amount an owner overkilled"






