import random
from util import *
from enemy import *
from variables import *




def player_death_screen(screen,clock,player):
    sound_effects['playerdeath'].play()
    pygame.mixer.music.stop()
    mousepos = (0,0)
    run_lost_screen = True
    while run_lost_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                return False
            if event.type == pygame.MOUSEMOTION:  # player가 마우스를 따라가도록
                mousepos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                sound_effects['confirm'].play()
                mousepos = pygame.mouse.get_pos()
                # do fight logic on player's turn
                if check_inside_button(mousepos, bottom_center_button, button_side_len_half): # confirmed
                    # exit
                    run_lost_screen = False
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                    run_lost_screen = False
                    break
                elif event.key == pygame.K_RETURN:
                    run_lost_screen = False
                    break
        screen.fill(fight_bg_color)
        write_text(screen, width // 2, height // 2 - 60, 'Wasted', 30, 'red')
        # write_text(screen, width // 2, height // 2 + 60, 'Depth record: '+str(player.current_depth), 20, 'black')
        player.draw_player_info_top(screen, mousepos)

        # draw button
        if check_inside_button(mousepos, bottom_center_button, button_side_len_half):
            write_text(screen, bottom_center_button[0], bottom_center_button[1], "confirm", 15)
        else:
            screen.blit(confirm_img, confirm_img.get_rect(center=bottom_center_button))


        pygame.display.flip()
        clock.tick(game_fps)

def player_win_screen(screen,clock,player,enemy_drops, earned_gold):
    gold_icon_location = [width//2 - 30, height//2 + 200]

    run_win_screen = True
    music_Q("cozy")
    mousepos = (0,0)
    time.sleep(0.5)
    while run_win_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                run_win_screen = False
                break
            if event.type == pygame.MOUSEMOTION:  # player가 마우스를 따라가도록
                mousepos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                sound_effects['confirm'].play()
                mousepos = pygame.mouse.get_pos()
                # do fight logic on player's turn
                if check_inside_button(mousepos, bottom_center_button, button_side_len_half): # confirmed
                    # exit
                    transition_screen_obj.exit_screen(screen, clock)
                    run_win_screen = False
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                    run_win_screen = False
                    break
                elif event.key == pygame.K_RETURN:
                    transition_screen_obj.exit_screen(screen, clock)
                    run_win_screen = False
                    break
        screen.fill(adventure_bg_color)
        write_text(screen, width // 2, height // 2 - 240, 'You won!', 30, 'gold')
        # show some gold earned
        screen.blit(gold_icon, gold_icon.get_rect(center=gold_icon_location))
        write_text(screen, gold_icon_location[0] + 50, gold_icon_location[1], '+ %d g'%earned_gold, 20, 'gold')
        # show some items dropped etc.


        # Draw player main info
        player.draw_player_info_top(screen, mousepos)

        # draw button
        if check_inside_button(mousepos, bottom_center_button, button_side_len_half):
            write_text(screen, bottom_center_button[0], bottom_center_button[1], "confirm", 15)
        else:
            screen.blit(confirm_img, confirm_img.get_rect(center=bottom_center_button))

        transition_screen_obj.opening()
        pygame.display.flip()
        clock.tick(game_fps)


def exit_fight():
    return



def safe_delete(entity_list, player):
    ### DELETE DEAD ENEMY ###
    delete_idx = []
    for i in range(len(entity_list)):
        if entity_list[i].is_dead():
            player.on_enemy_death(entity_list[i])
            delete_idx.append(i)
    delete_idx.reverse()

    for i in delete_idx:
        del entity_list[i]
    ### DELETE DEAD ENEMY ###

    # update enemy list here
    for entity in entity_list:
        entity.enemy_list = entity_list




def fight(screen, clock, player, place = None):
    global TAB_img, rotate_img, back_img, skip_img, bottom_left_button, bottom_right_button, bottom_center_button, mob_Y_level, sound_effects, text_description_level, turn_text_level

    current_turn = 0
    player_turn = True
    player_turn_step = 0
    number_of_targets_to_specify = 0
    enemy_targets = set()
    mousepos = (0,0)
    busy_drawing_ticks = 20
    battle_finished = False

    background_color = fight_bg_color
    if place=="ruin": # ruins fight
        background_color ='darkseagreen'
        ### different enemy spawn requests
    elif player.reached_max_depth(): # boss fight
        background_color = terracotta


    #################### randomly generate enemy following some logic ##################
    enemy_request = []
    candidate_enemy_list = []

    enemies_by_depth = {1:['mob', 'fragment', 'lenz', 'mine', 'norm', 'scout', 'observer', 'sentinel'], 2:[ 'embryo', 'scalpion', 'snider','snalk','apostle'], 3:[ 'parasite','urchin','operator', 'guard','wall','ikarus'], 'ruin':['stem', 'beast', 'raider', 'shatter','golem']}
    params_by_depth = {1:[[25, 8.6] , [30, 6.8],[50, 6.2],[50, 6.2],[80,5.4],[73,6.3],[80,5.4],[80,5.4] ], 2:[[25, 8.6], [30, 6.8], [50, 6.2],[50, 6.2],[95,5.4]], 3:[[25, 8.6], [30, 6.8],[50, 6.2],[50, 6.2],[73,6.3],[90,5.4]], 'ruin':[[40, 14] , [60, 9.6],[110, 13],[120, 10],[135,9]]}

    cur_depth = player.get_depth()

    if player.reached_max_depth(): # boss fight happens whenever depth is on -300
        music_Q('BossTheme', True)
        enemy_request = ['halo']  # boss fight
    elif place == "ruin": # for the ruin, we summon different mobs

        if player.check_ruin_boss():
            music_Q('Trick_style', True)
            enemy_request = ['watcher', 'shatter', 'golem']  # you are so dead
            player.killed_watcher = True
        else:
            music_Q('Anxiety', True)
            ### use ruin enemies ###
            cur_depth = player.get_depth()
            candidate_enemy_list = enemies_by_depth['ruin']
            current_params = params_by_depth['ruin']

            enemy_request = get_request(cur_depth, candidate_enemy_list,
                                        current_params)  # use the whole depth for ruins!
    elif player.check_primary_boss():# for boss stages, we summon these instead
        # enemy_request = ['carrier','observer','sentinel']
        music_Q('Encounter', True)
        enemy_request = ['carrier']
        player.proceed_next_boss_stage()
    elif player.check_secondary_boss():# for boss stages, we summon these instead
        music_Q('Aquatic', True)
        enemy_request = ['silent','embryo','embryo']
        player.proceed_next_boss_stage()
    else:
        music_Q('Fight', True)
        candidate_enemy_list = enemies_by_depth[abs(cur_depth) // 100 + 1]
        current_params = params_by_depth[abs(cur_depth) // 100 + 1]

        effective_depth = - (abs(cur_depth) % 100)  # make depth to -100 ~ 0 range (for each stage)
        enemy_request = get_request(effective_depth, candidate_enemy_list, current_params)
    #####################################################################################
    # enemy_request = ['raider'for i in range(3)] #
    # enemy_request = ['wall','ikarus']
    # enemy_request =['halo']

    enemies = []
    mob_number_cap = 3
    # mob_X = width - 148 - (len(enemy_request) - 1) * (mob_side_len + mob_gap) / 2
    mob_locations = [width - 148 + ( mob_side_len + mob_gap ) * (i - 1) for i in range(mob_number_cap)]

    for i in range(len(enemy_request)):
        spawn_enemy(enemies, enemy_request[i],mob_number_cap, mob_locations)

    # determine golds / enemy drops
    enemy_drops = []
    earned_gold = 0
    for enemy in enemies:
        drop = enemy.get_drop() # drops and gold is determined here (summoned enemies do not give extra gold. They are already considered into the summoner's reward)
        if drop:
            enemy_drops.append(drop)
        earned_gold += enemy.get_gold()

    #########################################
    player.new_fight(enemies)

    game_run = True
    current_display_text = "Hover mouse on a tile for description"
    while game_run:
        if player.death_check():  # check player death first
            exit_fight()
            game_run = False
            print('player lost!')
            # transition_screen_obj.exit_screen(screen, clock)
            return True, True,enemy_drops, earned_gold
        elif len(enemies) == 0:
            # give player these!

            busy_drawing_ticks -= 1
            if not battle_finished:
                print('player wins!')
                battle_finished = True
                pygame.mixer.music.stop()  # no music

            if busy_drawing_ticks <= 0 and battle_finished:
                earned_gold = player.get_gold(earned_gold)
                player.get_drop(enemy_drops)

                exit_fight()
                transition_screen_obj.exit_screen(screen, clock)
                game_run = False
                return False, True,enemy_drops, earned_gold
        ### DELETE DEAD ENEMY ###
        safe_delete(enemies, player)
        ### DELETE DEAD ENEMY ###

        screen.fill(background_color)


        if not player_turn and (not battle_finished):  # enemy turn
            ########################################### Just after the player turn ###########################
            player.get_buff_effect(enforced=False)  # update buff effect every turn
            player.board_reset(enemies) # clear board just after the player's turn!

            ### DELETE DEAD ENEMY ###
            safe_delete(enemies, player)
            ### DELETE DEAD ENEMY ###

            if player.kill_all:
                enemies = []

            current_turn += 1

            for entity in enemies:
                entity.behave(player, enemies)
                # check enemy death
                # draw again
                screen.fill(background_color)
                write_text(screen, width // 2, turn_text_level, "Enemy's turn", 30, 'darkgoldenrod')
                pygame.display.update((0, turn_text_level - 15, width, 30))

                player.draw(screen, mousepos, fast_draw = True)
                # pygame.display.update((0, turn_text_level - 15, width, 30))
                player.draw_giant_hp_only(screen, fast_draw = True)

                for entity_draw in enemies:
                    entity_draw.draw(screen,mousepos, fast_draw = True)
                # pygame.display.flip()

                clock.tick_busy_loop(game_fps)
                time.sleep(0.3)

            # watch for new spawnings!
            for entity in enemies:
                if entity.spawn_request:
                    spawn_enemy(enemies, entity.get_spawn_mob_name(), mob_number_cap, mob_locations)

            player.fissure_attack(enemies)

            ### DELETE DEAD ENEMY ###
            safe_delete(enemies,player)
            ### DELETE DEAD ENEMY ###



            ########################################### Just before the player turn starts! ###########################
            player_turn = True
            if not (len(enemies) == 0 or player.health <= 0): # player's turn is refreshed only when game did not end!
                player.refresh_my_turn()
            current_display_text = "Hover mouse on a tile for description"
            continue

        if (not battle_finished):
            events = pygame.event.get()
            # Event handling
            keys = pygame.key.get_pressed()  # 꾹 누르고 있으면 계속 실행되는 것들 # SHOULD BE CALLED AFTER pygame.event.get()!

            if keys[pygame.K_f]:
                pass
            for event in events:
                if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                    exit_fight()
                    game_run = False
                    return True, False,enemy_drops, earned_gold

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
                                # player.board.confirm_using_tile()
                                player.end_my_turn(enemies)
                                player_turn = False
                                player_turn_step = 0
                                number_of_targets_to_specify = 0
                                enemy_targets = set()
                                current_display_text = "Hover mouse on a tile for description"  # reset text
                                continue  # skip below
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
                                player.board.confirm_using_tile()
                                player.end_my_turn(enemies)
                                player_turn = False
                                player_turn_step = 0
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

                                    # end players turn
                                    player.board.confirm_using_tile()
                                    player.end_my_turn(enemies)
                                    player_turn = False
                                    player_turn_step = 0
                                    number_of_targets_to_specify = 0
                                    enemy_targets = set()
                                    continue  # skip below
                            else:
                                player.reset_skill_idx()


                        elif player_turn_step == 2:
                            if check_inside_button(mousepos, bottom_right_button, button_side_len_half):  # back
                                # go to initial stage and do it again
                                player_turn_step = 0
                                player.reset_skill_idx()
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
                        #     player.end_my_turn(enemies)
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

        if player_turn and (not battle_finished):
            ### DRAWING ###
            write_text(screen, width // 2, turn_text_level, "Your turn", 30, 'darkgoldenrod')
            player.board.draw(screen, player_turn_step, mousepos)

            if player_turn_step == 0:  # listen for the inputs
                if check_inside_button(mousepos, bottom_left_button, button_side_len_half):
                    write_text(screen, mousepos[0] + 100, mousepos[1], "toggle planar figure", 15)
                elif check_inside_button(mousepos, bottom_right_button, button_side_len_half):
                    write_text(screen, mousepos[0] - 100, mousepos[1], "rotate planar figure", 15)

                ### DRAWING ###
                screen.blit(TAB_img, TAB_img.get_rect(center=bottom_left_button))
                screen.blit(rotate_img, rotate_img.get_rect(center=bottom_right_button))
                draw_toggle_button(screen, mousepos, skip_img, skip_img_white, bottom_center_button, button_side_len_half)

                player.board.net.draw_planar_figure(screen, mousepos)

            elif player_turn_step == 1:
                ### DRAWING ###
                screen.blit(back_img, back_img.get_rect(center=bottom_right_button))
                player.draw_buttons(screen)  # replace to basic move buttons - explanation is shown only when hovering
                write_text_description(screen, width // 2 + 30, text_description_level, current_display_text, 15)
                player.show_required_tiles(screen)
                player.draw_skills(screen)
                player.show_current_tiles(screen, mousepos)
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
                        enemies[i].draw(screen,mousepos)  # redraw
                    # end players turn
                    player.board.confirm_using_tile()
                    player.end_my_turn(enemies)
                    player_turn = False
                    player_turn_step = 0
                    number_of_targets_to_specify = 0
                    enemy_targets = set()
                    continue  # skip below

                ### DRAWING ###
                screen.blit(back_img, back_img.get_rect(center=bottom_right_button))
                write_text(screen, width // 2, height - 30, "Click the enemy to target", 15)


        # draw player
        player.draw(screen,mousepos)

        # draw enemy
        for entity in enemies:
            entity.draw(screen,mousepos)

        # draw effects

        # Draw player main info
        player.draw_player_info_top(screen, mousepos)

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

        transition_screen_obj.opening()
        pygame.display.flip()
        clock.tick_busy_loop(fast_fps)
