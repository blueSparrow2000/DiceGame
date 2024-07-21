import pygame
def draw_bar(screen,x,y,bar_width,bar_height, current_percent, color): # x,y is a position of x,y axis of bar
    pygame.draw.rect(screen,color,[x-bar_width//2, y-bar_height//2,int(bar_width*(current_percent/100)),bar_height])
