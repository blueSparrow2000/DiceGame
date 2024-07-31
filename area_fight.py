import random
from util import *
from enemy import *





def player_death_screen(screen,clock,player):
    print('player lost!')
    sound_effects['playerdeath'].play()
    pygame.mixer.music.stop()

    run_lost_screen = True
    while run_lost_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                    run_lost_screen = False
                    break
                elif event.key == pygame.K_RETURN:
                    run_lost_screen = False
                    break
        screen.fill(fight_bg_color)
        write_text(screen, width // 2, height // 2 - 60, 'Wasted', 30, 'red')
        write_text(screen, width // 2, height // 2, 'Press enter to quit', 20, 'red')
        pygame.display.flip()
        clock.tick(game_fps)

def player_win_screen(screen,clock,player):
    run_win_screen = True
    music_Q("cozy")
    time.sleep(0.5)
    while run_win_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                run_win_screen = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                    run_win_screen = False
                    break
                elif event.key == pygame.K_RETURN:
                    run_win_screen = False
                    break
        screen.fill(adventure_bg_color)
        write_text(screen, width // 2, height // 2 - 240, 'You won!', 30, 'gold')
        write_text(screen, width // 2, height // 2, 'Press enter to confirm', 20,
                   'gray')
        # show some items dropped etc.
        pygame.display.flip()
        clock.tick(game_fps)


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

def fight(screen, clock, player):
    global mousepos, TAB_img, rotate_img, back_img, skip_img, bottom_left_button, bottom_right_button, bottom_center_button, mob_Y_level, sound_effects, text_description_level, turn_text_level
    music_Q('Fight', True)
    current_turn = 0
    player_turn = True
    player_turn_step = 0
    number_of_targets_to_specify = 0
    enemy_targets = set()

    player.new_fight()
    # randomly generate enemy following some logic
    trial = random.randint(1, 3)
    enemy_request = ['mob' for i in range(trial)]  # string으로 받으면 Get attr함수 써서 객체로 만들어 받아옴
    if player.reached_max_depth():
        enemy_request = ['halo']  # boss fight

    enemies = []

    mob_X = width - 148 - (len(enemy_request) - 1) * (mob_side_len + mob_gap) / 2

    # Mob(my_name='enemies/mob', hp=30, hpmax=30, attack_damage=5, pos=(mob_X, mob_Y_level))
    # enemy.update_buffs()

    # determine golds / enemy drops
    enemy_drops = []
    earned_gold = 0

    for i in range(len(enemy_request)):
        enemy = None
        if enemy_request[i] == 'mob':
            enemy = Mob(pos=(mob_X, mob_Y_level), rank=1)

        elif enemy_request[i] == 'halo':
            enemy = Halo(pos=(mob_X, mob_Y_level))

        drop = enemy.get_drop()
        if drop:
            enemy_drops.append(drop)
        earned_gold += enemy.get_gold()
        # enemy.update_buffs()
        enemies.append(enemy)
        mob_X += mob_side_len + mob_gap

    game_run = True

    current_display_text = "Hover mouse on a tile for description"

    while game_run:
        if player.health <= 0:  # check player death first
            exit_fight()
            game_run = False
            print('player lost!')
            return True, True
        elif len(enemies) == 0:
            # give player these!
            player.get_gold(earned_gold)
            player.get_drop(enemy_drops)

            exit_fight()
            game_run = False
            print('player wins!')
            return False, True

        screen.fill(fight_bg_color)


        if not player_turn:  # enemy turn
            ########################################### Just after the player turn ###########################
            player.get_buff_effect()  # update buff effect every turn

            ### DELETE DEAD ENEMY ###
            safe_delete(enemies)
            ### DELETE DEAD ENEMY ###

            current_turn += 1

            for entity in enemies:
                entity.behave(player)
                # draw again
                screen.fill(fight_bg_color)
                write_text(screen, width // 2, turn_text_level, "Enemy's turn", 30, 'darkgoldenrod')
                player.draw(screen)
                player.draw_player_info_top(screen)  # Draw player main info
                for entity_draw in enemies:
                    entity_draw.draw(screen)
                pygame.display.flip()
                clock.tick_busy_loop(game_fps)
                time.sleep(0.2)

            ### DELETE DEAD ENEMY ###
            safe_delete(enemies)
            ### DELETE DEAD ENEMY ###

            ########################################### Just before the player turn starts! ###########################
            player_turn = True
            player.refresh_my_turn()
            player.board.reset()
            current_display_text = "Hover mouse on a tile for description"
            continue

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
                    if new_text is not None:  # optimization (change only when needed)
                        current_display_text = new_text

            if event.type == pygame.MOUSEBUTTONUP:
                sound_effects['confirm'].play()
                (xp, yp) = pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(), (xp, yp)))
                # do fight logic on player's turn
                if player_turn:  # listen for the inputs
                    if player_turn_step == 0:
                        if check_inside_button(mousepos, bottom_left_button, button_side_len_half):
                            player.board.net.change_planar_figure(player.confused)
                        elif check_inside_button(mousepos, bottom_right_button, button_side_len_half):
                            player.board.net.rotate_once()
                        elif check_inside_button(mousepos, bottom_center_button, button_side_len_half):
                            # skip player's turn
                            player.end_my_turn()
                            player_turn = False
                            player_turn_step = 0
                            number_of_targets_to_specify = 0
                            enemy_targets = set()
                            current_display_text = "Hover mouse on a tile for description"  # reset text
                        else:
                            valid_location = player.board.collect_tiles((xp, yp))
                            player.initialize_step_1()
                            if not valid_location:
                                pass
                            else:
                                player.push_tile_infos(valid_location)
                                player_turn_step = 1  # progress to next stage

                    elif player_turn_step == 1:  # choose skill or attack
                        if check_inside_button(mousepos, bottom_right_button, button_side_len_half):  # back
                            # go to initial stage and do it again
                            player_turn_step = 0
                            current_display_text = "Hover mouse on a tile for description"  # reset text
                            continue  # skip below

                        # check whether to transform joker tiles if exists
                        player.tile_transform_button(mousepos)

                        # basic buttons
                        process_completed, player_turn_step, number_of_targets_to_specify = player.check_activate_button(
                            mousepos)  # -1: not selected / 0,1,2: attack, defence, regen

                        if process_completed:  # defence or regen does not need to modify global variables
                            # end players turn
                            player.end_my_turn()
                            player_turn = False
                            player_turn_step = 0
                            player.board.confirm_using_tile()
                            number_of_targets_to_specify = 0
                            enemy_targets = set()
                            continue  # skip below

                        ### skill buttons here!
                        is_valid_move = False
                        skill_num = player.check_skill_button(mousepos)
                        if skill_num >= 0:
                            is_valid_move, number_of_targets_to_specify = player.skill_ready(skill_num)

                        if is_valid_move:
                            if number_of_targets_to_specify > 0:
                                player_turn_step = 2

                            else:
                                # use the skill!
                                player.use_skill(enemies)

                                player.current_skill_idx = -1
                                # end players turn
                                player.end_my_turn()
                                player_turn = False
                                player_turn_step = 0
                                player.board.confirm_using_tile()
                                number_of_targets_to_specify = 0
                                enemy_targets = set()


                    elif player_turn_step == 2:
                        if check_inside_button(mousepos, bottom_right_button, button_side_len_half):  # back
                            # go to initial stage and do it again
                            player_turn_step = 0
                            current_display_text = "Hover mouse on a tile for description"  # reset text

                            for i in range(len(enemies)):
                                enemies[i].targeted = False
                            number_of_targets_to_specify = 0
                            enemy_targets = set()
                            # continue  # skip below

                        else:
                            for i in range(len(enemies)):
                                if check_inside_button(mousepos, enemies[i].mypos, mob_side_len // 2):
                                    enemy_targets.add(enemies[i])
                                    enemies[i].targeted = True

            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 pause
                #     exit_fight()
                #     game_run = False
                #     break
                if player_turn:  # listen for the inputs
                    sound_effects['confirm'].play()
                    # if event.key == pygame.K_RETURN:    # skip player's turn
                    #     player.end_my_turn()
                    #     player_turn = False
                    #     player_turn_step = 0
                    #     number_of_targets_to_specify = 0
                    # enemy_targets = set()
                    if event.key == pygame.K_BACKSPACE:
                        # go to initial stage and do it again
                        player_turn_step = 0
                        current_display_text = "Hover mouse on a tile for description"  # reset text
                        for i in range(len(enemies)):
                            enemies[i].targeted = False
                        number_of_targets_to_specify = 0
                        enemy_targets = set()

                    if player_turn_step == 0:
                        if event.key == pygame.K_r:
                            player.board.net.rotate_once()
                        if event.key == pygame.K_TAB:
                            player.board.net.change_planar_figure(player.confused)
                    if player_turn_step == 1:
                        pass

        if not game_run:
            break



        if player_turn:
            ### DRAWING ###
            write_text(screen, width // 2, turn_text_level, "Player's turn", 30, 'gold')
            player.board.draw(screen, player_turn_step, mousepos)

            if player_turn_step == 0:  # listen for the inputs
                if check_inside_button(mousepos, bottom_left_button, button_side_len_half):
                    write_text(screen, mousepos[0] + 100, mousepos[1], "toggle planar figure", 15)
                elif check_inside_button(mousepos, bottom_right_button, button_side_len_half):
                    write_text(screen, mousepos[0] - 100, mousepos[1], "rotate planar figure", 15)

                ### DRAWING ###
                screen.blit(TAB_img, TAB_img.get_rect(center=bottom_left_button))
                screen.blit(rotate_img, rotate_img.get_rect(center=bottom_right_button))
                screen.blit(skip_img, skip_img.get_rect(center=bottom_center_button))

                player.board.net.draw_planar_figure(screen, mousepos)

            elif player_turn_step == 1:
                ### DRAWING ###
                screen.blit(back_img, back_img.get_rect(center=bottom_right_button))
                player.draw_buttons(screen)  # replace to basic move buttons - explanation is shown only when hovering
                write_text_description(screen, width // 2 + 30, text_description_level, current_display_text, 15)
                player.show_required_tiles(screen)
                player.draw_skills(screen)
                player.show_current_tiles(screen)
                # if joker is in the current tiles, you should select one!
                player.draw_tile_transform_button(screen)

            elif player_turn_step == 2:
                # immediate attack
                if number_of_targets_to_specify >= len(
                        enemies):  # if number_of_targets_to_specify >= len(enemies) # 즉 지정할 적의 수가 존재하는 적의 수보다 많을 경우, 지정할 필요 없이 바로 전체데미지 주면 되니까
                    for enemy in enemies:  # enemy_targets = set(enemies) for a faster way, but it does not change enemy.targeted = True
                        enemy_targets.add(enemy)
                        enemy.targeted = True

                # detect enemy
                listed_enemy_targets = list(enemy_targets)
                if number_of_targets_to_specify == len(listed_enemy_targets) or (
                        len(enemies) < number_of_targets_to_specify and len(enemies) == len(
                    listed_enemy_targets)):  # collected all
                    if player.current_skill_idx < 0:  # basic attack
                        player.attack(listed_enemy_targets)
                    else:
                        # use the skill!
                        player.use_skill(listed_enemy_targets)
                    for i in range(len(enemies)):
                        enemies[i].targeted = False
                        enemies[i].draw(screen)  # redraw
                    # end players turn
                    player.end_my_turn()
                    player_turn = False
                    player_turn_step = 0
                    player.board.confirm_using_tile()
                    number_of_targets_to_specify = 0
                    enemy_targets = set()

                ### DRAWING ###
                screen.blit(back_img, back_img.get_rect(center=bottom_right_button))
                write_text(screen, width // 2, height - 30, "Click the enemy to target", 15)


        # draw player
        player.draw(screen)

        # draw enemy
        for entity in enemies:
            entity.draw(screen)

        # draw effects

        # Draw player main info
        player.draw_player_info_top(screen)

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
