# system variables
game_fps = 30 #60
width,height = 480, 960#480, 960
mousepos = (0,0)

# game variables
board_Y_level = 480
map_Y_level = 480
mob_Y_level = 280
MAX_DEPTH = - 300
PRIMARY_BOSS_DEPTH = -100
SECONDARY_BOSS_DEPTH = -200
WATCHER_DEPTH = -150

mob_side_len = 64
mob_gap = 28

# text levels
text_description_level = 640
requirement_level = 760
turn_text_level = 155
area_name_Y_level = 155

middle_button_Y_level = 380
upper_button_Y_level = 200
upper_side_Y_level = 225

# TILES INIT - need to add new type if nessesary
tile_name_description_dic = {
'Attack':"used for attack"
, 'Defence':"used for defence"
, 'Regen':"used for healing"
, 'Skill':"used for skills"
, 'Used':""
, 'Empty':""
,'Unusable':""
, 'Joker':"can turn into 4 basic tiles"
, 'Karma':"[replicate]"
, 'Proliferation':"[replicate] when board reset, take 5 damage"
, 'Slime':"when contained in net, halves attack damage"
, 'Spike':"when contained in net, take 5 damage"
}
tile_names = list(tile_name_description_dic.keys())# ['Attack', 'Defence', 'Regen', 'Skill', 'Used', 'Empty','Unusable', 'Joker', 'Karma', 'Proliferation', 'Chained', 'Spike']


joker_transformable_tiles = ['Attack', 'Defence', 'Regen', 'Skill',  'Karma']

# other variables
runnable_skill_price_dict ={'poison_dart':10, 'holy_barrier':30}



# move background
background_y = -470
background_layer_y = 100

# mouse
mouse_particle_list = []  # mouse click effects
water_draw_time = 0.8
water_draw_time_mouse = 0.6
particle_width = 6
particle_width_mouse = 3
mouse_particle_radius = 5
droplet_radius = 33
# mouse color
effect_color = 'darkgoldenrod'#(150, 200, 240)
adventure_effect_color = 'darkgoldenrod'
option_effect_color = 'gold'
altar_effect_color = 'black'
shop_effect_color = 'gold'

# screen colors
fight_bg_color = 'lightgray' #  'oldlace'
adventure_bg_color = (100,130,100)
terracotta = (150, 140, 120)
darker_gold = (133, 83, 0)

### basic buttons
button_side_len_half = 25 # buttons are all of side 50 pixels

bottom_left_button = (40, height - 40)
bottom_right_button = (width - 40, height - 40)
bottom_center_button = (width//2,height-40)

right_middle_button = (width - 40,middle_button_Y_level)
left_middle_button = (40,middle_button_Y_level)

right_upper_button = (width - 40,upper_button_Y_level)
left_upper_button = (40,upper_button_Y_level)

right_side_button = (width//2 + 75,upper_side_Y_level)
right_side_upper_button = (width//2 + 75,upper_side_Y_level - 75)