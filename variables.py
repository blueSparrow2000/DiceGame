# system variables
game_fps = 30 #60
width,height = 480, 960#480, 960
mousepos = (0,0)

# game variables
board_Y_level = 480
map_Y_level = 480
mob_Y_level = 280
MAX_DEPTH = -100

mob_side_len = 64
mob_gap = 28

# text levels
text_description_level = 640
requirement_level = 760
turn_text_level = 160
area_name_Y_level = 160

# TILES INIT - need to add new type if nessesary
tile_names =['Attack', 'Defence', 'Regen', 'Skill', 'Used', 'Empty','Unusable', 'Joker', 'Karma']
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
terracotta = (120, 110, 100)

### basic buttons
bottom_left_button = (40, height - 40)
bottom_right_button = (width - 40, height - 40)
bottom_center_button = (width//2,height-40)


button_side_len_half = 25