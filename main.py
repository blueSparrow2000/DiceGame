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

#music_Q('Lobby',True)
#music_Q('Encounter',True)




pygame.init()  # 파이게임 초기화
clock = pygame.time.Clock()
# computer screen size: 1920 x 1080
width,height = 480, 960
screen = pygame.display.set_mode((width,height))  # window 생성
pygame.display.set_caption('Dice Game')  # window title
width, height = pygame.display.get_surface().get_size()  # window width, height

screen.fill((0,0,0))  # background color
game_fps = 30 #60

def exit():
    pygame.quit()
    return False, False

def exit_fight():
    return

mouse_particle_list = []  # mouse click effects
water_draw_time = 0.8
water_draw_time_mouse = 0.6
particle_width = 6
particle_width_mouse = 3
mouse_particle_radius = 5
droplet_radius = 33
effect_color = (150, 200, 240)

def calc_drop_radius(factor,start_radius,mouse=True):  # factor is given by float between 0 and 1 (factor changes from 0 to 1)
    if not mouse:
        width = int(math.pow(3*(1-factor),3)+3.5)
    else:
        width = int(math.pow(2.5*(1-factor),3)+1.7)
    r = max(width,int(start_radius*(1+4*math.pow(factor,1/5))))
    return r

def show_nonzero_dict(dd):
    result = dict()
    for key, value in dd.items():
        if value > 0:
            result[key]=value
    return result


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


