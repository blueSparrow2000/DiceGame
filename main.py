'''
Test version of the dice game

2024.07.21 ~

To test the basic mechanism


MANUAL
player_turn_step = 0
R: rotate the planar figure
Q: toggle planar figure to use (between primary and secondary)

player_turn_step = 1 (choose the skill to use)
1: use the first skill
2: use the second skill
3: use the third skill
...
7: basic attack
8: (defence mode) gain defence
9: heal

Click: 1) use the current planar figure on the board / player_turn_step = 0
2) If you can choose the target, do it / player_turn_step = 2

BACK: go back to the beggining (using planar figure)
RETURN: skip my turn

'''
import pygame
from player import Player
from board import *
from util import *
from skill_book import *

from area_map import *

pygame.init()  # 파이게임 초기화
clock = pygame.time.Clock()
# computer screen size: 1920 x 1080
screen = pygame.display.set_mode((width,height))  # window 생성
pygame.display.set_caption('Dice Game')  # window title
# width, height = pygame.display.get_surface().get_size()  # window width, height

screen.fill((0,0,0))  # background color



####################################################################################################### fight loop #######################################################################################################



####################################################################################################### adventure loop #######################################################################################################

####################################################################################################### character selection loop #######################################################################################################
# main screen ---------------------------------------------------

meta_run = True
while meta_run:
    # The Music in main
    music_Q('Lobby', True)
    run_character_selection = True

    ###################### call the character selecting function here! ######################


    # get the data (character name and planar figure index) and assign here!
    character_name = 'Mirinae'
    character_skills = character_skill_dictionary[character_name]
    character_tiles = character_tile_dictionary[character_name]

    planar_figure_idx = [0, 6]  # choose two between 0~9 # currently 10 planar figures available (11th one is different)
    # warning: some tiles cannot reach boss room! Becareful to choose!

    player = Player(character_name, character_skills, Board(character_tiles, planar_figure_idx))
    map = Map()
    print("Starting a new game!")

    ###### reset global data ########
    reset_altar()


    while run_character_selection:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                run_character_selection = False
                meta_run = False
                pygame.quit()
                break

            if event.type == pygame.MOUSEMOTION:
                continue
            if event.type == pygame.MOUSEBUTTONUP:
                sound_effects['confirm'].play()
                (xp, yp) = pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(), (xp, yp)))

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                    run_character_selection = False
                    meta_run = False
                    pygame.quit()
                    break
                elif event.key == pygame.K_RETURN:
                    run_character_selection = False

                    #### set character abilities (like fixing a tile etc) ####
                    go_to_shop(screen, clock, player)
                    # for i in range(1):
                    #     obtain_skill(screen, clock, player, 'holy_barrier')  # spell_name: string
                    #     obtain_skill(screen, clock, player, 'poison_dart')
                    # for i in range(3):
                    #     fix_a_tile(screen, clock, player,'Attack')
                    #     fix_a_tile(screen, clock, player,'Defence')

                    try_again = adventure_loop(screen, clock,player,map)
                    # player_lost,valid_termination = adventure_loop(player,map)
                    # if not valid_termination:
                    #     break
                    if not try_again:
                        meta_run = False
                    break


        if not run_character_selection:
            break

        screen.fill('dimgray')
        write_text(screen, width // 2, height // 2 - 240, 'Choose a character and press enter to start!', 20, 'gold')


        if mouse_particle_list:  # if not empty
            #print(len(mouse_particle_list))
            current_run_time = pygame.time.get_ticks()
            for mouse_particle in mouse_particle_list:
                #draw_particle(screen, mouse_particle)
                mouse_click_time = mouse_particle[0]
                position = mouse_particle[1]
                delta = (current_run_time - (mouse_click_time))/1000
                if  delta >= water_draw_time_mouse:
                    mouse_particle_list.remove(mouse_particle)
                factor = delta / water_draw_time_mouse
                radi = calc_drop_radius(factor, mouse_particle_radius)
                pygame.draw.circle(screen,option_effect_color, position, radi, particle_width_mouse)

        pygame.display.flip()
        clock.tick(game_fps)






