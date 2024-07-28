import pygame
from image_processor import *
import time
from music import *
from variables import *
import math

TAB_img = load_image("icons/TAB") # size 50 pixel
rotate_img = load_image("icons/rotate")
back_img = load_image("icons/back")
skip_img = load_image("icons/skip")

TAB_img_white = load_image("icons/TAB_white") # size 50 pixel
rotate_img_white = load_image("icons/rotate_white")
back_img_white = load_image("icons/back_white")
skip_img_white = load_image("icons/skip_white")


button_side_len_half = 25



def calc_drop_radius(factor,start_radius,mouse=True):  # factor is given by float between 0 and 1 (factor changes from 0 to 1)
    if not mouse:
        width = int(math.pow(3*(1-factor),3)+3.5)
    else:
        width = int(math.pow(2.5*(1-factor),3)+1.7)
    r = max(width,int(start_radius*(1+4*math.pow(factor,1/5))))
    return r



def draw_bar(screen,x,y,bar_length,bar_height, current_percent, color): # x,y is a position of x,y axis of bar
    pygame.draw.rect(screen,color,[x-bar_length//2, y-bar_height//2,int(bar_length*(current_percent/100)),bar_height])

def write_text(surf, x, y, text, size,color='black',bg_color = None): #(50, 200, 50)
    font = pygame.font.Font('freesansbold.ttf', size)
    if bg_color is not None:
        text = font.render(text, True, color, bg_color)
    else:
        text = font.render(text, True, color)
    # text.set_alpha(127)
    textRect = text.get_rect()
    textRect.center = (x, y)
    surf.blit(text, textRect)

'''
알아서 길이별로 잘라서 잘 보여주는 함수
'''
def write_text_description(surf, x, y, text, size,color='black',bg_color = None):
    if not text:
        return
    text_list = text.split('|')
    title = ""
    content = text_list[0]
    if (len(text_list) > 1):
        title = "{ %s }"%text_list[0]
        content = text_list[1]
    center_x_level = x # fixed
    y_level = y

    total_length = len(content)
    content_blocks = []
    content_per_line = 40
    current_start = 0
    while current_start + content_per_line < total_length:
        content_blocks.append(content[current_start:current_start+content_per_line])
        current_start += content_per_line
    content_blocks.append(content[current_start:total_length])

    write_text(surf, center_x_level, y_level - size - 20, title, size+10, color, bg_color)
    for i in range(len(content_blocks)):
        write_text(surf, center_x_level, y_level+i*size, content_blocks[i], size, color, bg_color)

    write_text(surf, center_x_level, requirement_level, "~ Requirements ~", 20, color, bg_color)


def check_inside_button(mouse_pos,button_center, button_side_len_half):
    if abs(mouse_pos[0] - button_center[0])<button_side_len_half and abs(mouse_pos[1] - button_center[1])<button_side_len_half:
        return True
    else:
        return False


'''
safely add a tile in a dictionary
'''
def safe_tile_add_one(dictionary, target_tile):
    if target_tile in dictionary:
        dictionary[target_tile] += 1 # increase one
    else:
        dictionary[target_tile] = 1 # add new tile

def safe_delete_dict(dictionary, target_tile):
    if target_tile in dictionary: # only when exists
        if (dictionary[target_tile]<=0):
            print("WARNING: possible error in the code (not deleted properly somewhere)\nREASON: Delete entity with amount 0 or less than 0")
        dictionary[target_tile] -= 1
        if dictionary[target_tile] <= 0: # delete entry if no longer exist
            del dictionary[target_tile]


