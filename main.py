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

from variables import *
from player import Player
from board import *
from util import *
from skill_book import *
from area_map import *
from relic import *
from title_screen import *
from game_saver import *


screen.fill((0,0,0))  # background color


# main screen ---------------------------------------------------
playable_characters = ['Mirinae', 'Baron', 'Cinavro'] #,'Narin', 'Riri', 'Arisu','Ato'
dummy_net = Net([0],50,100)


first_run = True
music_Q('Lobby', True)

meta_run = True

while meta_run:
    transition_screen_obj.init_goto()
    random.seed(None) # initialize seed
    map = Map()

    if not first_run:
        music_Q('Lobby', True)     # The Music in main

    quit_flag, new_game, load_game_player = title_screen(screen, clock)
    if quit_flag:
        pygame.quit()
        break

    if not new_game:
        # load game을 이용하여 새로운 게임을 시작함
        ############## game start module #################
        # game_win_screen(screen,clock,player)
        transition_screen_obj.exit_screen(screen, clock)
        try_again = adventure_loop(screen, clock, load_game_player, map)
        first_run = False
        if not try_again:
            meta_run = False
        continue
        ############## game start module #################

    run_character_selection = True
    mousepos = (0, 0)

    print("Starting a new game!")

    ### change planar figure ###
    planar_figure_text_Y_level = 100
    planar_figure_phase = 0 # 0 or 1 etc.
    planar_figure_indices = [i for i in range(len(planar_figures))]
    # choose two between 0~9 # currently 10 planar figures available (11th one is different)]
    planar_figure_idx = [0, 3] # [1,2,3] etc. you can expand to use more tiles
    ### change planar figure ###

    ### change character ###
    character_index = 0
    character_name = playable_characters[character_index]
    ### change character ###

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

                ### change planar figure ###
                add_button, subtract_button = check_inside_button(mousepos, right_upper_button, button_side_len_half), check_inside_button(mousepos, left_upper_button, button_side_len_half)
                if planar_figure_phase < len(planar_figure_idx) and (add_button or subtract_button):
                    if add_button:
                        planar_figure_idx[planar_figure_phase] = (planar_figure_idx[planar_figure_phase]+1)%(len(planar_figures))
                    elif subtract_button:
                        planar_figure_idx[planar_figure_phase] = (planar_figure_idx[
                                                                             planar_figure_phase] - 1) % (
                                                                                    len(planar_figures))

                if planar_figure_phase > 0 and check_inside_button(mousepos, right_side_button, button_side_len_half): # back
                    planar_figure_phase -= 1 # go to set primary planar figure again

                if planar_figure_phase < len(planar_figure_idx) and check_inside_button(mousepos, right_side_upper_button, button_side_len_half): # confirm shape
                    planar_figure_phase += 1
                ### change planar figure ###


                if check_inside_button(mousepos, bottom_center_button, button_side_len_half): # confirmed
                    # set player
                    character_skills = character_skill_dictionary[character_name]
                    character_tiles = character_tile_dictionary[character_name]
                    player = Player(character_name, character_skills, Board(character_tiles, planar_figure_idx))

                    run_character_selection = False
                    if character_name=="Mirinae":   # , 'Cinavro', 'Baron'
                        fix_a_tile(screen, clock, player, 'Attack')
                        # player.pick_up_relic(BagOfDagger())
                    elif character_name=="Baron":
                        fix_a_tile(screen, clock, player, 'Defence')
                        # player.pick_up_relic(IronPlate())
                    elif character_name=="Riri":
                        fix_a_tile(screen, clock, player, 'Regen')

                    #### set character abilities here (like fixing a tile etc) ####
                    # player.pick_up_relic(Relic()) #
                    # player.pick_up_relic(SerpentHeart())  #
                    # player.golds = 1000
                    # player.gamemode = 'creator'
                    # player.pick_up_relic(Rapier())
                    # for i in range(23):
                    #     player.pick_up_relic(SerpentHeart())
                    # player.pick_up_relic(BlueCube())
                    # for i in range(1):
                    #     player.pick_up_relic(Dagger())
                    # player.pick_up_relic(BlackCube())
                    # for i in range(30):

                    #     go_to_ruin(screen, clock, player, False)
                    # for i in range(10):
                    #     go_to_shop(screen, clock, player)
                    # obtain_skill(screen, clock, player, 'holy_barrier')
                    # for i in range(3):
                    #     go_to_altar(screen, clock, player)
                    # go_to_campfire(screen, clock, player)
                    # for i in range(10):
                    #     go_to_shop(screen, clock, player)
                    # for i in range(20):
                    #     go_to_ruin(screen, clock, player, True)
                    # for i in range(1):
                    #     obtain_skill(screen, clock, player, 'holy_barrier')  # spell_name: string
                    #     obtain_skill(screen, clock, player, 'poison_dart')
                    # for i in range(3):
                    #     fix_a_tile(screen, clock, player,'Attack')
                    #     fix_a_tile(screen, clock, player,'Defence')

                    # player.pick_up_relic(Candle())
                    # player.pick_up_relic(RecycledSword())
                    # for i in range(20):
                    #     player.pick_up_relic(TiltedScale())
                    # for i in range(10):
                    #     player.pick_up_relic(Paranoia())
                    # for i in range(3):
                    #     player.pick_up_relic(WhiteCube())
                    #
                    # player.pick_up_relic(BlueCube())
                    # for i in range(10):
                    #     player.pick_up_relic(RedCube())
                    # if not first_run:
                    #     # 일종의 축복 스타터 보너스..? 유물 개수 24개 제한이니 없는게 나을지도..?
                    #     player.pick_up_relic(GoldenClover())
                    ############## game start module #################
                    # game_win_screen(screen,clock,player)
                    transition_screen_obj.exit_screen(screen, clock)
                    try_again = adventure_loop(screen, clock, player, map)
                    first_run = False
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
                #     first_run = False
                #     if not try_again:
                #         meta_run = False
                #     break


        if not run_character_selection:
            break

        screen.fill('dimgray')
        write_text(screen, width // 2, 40, 'Choose two nets', 20, 'gold')

        # draw button
        if check_inside_button(mousepos, bottom_center_button, button_side_len_half):
            write_text(screen, bottom_center_button[0], bottom_center_button[1], "confirm", 15)
        else:
            screen.blit(confirm_img, confirm_img.get_rect(center=bottom_center_button))

        ### change character ###
        write_text(screen, width // 2, middle_button_Y_level - 40, 'Choose a character', 20, 'gold')
        global_dummy_player.draw_character(screen,mousepos) # draw character attributes

        draw_toggle_button(screen, mousepos, right_button, right_button_gold, right_middle_button, button_side_len_half)
        draw_toggle_button(screen, mousepos, left_button, left_button_gold, left_middle_button, button_side_len_half)

        ### change character ###


        ### change planar figure ###
        if planar_figure_phase == 0:
            write_text(screen, width//2 + 75,planar_figure_text_Y_level, 'primary',20)
        elif 0< planar_figure_phase < len(planar_figure_idx):
            write_text(screen, width // 2 + 75, planar_figure_text_Y_level, 'secondary', 20)
        if planar_figure_phase < len(planar_figure_idx):
            screen.blit(confirm_img, confirm_img.get_rect(center=right_side_upper_button))
            current_figure = planar_figures[planar_figure_idx[planar_figure_phase]]

            dummy_net.draw_net_on_location(screen, [ width // 2 - 75, planar_figure_text_Y_level + 50 ], given_shape=current_figure)
            # for i in range(len(current_figure)):
            #     write_text(screen, width // 2 - 100, planar_figure_text_Y_level + 50 + i*20, "%s"%(current_figure[i]), 15)

        draw_toggle_button(screen, mousepos, back_img, back_img_gold, right_side_button, button_side_len_half)

        draw_toggle_button(screen, mousepos, right_button, right_button_gold, right_upper_button, button_side_len_half)
        draw_toggle_button(screen, mousepos, left_button, left_button_gold, left_upper_button, button_side_len_half)

        ### change planar figure ###


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

        transition_screen_obj.opening()
        pygame.display.flip()
        clock.tick(slow_fps)






