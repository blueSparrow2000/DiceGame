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



# main screen ---------------------------------------------------
playable_characters = ['Mirinae', 'Cinavro','Narin']


meta_run = True

while meta_run:
    # The Music in main
    music_Q('Lobby', True)
    run_character_selection = True
    mousepos = (0, 0)
    ###################### call the character selecting function here! ######################

    planar_figure_idx = [0, 6]  # choose two between 0~9 # currently 10 planar figures available (11th one is different)
    # get the data (character name and planar figure index) and assign here!
    character_index = 0
    character_name = playable_characters[character_index]
    # character_skills = character_skill_dictionary[character_name]
    # character_tiles = character_tile_dictionary[character_name]
    # player = Player(character_name, character_skills, Board(character_tiles, planar_figure_idx))


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
                mousepos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                sound_effects['confirm'].play()
                mousepos = pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(), mousepos))

                ### change character ###
                if check_inside_button(mousepos, right_middle_button, button_side_len_half):
                    character_index = (character_index+1)%len(playable_characters)
                    character_name = playable_characters[character_index]
                    global_dummy_player.update_char(character_name)
                elif check_inside_button(mousepos, left_middle_button, button_side_len_half):
                    character_index = (character_index-1)%len(playable_characters)
                    character_name = playable_characters[character_index]
                    global_dummy_player.update_char(character_name)
                ### change character ###


                elif check_inside_button(mousepos, bottom_center_button, button_side_len_half): # confirmed
                    # set player
                    character_skills = character_skill_dictionary[character_name]
                    character_tiles = character_tile_dictionary[character_name]
                    player = Player(character_name, character_skills, Board(character_tiles, planar_figure_idx))

                    run_character_selection = False
                    #### set character abilities here (like fixing a tile etc) ####
                    # go_to_altar(screen, clock, player)
                    # go_to_campfire(screen, clock, player)
                    # go_to_shop(screen, clock, player)
                    # for i in range(1):
                    #     obtain_skill(screen, clock, player, 'holy_barrier')  # spell_name: string
                    #     obtain_skill(screen, clock, player, 'poison_dart')
                    # for i in range(3):
                    #     fix_a_tile(screen, clock, player,'Attack')
                    #     fix_a_tile(screen, clock, player,'Defence')
                    ############## game start module #################
                    try_again = adventure_loop(screen, clock, player, map)
                    if not try_again:
                        meta_run = False
                    break
                    ############## game start module #################

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                    run_character_selection = False
                    meta_run = False
                    pygame.quit()
                    break
                # elif event.key == pygame.K_RETURN:
                #     run_character_selection = False
                #     try_again = adventure_loop(screen, clock,player,map)
                #     if not try_again:
                #         meta_run = False
                #     break


        if not run_character_selection:
            break

        screen.fill('dimgray')
        write_text(screen, width // 2, 40, 'Choose a net and a character', 20, 'gold')


        # draw button
        if check_inside_button(mousepos, bottom_center_button, button_side_len_half):
            write_text(screen, bottom_center_button[0], bottom_center_button[1], "confirm", 15)
        else:
            screen.blit(confirm_img, confirm_img.get_rect(center=bottom_center_button))

        screen.blit(right_button, right_button.get_rect(center=right_middle_button))
        screen.blit(left_button, left_button.get_rect(center=left_middle_button))



        # draw character attributes
        global_dummy_player.draw_character(screen,mousepos)



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






