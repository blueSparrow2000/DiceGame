'''
tile_to_fix: String of a tile name that will be fixed (only one at a time!)

'''
from util import *

def fix_a_tile(screen,clock, player, tile_to_fix):
    game_run = True
    mousepos = (0,0)

    while game_run:
        screen.fill('oldlace')

        events = pygame.event.get()
        # Event handling
        keys = pygame.key.get_pressed()  # 꾹 누르고 있으면 계속 실행되는 것들 # SHOULD BE CALLED AFTER pygame.event.get()!

        if keys[pygame.K_f]:
            pass
        for event in events:
            if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                game_run = False
                return True, False

            if event.type == pygame.MOUSEMOTION:  # player가 마우스를 따라가도록
                mousepos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                sound_effects['confirm'].play()
                mousepos = pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(), mousepos))

                if check_inside_button(mousepos, bottom_center_button, button_side_len_half): # confirmed
                    # confirm changes
                    player.board.confirm_fixing_tile(tile_to_fix)
                    # exit
                    transition_screen_obj.exit_screen(screen, clock)
                    game_run = False
                    break

                elif check_inside_button(mousepos, bottom_right_button, button_side_len_half):  # back
                    # go to initial stage and do it again
                    player.board.reset_fixing_tile()

                player.board.update_temp_fixed(mousepos, tile_to_fix)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                    game_run = False
                    break
                elif event.key == pygame.K_RETURN:
                    transition_screen_obj.exit_screen(screen, clock)
                    game_run = False
                    break


        if not game_run:
            break

        # draw button
        if check_inside_button(mousepos, bottom_center_button, button_side_len_half):
            write_text(screen, bottom_center_button[0], bottom_center_button[1], "confirm", 15)
        else:
            screen.blit(confirm_img, confirm_img.get_rect(center=bottom_center_button))
        screen.blit(back_img, back_img.get_rect(center = bottom_right_button))


        # Draw player main info
        player.draw_player_info_top(screen, mousepos)

        player.board.draw_fixed_board(screen)

        # draw a tile to fix
        player.board.display_tile(screen, tile_to_fix, [width//2, turn_text_level+70])
        write_text(screen, width//2, turn_text_level+160, "Choose the location to fix a(n) %s tile"%tile_to_fix, 20, 'darkgoldenrod')



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
        clock.tick_busy_loop(slow_fps)