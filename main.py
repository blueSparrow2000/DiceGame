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

Click: 1) use the current planar figure on the board / player_turn_step = 0
2) If you can choose the target, do it / player_turn_step = 2

BACK: go back to the beggining (using planar figure)
RETURN: skip my turn

'''
import pygame
from image_processor import *
import math
from player import Player
from enemy import *
from board import *
from music import *
from map_logic import *
from util import *

pygame.init()  # 파이게임 초기화
clock = pygame.time.Clock()
# computer screen size: 1920 x 1080
width,height = 480, 960
screen = pygame.display.set_mode((width,height))  # window 생성
pygame.display.set_caption('Dice Game')  # window title
width, height = pygame.display.get_surface().get_size()  # window width, height

screen.fill((0,0,0))  # background color
game_fps = 30 #60

def exit_game():
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

# main screen ---------------------------------------------------
TAB_img = load_image("icons/TAB") # size 50 pixel
rotate_img = load_image("icons/rotate")
back_img = load_image("icons/back")
skip_img = load_image("icons/skip")

button_side_len_half = 25

tab_center = (40,height-40)
rotate_center = (width-40,height-40)
back_center = (width-40,height-40)
skip_center = (width//2,height-40)

mousepos = (0,0)

player = Player()
board = Board(player.tile_dict)

def fight():
    global mousepos,player, board,TAB_img,rotate_img
    current_turn = 0
    player_turn = True
    player_turn_step = 0

    board.reset()
    player.new_fight()
    # randomly generate enemy following some logic
    enemies = []
    enemy = Mob()
    # enemy.update_buffs()
    enemies.append(enemy)

    game_run = True


    while game_run:
        if enemy.is_dead():
            exit_fight()
            game_run = False
            print('player wins!')
            break
        elif player.health<=0:
            exit_fight()
            game_run = False
            print('player lost!')
            return True

        if not player_turn:  # enemy turn
            current_turn += 1
            # do enemy logic - if something has changed, call board.update() -> do it inside the enemy class
            for entity in enemies:
                entity.behave(player)
            player_turn = True
            player.refresh_my_turn()
            if (current_turn % 6 == 0):  # every 6th turn, reset the board
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
                break

            if event.type == pygame.MOUSEMOTION:  # player가 마우스를 따라가도록
                mousepos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
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
                        else:
                            # if chosen valid enemy
                            is_valid_enemy = False

                            # detect enemy
                            if is_valid_enemy:
                                # use the skill!
                                player.use_skill(enemies)

                                # end players turn
                                player.end_my_turn()
                                player_turn = False
                                player_turn_step = 0
                                board.confirm_using_tile()

                        # do player logic
                        # change through primary/secondary planar figures
                        # rotate the planar figure
                        # click the board
                        # select the skill


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                    exit_fight()
                    game_run = False
                    break
                if player_turn:  # listen for the inputs
                    # if event.key == pygame.K_RETURN:
                    #     # skip player's turn
                    #     player.end_my_turn()
                    #     player_turn = False
                    #     player_turn_step = 0
                    if event.key == pygame.K_BACKSPACE:
                        # go to initial stage and do it again
                        player_turn_step = 0

                    if player_turn_step == 0:
                        if event.key == pygame.K_r:
                            board.rotate_once()
                        if event.key == pygame.K_TAB:
                            board.change_planar_figure()
                    if player_turn_step == 1:
                        is_valid_move,need_to_specify_target = False,False
                        if event.key == pygame.K_1:
                            is_valid_move,need_to_specify_target = player.skill_ready(1)
                        elif event.key == pygame.K_2:
                            is_valid_move,need_to_specify_target = player.skill_ready(2)
                        elif event.key == pygame.K_3:
                            is_valid_move,need_to_specify_target = player.skill_ready(3)
                        elif event.key == pygame.K_4:
                            is_valid_move,need_to_specify_target = player.skill_ready(4)
                        elif event.key == pygame.K_5:
                            is_valid_move,need_to_specify_target = player.skill_ready(5)
                        elif event.key == pygame.K_6:
                            is_valid_move,need_to_specify_target = player.skill_ready(6)

                        if is_valid_move:
                            if need_to_specify_target:
                                player_turn_step = 2
                            else:
                                # use the skill!
                                player.use_skill(enemies)

                                # end players turn
                                player.end_my_turn()
                                player_turn = False
                                player_turn_step = 0
                                board.confirm_using_tile()



                        if event.key == pygame.K_7 and player.can_attack:
                            player.attack(enemies[0]) # attackes the closest enemy
                            # end players turn
                            player.end_my_turn()
                            player_turn = False
                            player_turn_step = 0
                            board.confirm_using_tile()
                        if event.key == pygame.K_8:
                            player.defend()
                            # end players turn
                            player.end_my_turn()
                            player_turn = False
                            player_turn_step = 0
                            board.confirm_using_tile()
                        if event.key == pygame.K_9:
                            player.regen()
                            # end players turn
                            player.end_my_turn()
                            player_turn = False
                            player_turn_step = 0
                            board.confirm_using_tile()


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
    # music_Q(lobbyMusic,True)
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
                    player_lost = fight()
                    if player_lost:
                        time.sleep(0.5)
                        while 1:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                                    run, meta_run = exit()
                                    break
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                                        run, meta_run = exit()
                                        break
                                    elif event.key == pygame.K_RETURN:
                                        run, meta_run = exit()
                                        break

                            screen.fill('white')
                            write_text(screen, width//2, height//2 - 60, 'Wasted',30,'red')
                            write_text(screen, width // 2, height // 2, 'Press enter to quit', 20, 'red')
                            pygame.display.flip()
                            clock.tick(game_fps)
                        meta_run = False

                    break


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






