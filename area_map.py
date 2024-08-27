from map_logic import *
from area_ruin import *
from area_campfire import *
from area_altar import *
from area_shop import *
from area_fight import *
from game_win_screen import *

def exit():
    pygame.quit()
    return False, False

def update_depth_color(player):
    color_limit = -100
    if player.reached_max_depth():
        depth = color_limit
    else:
        depth = max(player.current_depth//10 , color_limit)

    return (100 + depth, 130 + depth, 100 + depth)




def adventure_loop(screen, clock, player,map):
    global background_y, background_layer_y, adventure_bg_color
    adventure_bg_color = update_depth_color(player)
    meta_run_adventure = True
    mousepos = (0,0)

    while meta_run_adventure:
        # The Music in main
        if player.reached_max_depth():
            pygame.mixer.music.stop() # no music
        else:
            music_Q('Adventure', True)
        run_adventure = True

        map.random_initialize(player)

        player.board.net.init_turn()
        map_choosing_step = 0  # 0: placing planar figure / 1: clicking reachable map tile => fight etc

        # reset
        animation_block = False
        activate_tile = False
        is_valid, which_event, move_depth = False, False, 0

        if player.health <= 0:  # check player death first
            player_death_screen(screen, clock, player)
            return True  # try again for other characters

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

                if animation_block: #no event listening
                    break

                if event.type == pygame.MOUSEMOTION:
                    mousepos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONUP:
                    sound_effects['confirm'].play()
                    (xp, yp) = pygame.mouse.get_pos()
                    mouse_particle_list.append((pygame.time.get_ticks(), (xp, yp)))

                    if check_inside_button(mousepos, bottom_left_button, button_side_len_half):
                        player.board.net.change_planar_figure(False)
                    elif check_inside_button(mousepos, bottom_right_button, button_side_len_half):
                        player.board.net.rotate_once()

                    if map_choosing_step == 0: # check map
                        is_valid = map.check_tiles((xp, yp),player.board)
                        if is_valid: # goto next step (only happens here)
                            map_choosing_step = 1
                    elif map_choosing_step == 1:
                        if check_inside_button(mousepos, bottom_center_button, button_side_len_half):  # back
                            # go to initial stage and do it again
                            map_choosing_step = 0
                            map.reset()
                            player.board.net.init_turn()
                            continue  # skip below


                        is_valid, which_event, move_depth = map.check_reachable_locations((xp, yp)) #['campfire','fight','ruin','shop','altar']
                        if is_valid:
                            new_event, new_depth =  map.find_path()
                            if new_event:
                                which_event,move_depth = new_event, new_depth # 패스 파인터 실행 / 타깃 변경시 이벤트도 같이 변경되도록 만든다!!

                            # then request animation, then at the end of the animation, execute flag turns on, and animate flag turns off
                            animation_block = True


                        else: # not valid move => pass
                            pass

                if event.type == pygame.KEYDOWN:
                        sound_effects['confirm'].play()
                        if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                            run_adventure, meta_run_adventure = exit()
                            break
                        elif event.key == pygame.K_r:
                            player.board.net.rotate_once()
                        elif event.key == pygame.K_TAB:
                            player.board.net.change_planar_figure(False)

                        elif event.key == pygame.K_RETURN:
                            pass

            if not run_adventure:
                break

            screen.fill(adventure_bg_color)
            # screen.blit(bg_list[0], (0, background_y))
            # y_rel = background_layer_y % height
            # y_part2 = y_rel - height if y_rel > 0 else y_rel + height
            # screen.blit(layer, (0, y_rel))
            # screen.blit(layer, (0, y_part2))


            if animation_block:
                activate_tile = map.animate_draw(screen)
            else:
                map.draw(screen)

            if activate_tile:
                player.update_depth(move_depth)
                adventure_bg_color = update_depth_color(player)
                run_adventure = False

                if which_event == 'campfire':
                    go_to_campfire(screen, clock, player)
                elif which_event == 'ruin':
                    chance = random.randint(1, 100)

                    # relic chance increasing
                    for relic in player.relics:
                        chance -= relic.ruin_chance_increaser()
                    # relic chance increasing
                    fought = False
                    if (player.my_name == "Arisu") or chance <= 40 or player.killed_ruin_boss():  # with 40% probability => get a relic
                        pass
                    else:   # with probability 60% => elite fight
                        fought = True
                        ########################################################## go to fight #################################################
                        # initialize board attributes
                        player.board.net.init_turn()
                        player_lost, valid_termination,enemy_drops, earned_gold = fight(screen, clock, player, place = "ruin")
                        player.board.net.init_turn()
                        # initialize board attributes
                        if not valid_termination:
                            meta_run_adventure = False
                            break
                        if player_lost:
                            time.sleep(0.5)
                            ###############################
                            player_death_screen(screen, clock, player)
                            return True  # try again for other characters
                        else:
                            if player.reached_max_depth():
                                game_win_screen(screen, clock, player)
                                return True
                            else:
                                player_win_screen(screen, clock, player,enemy_drops, earned_gold)
                        ########################################################## go to fight #################################################
                    go_to_ruin(screen, clock, player, fought)


                elif which_event == 'shop':
                    go_to_shop(screen, clock, player)
                elif which_event == 'altar':
                    go_to_altar(screen, clock, player)
                elif which_event == 'fight':
                    ########################################################## go to fight #################################################
                    # initialize board attributes
                    player.board.net.init_turn()
                    player_lost, valid_termination,enemy_drops, earned_gold = fight(screen, clock, player)
                    player.board.net.init_turn()
                    # initialize board attributes
                    if not valid_termination:
                        meta_run_adventure = False
                        break
                    if player_lost:
                        time.sleep(0.5)
                        ###############################
                        player_death_screen(screen, clock, player)
                        return True # try again for other characters
                    else:
                        if player.reached_max_depth():
                            game_win_screen(screen, clock, player)
                            return True
                        else:
                            player_win_screen(screen, clock, player,enemy_drops, earned_gold)
                    ########################################################## go to fight #################################################


            # Draw player main info
            player.draw_player_info_top(screen, mousepos)
            screen.blit(shadow_layer, (0, 0))

            if map_choosing_step==1 and not animation_block:
                map.highlight_reachable_locations(screen)
                screen.blit(back_img_white, back_img_white.get_rect(center=bottom_center_button))
                preview_tile_depth = map.get_closest_tile_depth(mousepos)
                if preview_tile_depth >= 0:
                    if not player.reached_max_depth() and player.current_depth>-297:
                        # depth_preview = str(-preview_tile_depth)
                        depth_preview = str(player.get_depth() - preview_tile_depth)+" m"
                        write_text(screen, mousepos[0], mousepos[1]-15,depth_preview,20, 'gold')
                    else:
                        write_text(screen, mousepos[0], mousepos[1]-15, '???', 20, 'gold')

            if map_choosing_step==0 and mousepos[1] >= board_Y_level:  # on the board
                player.board.net.draw_planar_figure(screen, mousepos)
                screen.blit(TAB_img_white, TAB_img_white.get_rect(center=bottom_left_button))
                screen.blit(rotate_img_white, rotate_img_white.get_rect(center=bottom_right_button))



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
            clock.tick(fast_fps)

