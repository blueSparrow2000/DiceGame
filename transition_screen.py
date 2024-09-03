'''
Rename the function go_to_area

'''
from image_processor import *
import pygame

class TransitionScreen():
    def __init__(self, screen):
        self.transition_on = True

        self.shadow_down = pygame.transform.smoothscale(load_image("background/shadow_down"), (width, height))
        self.shadow_up = pygame.transform.smoothscale(load_image("background/shadow_up"), (width, height))
        self.screen = screen
        self.y =height//2 # 0#height//2

        self.tolerance = 10
        self.transition_step = self.tolerance

        self.exit_complete = False
        self.goto_complete = False

    def init_goto(self):
        self.y = height//2
        self.goto_complete = False

    def init_exit(self):
        self.y = 0
        self.exit_complete = False

    def calc_screen_speed(self, target):
        amount = abs(target - self.y) // self.transition_step
        return amount

    def closing_screen(self):
        self.y -= self.calc_screen_speed(-30)
        self.screen.blit(self.shadow_down, (0, self.y))
        self.screen.blit(self.shadow_up, (0, -self.y))

        if self.y <= self.tolerance and not self.goto_complete:
            self.init_exit() # next move is exit
            self.goto_complete = True

            # print("done!")

    def opening(self):
        if not self.transition_on:
            return
        self.y += self.calc_screen_speed(height//2)
        self.screen.blit(self.shadow_down, (0, self.y))
        self.screen.blit(self.shadow_up, (0, -self.y))

        if self.y >= height//2 - self.tolerance and not self.exit_complete:
            self.init_goto() # next move is goto
            self.exit_complete = True

    def exit_screen(self,screen, clock):
        if not self.transition_on:
            return
        while not self.goto_complete:
            self.closing_screen()
            pygame.display.flip()
            clock.tick(slow_fps)
        screen.fill("black")
        pygame.display.flip()

        # some busy loop
        tick = 0
        while tick <= 5:
            tick+=1
            clock.tick(slow_fps)

transition_screen_obj = TransitionScreen(screen)



