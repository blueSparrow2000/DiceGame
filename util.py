import pygame
from image_processor import *
import time
from music import *
from variables import *

TAB_img = load_image("icons/TAB") # size 50 pixel
rotate_img = load_image("icons/rotate")
back_img = load_image("icons/back")
skip_img = load_image("icons/skip")

button_side_len_half = 25




def draw_bar(screen,x,y,bar_width,bar_height, current_percent, color): # x,y is a position of x,y axis of bar
    pygame.draw.rect(screen,color,[x-bar_width//2, y-bar_height//2,int(bar_width*(current_percent/100)),bar_height])

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
    center_x_level = x # fixed
    y_level = y

    total_length = len(text)
    text_blocks = []
    text_per_line = 40
    current_start = 0
    while current_start + text_per_line < total_length:
        text_blocks.append(text[current_start:current_start+text_per_line])
        current_start += text_per_line
    text_blocks.append(text[current_start:total_length])

    for i in range(len(text_blocks)):
        write_text(surf, center_x_level, y_level+i*size, text_blocks[i], size, color, bg_color)


def check_inside_button(mouse_pos,button_center, button_side_len_half):
    if abs(mouse_pos[0] - button_center[0])<=button_side_len_half and abs(mouse_pos[1] - button_center[1])<=button_side_len_half:
        return True
    else:
        return False