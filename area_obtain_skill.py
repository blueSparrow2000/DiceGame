'''
How to use:
call
obtain_skill(screen, clock, player, spell_name)  # spell_name: string

CAN USE ONE AT A TIME ONLY! (other wise, loop)

'''
from util import *

def obtain_skill(screen,clock, player,skill_to_learn):
    game_run = True
    mousepos = (0,0)
    current_display_text = "Hover mouse on a tile for description"

    while game_run:
        screen.fill('white')

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
                new_text = player.my_turn_lookahead(mousepos)
                if new_text is not None:  # optimization (change only when needed)
                    current_display_text = new_text

            if event.type == pygame.MOUSEBUTTONUP:
                sound_effects['confirm'].play()
                mousepos = pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(), mousepos))

                if check_inside_button(mousepos, bottom_center_button, button_side_len_half): # confirmed
                    # confirm changes
                    player.confirm_skill_replacement()

                    # exit
                    game_run = False
                    break

                elif check_inside_button(mousepos, bottom_right_button, button_side_len_half):  # back
                    # go to initial stage and do it again
                    current_display_text = "Hover mouse on a tile for description"  # reset text
                    player.reset_replacement_of_skill()

                player.replace_current_skill(mousepos, skill_to_learn)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                    game_run = False
                    break
                elif event.key == pygame.K_RETURN:
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
        player.draw_player_info_top(screen)

        player.show_required_tiles(screen)
        player.draw_skill_to_learn(screen, skill_to_learn)
        player.draw_skill_to_swap(screen)

        write_text_description(screen, width // 2 + 30, text_description_level, current_display_text, 15)


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