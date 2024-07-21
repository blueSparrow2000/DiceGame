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
    try:
        APP_FOLDER = IMAGE_FOLDER
        full_path = os.path.join(APP_FOLDER, '%s.png'%filename)
        #print(full_path)
        return pygame.image.load(full_path)
    except:
        print(filename)
        return None

