import pygame
from image_processor import *
import time
from music import *
from variables import *
import math
import random


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
    if not (0 <= y <= height):
        return
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
def write_text_description(surf, x, y, text, size,color='black',bg_color = None, requirement_shown = True, requirement_pos = []):
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

    if requirement_shown:
        req_tile_x, req_tile_y = center_x_level, requirement_level
        if not requirement_pos == []:
            req_tile_x, req_tile_y = requirement_pos

        write_text(surf, req_tile_x, req_tile_y, "~ Requirements ~", 20, color, bg_color)




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

def safe_delete_dict_one(dictionary, target_tile):
    if target_tile in dictionary: # only when exists
        if (dictionary[target_tile]<=0):
            print("WARNING: possible error in the code (not deleted properly somewhere)\nREASON: Delete entity with amount 0 or less than 0")
        dictionary[target_tile] -= 1
        if dictionary[target_tile] <= 0: # delete entry if no longer exist
            del dictionary[target_tile]


def string_capitalizer(input):
    output = input
    if 'a' <= input[0] <= 'z':
        output = input[0].upper() + input[1:]
    return output


########### for traversal
class Node():
    final_path = []  # class variable
    final_coord_path = []  # path of tile coordinates excluding target (final) tile

    def __init__(self, how_to_get_here, parent_node, my_coord, bridge_map, target_loc):
        self.how_to_get_here = how_to_get_here
        self.parent_node = parent_node
        self.my_coord = my_coord
        self.childs = []

        ## global references
        self.bridge_map = bridge_map
        self.target_loc = target_loc  # [col,row]

    def init_class_var(self):
        Node.final_path = []  # class variable
        Node.final_coord_path = []  # path of tile coordinates excluding target (final) tile

    def found_target(self, how_to_get_child):  # make final path correctly

        # print("found target!")
        Node.final_path.append(how_to_get_child)  # the last step to reach a child
        cur_node = self
        while cur_node is not None:
            # print(cur_node.my_coord)
            Node.final_path.append(cur_node.how_to_get_here)
            Node.final_coord_path.append(cur_node.my_coord)
            cur_node = cur_node.parent_node

        Node.final_path.reverse()
        Node.final_coord_path.reverse()

    def find_target(self):  # [col, row]
        neighbors = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        how_to_get_moves = [[0, 0, 50, 0], [0, 0, 0, 50], [50, 0, 0, 0], [0, 50, 0, 0]]  # [+x, -x, +y, -y]
        for idx in range(len(neighbors)):
            col_diff, row_diff = neighbors[idx]
            how_to_get_child = how_to_get_moves[idx]
            coord = [self.my_coord[0] + col_diff, self.my_coord[1] + row_diff]
            if coord == self.target_loc:  # self.map[coord[0]][coord[1]][0]
                self.found_target(how_to_get_child)
                return True
            elif self.bridge_map[coord[0]][coord[1]]:  # if neighbor is a bridge - parent==None will not happen
                if self.parent_node is None:  # just do it
                    self.childs.append(Node(how_to_get_child, self, coord, self.bridge_map, self.target_loc))
                elif coord != self.parent_node.my_coord:
                    self.childs.append(Node(how_to_get_child, self, coord, self.bridge_map, self.target_loc))

        for child in self.childs:
            if child.find_target():
                return True
        # print("Map path finder: one branch failed in Depth first search")