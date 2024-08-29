'''
Rename the function go_to_area

'''
from util import *
from area_ruin import *

def go_to_blackmarket(screen,clock, player):
    global relic_by_rarity_dict, relic_price_by_rarity
    high_tier_relics = relic_by_rarity_dict['legendary'] + relic_by_rarity_dict['special']

    music_Q('Anxiety', True)
    game_run = True
    mousepos = (0,0)
    market_text_level = turn_text_level+20

    while game_run:
        screen.fill(dark_brown)

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
                mousepos = pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(), mousepos))
                if check_inside_button(mousepos, bottom_center_button, button_side_len_half): # confirmed
                    sound_effects['confirm'].play()
                    # exit
                    game_run = False
                    break

                discarded, discarded_relic = player.discard_relic(mousepos)
                if discarded:
                    sell_price = relic_price_by_rarity[discarded_relic.rarity] // 2
                    player.get_gold(sell_price)
                    sound_effects['jackpot'].play()


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


        # draw sell
        write_text(screen, width//2, market_text_level, 'Blackmarket', 30, 'white')

        write_text(screen, width//2, market_text_level + 100, 'Click a relic to sell', 20, 'white')

        player.show_estimated_relic_price(screen, mousepos, (width//2, market_text_level + 150))

        # buy random high tier relic with double price







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

        pygame.display.flip()
        clock.tick_busy_loop(slow_fps)