def fight():
    global mousepos,player, board,TAB_img,rotate_img, back_img,skip_img ,tab_center,rotate_center,back_center,skip_center ,mob_Y_level, sound_effects
    music_Q('Fight', True)
    current_turn = 0
    player_turn = True
    player_turn_step = 0
    number_of_targets_to_specify = 0
    enemy_targets = set()

    board.reset()
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
                write_text(screen, width // 2, 200, "Enemy's turn", 30, 'gold')
                player.draw(screen)
                for entity in enemies:
                    entity.draw(screen)
                pygame.display.flip()

            player_turn = True
            player.refresh_my_turn()
            if (current_turn % 6 == 0):  # every 6th turn, reset the board
                board.reset()

            ### DELETE DEAD ENEMY ###
            safe_delete(enemies)
            ### DELETE DEAD ENEMY ###



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

            if event.type == pygame.MOUSEBUTTONUP:
                sound_effects['confirm'].play()
                (xp, yp) = pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(), (xp, yp)))
                # do fight logic on player's turn
                if player_turn:  # listen for the inputs
                    if player_turn_step == 0:
                        if check_inside_button(mousepos, tab_center, button_side_len_half):
                            board.change_planar_figure()
                        elif check_inside_button(mousepos, rotate_center, button_side_len_half):
                            board.rotate_once()
                        elif check_inside_button(mousepos, skip_center, button_side_len_half):
                            # skip player's turn
                            player.end_my_turn()
                            player_turn = False
                            player_turn_step = 0
                            number_of_targets_to_specify = 0
                            enemy_targets = set()
                        else:
                            valid_location = board.collect_tiles((xp, yp))
                            if not valid_location:
                                pass
                            else:
                                player.push_tile_infos(valid_location)
                                player_turn_step = 1 # progress to next stage

                    elif player_turn_step == 1:
                        if check_inside_button(mousepos, back_center, button_side_len_half):
                            # go to initial stage and do it again
                            player_turn_step = 0

                    elif player_turn_step == 2:
                        if check_inside_button(mousepos, back_center, button_side_len_half):
                            # go to initial stage and do it again
                            player_turn_step = 0

                            for i in range(len(enemies)):
                                enemies[i].targeted = False
                            number_of_targets_to_specify = 0
                            enemy_targets = set()

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
                        for i in range(len(enemies)):
                            enemies[i].targeted = False
                        number_of_targets_to_specify = 0
                        enemy_targets = set()

                    if player_turn_step == 0:
                        if event.key == pygame.K_r:
                            board.rotate_once()
                        if event.key == pygame.K_TAB:
                            board.change_planar_figure()
                    if player_turn_step == 1:
                        is_valid_move = False
                        if event.key == pygame.K_1:
                            is_valid_move,number_of_targets_to_specify = player.skill_ready(0)
                        elif event.key == pygame.K_2:
                            is_valid_move,number_of_targets_to_specify = player.skill_ready(1)
                        elif event.key == pygame.K_3:
                            is_valid_move,number_of_targets_to_specify = player.skill_ready(2)
                        elif event.key == pygame.K_4:
                            is_valid_move,number_of_targets_to_specify = player.skill_ready(3)
                        elif event.key == pygame.K_5:
                            is_valid_move,number_of_targets_to_specify = player.skill_ready(4)
                        elif event.key == pygame.K_6:
                            is_valid_move,number_of_targets_to_specify = player.skill_ready(5)

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



                        if event.key == pygame.K_7 and player.can_attack: # basic attack
                            player_turn_step = 2
                            number_of_targets_to_specify = 1

                        if event.key == pygame.K_8:
                            player.defend()
                            # end players turn
                            player.end_my_turn()
                            player_turn = False
                            player_turn_step = 0
                            board.confirm_using_tile()
                            number_of_targets_to_specify = 0
                            enemy_targets = set()
                        if event.key == pygame.K_9:
                            player.regen()
                            # end players turn
                            player.end_my_turn()
                            player_turn = False
                            player_turn_step = 0
                            board.confirm_using_tile()
                            number_of_targets_to_specify = 0
                            enemy_targets = set()


        if player_turn_step == 1:
            screen.blit(back_img, back_img.get_rect(center=back_center))

            write_text(screen, width // 2, 480, 'Current tiles', 15)
            write_text(screen, width // 2, 500, '{}'.format(show_nonzero_dict(player.current_tile)), 15)
            if (player.can_attack):
                write_text(screen, width // 2, 540, '7: Attack - deals {} damage to closest enemy'.format(player.get_current_damage()), 15)
            write_text(screen, width // 2, 560, '8: Defend - gains {} temporal defence'.format(player.get_defence_gain()), 15)
            write_text(screen, width // 2, 580, '9: Regen - heals {} health'.format(player.get_heal_amount()), 15)
            write_text(screen, width // 2, 600, '1~6: Skills'.format(player.current_tile), 15)

            write_text(screen, width // 2, height - 30, "Press corresponding number key to confirm", 15)

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

        # draw board
        board.draw(screen, player_turn_step)

        # draw effects

        # if inside the border
        if player_turn:
            write_text(screen, width // 2, 200, "Player's turn", 30, 'gold')

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
            write_text(screen, width // 2, 200, "Enemy's turn", 30, 'gold')

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





# main loop - traverse through the map
run = True
meta_run = True

while meta_run:
    # The Music in main
    music_Q('Adventure', True)
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                run, meta_run = exit()
                break

            if event.type == pygame.MOUSEMOTION:
                mousepos = pygame.mouse.get_pos()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                    run, meta_run = exit()
                    break
                elif event.key == pygame.K_RETURN:
                    run = False
                    player_lost,valid_termination = fight()
                    if not valid_termination:
                        meta_run = False
                        break

                    if player_lost:
                        pygame.mixer.music.stop()
                        screen.fill('white')
                        write_text(screen, width//2, height//2 - 60, 'Wasted',30,'red')
                        write_text(screen, width // 2, height // 2, 'Press enter to quit', 20, 'red')
                        pygame.display.flip()

                        time.sleep(2)
                        meta_run = False

                        break
                    else:
                        run_win_screen = True
                        music_Q("cozy")
                        while run_win_screen:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                                    meta_run = False
                                    run_win_screen = False
                                    break

                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                                        run_win_screen = False
                                        break
                                    elif event.key == pygame.K_RETURN:
                                        run_win_screen = False
                                        break
                            screen.fill('white')
                            write_text(screen, width//2, height//2 - 240, 'You won!',30,'gold')
                            # show some items dropped etc.

                            pygame.display.flip()
                            clock.tick(game_fps)




        if not run:
            break

        screen.fill('dimgray')


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
                pygame.draw.circle(screen,effect_color, position, radi, particle_width_mouse)

        pygame.display.flip()
        clock.tick(game_fps)






