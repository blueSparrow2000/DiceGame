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
import time

import pygame
from image_processor import *
import math
from player import Player
from enemy import *
from board import *
from music import *
from map_logic import *
from util import *
import random
from skill_book import *
from map_logic import *
from area_ruin import *
from area_campfire import *
from area_altar import *
from area_shop import *


pygame.init()  # 파이게임 초기화
clock = pygame.time.Clock()
# computer screen size: 1920 x 1080
width,height = 480, 960
screen = pygame.display.set_mode((width,height))  # window 생성
pygame.display.set_caption('Dice Game')  # window title
width, height = pygame.display.get_surface().get_size()  # window width, height

screen.fill((0,0,0))  # background color


def exit():
    pygame.quit()
    return False, False

def exit_fight():
    return



def safe_delete(entity_list):
    ### DELETE DEAD ENEMY ###
    delete_idx = []
    for i in range(len(entity_list)):
        if entity_list[i].is_dead():
            delete_idx.append(i)
    delete_idx.reverse()
    for i in delete_idx:
        del entity_list[i]
    ### DELETE DEAD ENEMY ###

# main screen ---------------------------------------------------
tab_center = (40,height-40)
rotate_center = (width-40,height-40)
back_center = (width-40,height-40)
skip_center = (width//2,height-40)

mousepos = (0,0)

##### choose character here...
character_name = 'Mirinae'
character_skills = character_skill_dictionary[character_name]
player = Player(character_name,character_skills)
board = Board(player.tile_dict)
map = Map()
####################################################################################################### fight loop #######################################################################################################
def fight():
    global mousepos,player, board,TAB_img,rotate_img, back_img,skip_img ,tab_center,rotate_center,back_center,skip_center ,mob_Y_level, sound_effects ,text_description_level,turn_text_level
    music_Q('Fight', True)
    current_turn = 0
    player_turn = True
    player_turn_step = 0
    number_of_targets_to_specify = 0
    enemy_targets = set()

    board.reset(True)

    player.new_fight()
    # randomly generate enemy following some logic
    trial = random.randint(1,3)
    enemy_request = ['Mob' for i in range(trial)] # string으로 받으면 Get attr함수 써서 객체로 만들어 받아옴
    
    enemies = []
    enemy_num = len(enemy_request) # at most three
    
    mob_side_len = 64
    mob_gap = 28
    mob_X = 332 - (enemy_num-1)*(mob_side_len+mob_gap)/2

    for i in range(enemy_num):
        enemy = Mob(my_name = 'enemies/mob', hp=30, hpmax = 30, attack_damage = 5,pos = (mob_X,mob_Y_level))
        # enemy.update_buffs()
        enemies.append(enemy)
        mob_X += mob_side_len + mob_gap

    game_run = True

    current_display_text = ""

    while game_run:
        if player.health<=0: # check player death first
            sound_effects['playerdeath'].play()
            exit_fight()
            game_run = False
            print('player lost!')
            return True, True
        elif len(enemies)==0:
            exit_fight()
            game_run = False
            print('player wins!')
            return False, True


        if not player_turn:  # enemy turn
            ########################################### Just after the player turn ###########################

            ### DELETE DEAD ENEMY ###
            safe_delete(enemies)
            ### DELETE DEAD ENEMY ###

            current_turn += 1
            # do enemy logic - if something has changed, call board.update() -> do it inside the enemy class
            for entity in enemies:
                entity.behave(player)
                player.get_buff_effect() # update buff effect every turn
                # draw again
                screen.fill('white')
                write_text(screen, width // 2, turn_text_level, "Enemy's turn", 30, 'darkgoldenrod')
                player.draw(screen)
                player.draw_player_info_top(screen) # Draw player main info
                for entity in enemies:
                    entity.draw(screen)
                pygame.display.flip()

            ### DELETE DEAD ENEMY ###
            safe_delete(enemies)
            ### DELETE DEAD ENEMY ###

            ########################################### Just before the player turn starts! ###########################
            player_turn = True
            player.refresh_my_turn()
            board.reset()


        screen.fill('white')

        events = pygame.event.get()
        # Event handling
        keys = pygame.key.get_pressed()  # 꾹 누르고 있으면 계속 실행되는 것들 # SHOULD BE CALLED AFTER pygame.event.get()!

        if keys[pygame.K_f]:
            pass
        for event in events:
            if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                exit_fight()
                game_run = False
                return True, False

            if event.type == pygame.MOUSEMOTION:  # player가 마우스를 따라가도록
                mousepos = pygame.mouse.get_pos()
                if player_turn_step == 1:  # choose skill or attack
                    new_text = player.my_turn_lookahead(mousepos)
                    if new_text is not None: # optimization (change only when needed)
                        current_display_text = new_text

            if event.type == pygame.MOUSEBUTTONUP:
                sound_effects['confirm'].play()
                (xp, yp) = pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(), (xp, yp)))
                # do fight logic on player's turn
                if player_turn:  # listen for the inputs
                    if player_turn_step == 0:
                        if check_inside_button(mousepos, tab_center, button_side_len_half):
                            board.change_planar_figure(player.confused)
                        elif check_inside_button(mousepos, rotate_center, button_side_len_half):
                            board.rotate_once()
                        elif check_inside_button(mousepos, skip_center, button_side_len_half):
                            # skip player's turn
                            player.end_my_turn()
                            player_turn = False
                            player_turn_step = 0
                            number_of_targets_to_specify = 0
                            enemy_targets = set()
                            current_display_text = ""  # reset text
                        else:
                            valid_location = board.collect_tiles((xp, yp))
                            player.initialize_step_1()
                            if not valid_location:
                                pass
                            else:
                                player.push_tile_infos(valid_location)
                                player_turn_step = 1 # progress to next stage

                    elif player_turn_step == 1: # choose skill or attack
                        if check_inside_button(mousepos, back_center, button_side_len_half): # back
                            # go to initial stage and do it again
                            player_turn_step = 0
                            current_display_text = ""  # reset text
                            continue  # skip below

                        # basic buttons
                        process_completed, player_turn_step,number_of_targets_to_specify = player.check_activate_button(mousepos) # -1: not selected / 0,1,2: attack, defence, regen

                        if process_completed: # defence or regen does not need to modify global variables
                            # end players turn
                            player.end_my_turn()
                            player_turn = False
                            player_turn_step = 0
                            board.confirm_using_tile()
                            number_of_targets_to_specify = 0
                            enemy_targets = set()
                            continue # skip below


                        ### skill buttons here!
                        is_valid_move = False
                        skill_num = player.skill_book.check_button(mousepos)
                        if skill_num >= 0:
                            is_valid_move,number_of_targets_to_specify = player.skill_ready(skill_num)

                        if is_valid_move:
                            if number_of_targets_to_specify>0:
                                player_turn_step = 2

                            else:
                                # use the skill!
                                player.use_skill(enemies)

                                player.current_skill_idx = -1
                                # end players turn
                                player.end_my_turn()
                                player_turn = False
                                player_turn_step = 0
                                board.confirm_using_tile()
                                number_of_targets_to_specify = 0
                                enemy_targets = set()


                    elif player_turn_step == 2:
                        if check_inside_button(mousepos, back_center, button_side_len_half):
                            # go to initial stage and do it again
                            player_turn_step = 0
                            current_display_text = ""  # reset text

                            for i in range(len(enemies)):
                                enemies[i].targeted = False
                            number_of_targets_to_specify = 0
                            enemy_targets = set()
                            # continue  # skip below

                        else:
                            for i in range(len(enemies)):
                                if check_inside_button(mousepos, enemies[i].mypos, mob_side_len):
                                    enemy_targets.add(enemies[i])
                                    enemies[i].targeted = True

                            listed_enemy_targets = list(enemy_targets)
                            # detect enemy
                            if number_of_targets_to_specify==len(listed_enemy_targets) or (len(enemies)<number_of_targets_to_specify and len(enemies)==len(listed_enemy_targets)): # collected all
                                if player.current_skill_idx<0: # basic attack
                                    player.attack(listed_enemy_targets)
                                else:
                                    # use the skill!
                                    player.use_skill(listed_enemy_targets)
                                for i in range(len(enemies)):
                                    enemies[i].targeted = False
                                # end players turn
                                player.end_my_turn()
                                player_turn = False
                                player_turn_step = 0
                                board.confirm_using_tile()
                                number_of_targets_to_specify = 0
                                enemy_targets = set()

                        # do player logic
                        # change through primary/secondary planar figures
                        # rotate the planar figure
                        # click the board
                        # select the skill


            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 pause
                #     exit_fight()
                #     game_run = False
                #     break
                if player_turn:  # listen for the inputs
                    sound_effects['confirm'].play()
                    # if event.key == pygame.K_RETURN:
                    #     # skip player's turn
                    #     player.end_my_turn()
                    #     player_turn = False
                    #     player_turn_step = 0
                    #     number_of_targets_to_specify = 0
                    #enemy_targets = set()
                    if event.key == pygame.K_BACKSPACE:
                        # go to initial stage and do it again
                        player_turn_step = 0
                        current_display_text = ""  # reset text
                        for i in range(len(enemies)):
                            enemies[i].targeted = False
                        number_of_targets_to_specify = 0
                        enemy_targets = set()

                    if player_turn_step == 0:
                        if event.key == pygame.K_r:
                            board.rotate_once()
                        if event.key == pygame.K_TAB:
                            board.change_planar_figure(player.confused)
                    if player_turn_step == 1:
                        pass
                        # is_valid_move = False
                        # if event.key == pygame.K_1:
                        #     is_valid_move,number_of_targets_to_specify = player.skill_ready(0)
                        # elif event.key == pygame.K_2:
                        #     is_valid_move,number_of_targets_to_specify = player.skill_ready(1)
                        # elif event.key == pygame.K_3:
                        #     is_valid_move,number_of_targets_to_specify = player.skill_ready(2)
                        # elif event.key == pygame.K_4:
                        #     is_valid_move,number_of_targets_to_specify = player.skill_ready(3)
                        # elif event.key == pygame.K_5:
                        #     is_valid_move,number_of_targets_to_specify = player.skill_ready(4)
                        # elif event.key == pygame.K_6:
                        #     is_valid_move,number_of_targets_to_specify = player.skill_ready(5)
                        #
                        # if is_valid_move:
                        #     if number_of_targets_to_specify>0:
                        #         player_turn_step = 2
                        #
                        #     else:
                        #         # use the skill!
                        #         player.use_skill(enemies)
                        #
                        #         player.current_skill_idx = -1
                        #         # end players turn
                        #         player.end_my_turn()
                        #         player_turn = False
                        #         player_turn_step = 0
                        #         board.confirm_using_tile()
                        #         number_of_targets_to_specify = 0
                        #         enemy_targets = set()
                        #
                        #
                        #
                        # if event.key == pygame.K_7 and player.can_attack: # basic attack
                        #     player_turn_step = 2
                        #     number_of_targets_to_specify = 1
                        #
                        # if event.key == pygame.K_8:
                        #     player.defend()
                        #     # end players turn
                        #     player.end_my_turn()
                        #     player_turn = False
                        #     player_turn_step = 0
                        #     board.confirm_using_tile()
                        #     number_of_targets_to_specify = 0
                        #     enemy_targets = set()
                        # if event.key == pygame.K_9:
                        #     player.regen()
                        #     # end players turn
                        #     player.end_my_turn()
                        #     player_turn = False
                        #     player_turn_step = 0
                        #     board.confirm_using_tile()
                        #     number_of_targets_to_specify = 0
                        #     enemy_targets = set()
                        #

        if player_turn_step == 1:
            screen.blit(back_img, back_img.get_rect(center=back_center))

            # replace to basic move buttons - explanation is shown only when hovering
            player.draw_buttons(screen)

            write_text_description(screen, width // 2 + 30, text_description_level, current_display_text, 15)
            player.show_required_tiles(screen)

            player.skill_book.draw(screen)

            player.show_current_tiles(screen)

        elif player_turn_step == 2:
            screen.blit(back_img, back_img.get_rect(center=back_center))

            write_text(screen, width // 2, height - 30, "Click the enemy to target", 15)

        if not game_run:
            break


        # draw player
        player.draw(screen)

        # draw enemy
        for entity in enemies:
            entity.draw(screen)

        # draw effects

        # Draw player main info
        player.draw_player_info_top(screen)

        # if inside the border
        if player_turn:
            write_text(screen, width // 2, turn_text_level, "Player's turn", 30, 'gold')
            # draw board
            board.draw(screen, player_turn_step)


            if player_turn_step == 0:  # listen for the inputs
                if check_inside_button(mousepos, tab_center, button_side_len_half):
                    write_text(screen, mousepos[0]+100, mousepos[1], "toggle planar figure", 15)
                elif check_inside_button(mousepos, rotate_center, button_side_len_half):
                    write_text(screen, mousepos[0]-100, mousepos[1], "rotate planar figure", 15)


                write_text(screen, width // 2, height//2 - 20, "Click: confirm", 15)

                screen.blit(TAB_img, TAB_img.get_rect(center=tab_center))
                screen.blit(rotate_img, rotate_img.get_rect(center=rotate_center))
                screen.blit(skip_img, skip_img.get_rect(center=skip_center))


                if mousepos[1] >= 480:  # on the board
                    board.draw_planar_figure(screen, mousepos)
        else:
            write_text(screen, width // 2, turn_text_level, "Enemy's turn", 30, 'darkgoldenrod')

        if mouse_particle_list:  # if not empty
            # print(len(mouse_particle_list))
            current_run_time = pygame.time.get_ticks()
            for mouse_particle in mouse_particle_list:
                # draw_particle(screen, mouse_particle)
                mouse_click_time = mouse_particle[0]
                position = mouse_particle[1]
                delta = (current_run_time - (mouse_click_time)) / 1000
                if delta >= water_draw_time_mouse:
                    mouse_particle_list.remove(mouse_particle)
                factor = delta / water_draw_time_mouse
                radi = calc_drop_radius(factor, mouse_particle_radius)
                pygame.draw.circle(screen, effect_color, position, radi, particle_width_mouse)

        pygame.display.flip()
        clock.tick_busy_loop(game_fps)



####################################################################################################### adventure loop #######################################################################################################

def adventure_loop():
    global background_y, background_layer_y, board, map
    meta_run_adventure = True
    mousepos = (0,0)

    while meta_run_adventure:
        # The Music in main
        music_Q('Adventure', True)
        run_adventure = True

        map.random_initialize(player)

        board.init_turn()
        map_choosing_step = 0  # 0: placing planar figure / 1: clicking reachable map tile => fight etc

        while run_adventure:
            # keys = pygame.key.get_pressed()  # 꾹 누르고 있으면 계속 실행되는 것들
            # if keys[pygame.K_UP]:
            #     background_y += 1
            #     background_layer_y += 2
            # if keys[pygame.K_DOWN]:
            #     background_y -= 1
            #     background_layer_y -= 2

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                    run_adventure, meta_run_adventure = exit()
                    break

                if event.type == pygame.MOUSEMOTION:
                    mousepos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONUP:
                    sound_effects['confirm'].play()
                    (xp, yp) = pygame.mouse.get_pos()
                    mouse_particle_list.append((pygame.time.get_ticks(), (xp, yp)))

                    if check_inside_button(mousepos, tab_center, button_side_len_half):
                        board.change_planar_figure(False)
                    elif check_inside_button(mousepos, rotate_center, button_side_len_half):
                        board.rotate_once()

                    if map_choosing_step == 0: # check map
                        is_valid = map.check_tiles((xp, yp),board)
                        if is_valid: # goto next step (only happens here)
                            map_choosing_step = 1
                    elif map_choosing_step == 1:
                        if check_inside_button(mousepos, skip_center, button_side_len_half):  # back
                            # go to initial stage and do it again
                            map_choosing_step = 0
                            map.reset()
                            board.init_turn()
                            continue  # skip below


                        is_valid, which_event, move_depth = map.check_reachable_locations((xp, yp)) #['campfire','fight','ruin','shop','altar']
                        if is_valid:
                            player.update_depth(move_depth)
                            run_adventure = False

                            if which_event == 'campfire':
                                go_to_campfire(screen,clock, player)
                            elif which_event == 'ruin':
                                go_to_ruin(screen,clock, player)
                            elif which_event == 'shop':
                                go_to_shop(screen,clock, player)
                            elif which_event == 'altar':
                                go_to_altar(screen,clock, player)
                            elif which_event == 'fight':

                                # initialize board attributes
                                board.init_turn()
                                player_lost, valid_termination = fight()
                                board.init_turn()
                                # initialize board attributes

                                if not valid_termination:
                                    meta_run_adventure = False
                                    break

                                if player_lost:
                                    time.sleep(0.5)
                                    pygame.mixer.music.stop()
                                    screen.fill('white')
                                    write_text(screen, width // 2, height // 2 - 60, 'Wasted', 30, 'red')
                                    write_text(screen, width // 2, height // 2, 'Press enter to quit', 20, 'red')
                                    pygame.display.flip()

                                    time.sleep(2)
                                    meta_run_adventure = False

                                    break
                                else:
                                    run_win_screen = True
                                    music_Q("cozy")
                                    time.sleep(0.5)
                                    while run_win_screen:
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                                                meta_run_adventure = False
                                                run_win_screen = False
                                                break

                                            if event.type == pygame.KEYDOWN:
                                                if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                                                    run_win_screen = False
                                                    break
                                                elif event.key == pygame.K_RETURN:
                                                    run_win_screen = False
                                                    break
                                        screen.fill('seagreen')
                                        write_text(screen, width // 2, height // 2 - 240, 'You won!', 30, 'gold')
                                        write_text(screen, width // 2, height // 2, 'Press enter to confirm', 20,
                                                   'gray')
                                        # show some items dropped etc.

                                        pygame.display.flip()
                                        clock.tick(game_fps)


                        else: # not valid move => pass
                            pass

                if event.type == pygame.KEYDOWN:
                        sound_effects['confirm'].play()
                        if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                            run_adventure, meta_run_adventure = exit()
                            break
                        elif event.key == pygame.K_r:
                            board.rotate_once()
                        elif event.key == pygame.K_TAB:
                            board.change_planar_figure(False)

                        elif event.key == pygame.K_RETURN:
                            pass

            if not run_adventure:
                break

            screen.fill('seagreen')
            # screen.blit(bg_list[0], (0, background_y))
            # y_rel = background_layer_y % height
            # y_part2 = y_rel - height if y_rel > 0 else y_rel + height
            # screen.blit(layer, (0, y_rel))
            # screen.blit(layer, (0, y_part2))

            map.draw(screen)

            if map_choosing_step==1:
                map.highlight_reachable_locations(screen)
                screen.blit(back_img, back_img.get_rect(center=skip_center))

            # Draw player main info
            player.draw_player_info_top(screen)

            if map_choosing_step==0 and mousepos[1] >= 480:  # on the board
                board.draw_planar_figure(screen, mousepos)
                screen.blit(TAB_img, TAB_img.get_rect(center=tab_center))
                screen.blit(rotate_img, rotate_img.get_rect(center=rotate_center))

            if mouse_particle_list:  # if not empty
                # print(len(mouse_particle_list))
                current_run_time = pygame.time.get_ticks()
                for mouse_particle in mouse_particle_list:
                    # draw_particle(screen, mouse_particle)
                    mouse_click_time = mouse_particle[0]
                    position = mouse_particle[1]
                    delta = (current_run_time - (mouse_click_time)) / 1000
                    if delta >= water_draw_time_mouse:
                        mouse_particle_list.remove(mouse_particle)
                    factor = delta / water_draw_time_mouse
                    radi = calc_drop_radius(factor, mouse_particle_radius)
                    pygame.draw.circle(screen, adventure_effect_color, position, radi, particle_width_mouse)

            pygame.display.flip()
            clock.tick(game_fps)






####################################################################################################### character selection loop #######################################################################################################
run_character_selection = True

# The Music in main
music_Q('Lobby', True)

while run_character_selection:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
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
                pygame.quit()
                break
            elif event.key == pygame.K_RETURN:
                run_character_selection = False
                adventure_loop()
                # player_lost,valid_termination = adventure_loop()
                # if not valid_termination:
                #     break
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






