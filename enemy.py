import pygame
from image_processor import *
from util import *

mob_img = load_image("mob")

class Enemy():
    def __init__(self,hp, hpmax):
        self.health = hp
        self.max_health = hpmax


class Mob(Enemy):
    def __init__(self,hp=30, hpmax = 30):
        super().__init__(hp,hpmax)
        self.image = mob_img
        self.mypos = (380,400)
        self.attack = 100

    def draw(self,screen):
        screen.blit(self.image, self.image.get_rect(center=self.mypos))
        draw_bar(screen, self.mypos[0], self.mypos[1] - 60, 64, 10, 100, 'gray')
        draw_bar(screen, self.mypos[0], self.mypos[1] - 60, 64, 10, 100*self.health/self.max_health, 'red')
    def is_dead(self):
        return self.health <= 0

    def behave(self, player):
        player.take_damage(self.attack)

    def get_damage(self,damage):
        self.health -= damage