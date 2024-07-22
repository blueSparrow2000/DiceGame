'''
Collection of functions which draws stuff on screen

'''

import pygame
import os, sys

'''
When player clickes appropriate keys, 
computer highlights pressed 'line'
'''

IMAGE_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))+"/images/"

def center_image(image):
    one_side = image.get_height()
    rect = image.get_rect()
    rect = rect.move((one_side//2, one_side//2))
def move_image(img,coord):
    rect = img.get_rect()
    rect = rect.move(coord)
    return rect

def resize_image(img,size):
    return pygame.transform.scale(img, size)

def load_image(filename):
    # print(filename)
    try:
        APP_FOLDER = IMAGE_FOLDER
        full_path = os.path.join(APP_FOLDER, '%s.png'%filename)
        #print(full_path)
        return pygame.image.load(full_path)
    except:
        print(filename)
        return None

### icons / buff icons
icons = ['no op','shield','sword','buff','unkown']
buff_name_description_dic = {
'decay':"defence is halved every turn",
'strength':"deals double damage",
'weakness':"deals half damage",
'broken will':"cannot attack",
'confusion':"(player): cannot use secondary planar figure\n(enemies): misses an attack",
'heal ban':"cannot heal",
'poison':"takes 5 damage at the start of every turn",
'toxin':"incoming attacks penetrates defence",
}
# buff_names = ['decay', 'strength', 'weakness','broken will','confusion','heal ban','poison','toxin']
buff_names = list(buff_name_description_dic.keys())
# icon generator
icon_container = dict()
buff_icon_container = dict()

for ic in icons:
    icon_container[ic] = load_image("icons/%s"%ic)

for ic in buff_names:
    buff_icon_container[ic] = load_image("icons/buffs/%s"%ic)


### load enemy images
mob_img = load_image("mob")
