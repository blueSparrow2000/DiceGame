'''
Rename the function go_to_area

'''
from util import *

def falling_coeff(target_y, cur_y, coeff):
    fall_amount = (target_y - cur_y)//(10*coeff)

    return fall_amount




def title_screen(screen,clock):
    ########## particle ############
    particle_list = []
    ########## particle ############
    screen_y = 0
    first_drop = True
    game_run = True
    mousepos = (0,0)

    while game_run:
        screen.fill(terracotta)

        events = pygame.event.get()
        # Event handling
        keys = pygame.key.get_pressed()  # 꾹 누르고 있으면 계속 실행되는 것들 # SHOULD BE CALLED AFTER pygame.event.get()!

        if keys[pygame.K_f]:
            pass
        for event in events:
            if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                game_run = False
                return True, False

            if event.type == pygame.MOUSEMOTION:
                mousepos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                sound_effects['confirm'].play()
                mousepos = pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(), mousepos))
                if check_inside_button(mousepos, bottom_center_button, button_side_len_half): # confirmed
                    # exit
                    game_run = False
                    break


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
            write_text(screen, bottom_center_button[0], bottom_center_button[1], "PLAY", 40)
        else:
            screen.blit(confirm_img, confirm_img.get_rect(center=bottom_center_button))

        fall_delta = falling_coeff(240,screen_y, 2.5) # 240
        screen_y += fall_delta

        if first_drop and fall_delta<0.5:
            first_drop = False
            ########## particle ############
            particle_list.append((pygame.time.get_ticks(), (width//2, 240), 45, 5, 'gold'))
            ########## particle ############


        # draw effects
        write_text(screen, width//2, screen_y, 'Diagramiz', 30, 'gold')
        write_text(screen, width // 2, screen_y + 40, 'beta 1.3.4', 15, 'gold')
        # write_text(screen, width//2, screen_y+40, 'since 2024.07.21', 15, 'gold')


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

        ########## particle ############
        if particle_list:  # if not empty
            current_run_time = pygame.time.get_ticks()
            for particle in particle_list:
                mouse_click_time = particle[0]
                position = particle[1]
                particle_radius = particle[2]
                particle_width = particle[3]
                particle_color = particle[4]
                delta = (current_run_time - (mouse_click_time)) / 1000
                if delta >= water_draw_time_mouse:
                    particle_list.remove(particle)
                factor = delta / water_draw_time_mouse
                radi = calc_drop_radius(factor, particle_radius)
                pygame.draw.circle(screen, particle_color, position, radi, particle_width)
        ########## particle ############

        pygame.display.flip()
        clock.tick_busy_loop(slow_fps)