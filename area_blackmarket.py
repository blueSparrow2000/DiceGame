'''
Rename the function go_to_area

'''
from util import *
from area_ruin import *

def go_to_blackmarket(screen,clock, player):
    global relic_by_rarity_dict, relic_price_by_rarity
    high_tier_relics = relic_by_rarity_dict['legendary'] + relic_by_rarity_dict['special']
    random.shuffle(high_tier_relics)
    relic_samples = 3
    final_relic_name = [high_tier_relics[i][0] for i in range(relic_samples)]
    final_relic_sample = [high_tier_relics[i][1] for i in range(relic_samples)]
    relic_obtained = [False for i in range(relic_samples)]
    relic_base_Y_location = shop_text_description_level + 250
    shop_relic_button_loc = [[width//2, relic_base_Y_location + i*150] for i in range(relic_samples)]
    relic_price = [relic_price_by_rarity[final_relic_sample[i].rarity] for i in range(relic_samples)]


    music_Q('Anxiety', True)
    game_run = True
    mousepos = (0,0)
    market_text_level = turn_text_level+10

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
                    transition_screen_obj.exit_screen(screen, clock)
                    game_run = False
                    break

                discarded, discarded_relic = player.discard_relic(mousepos)
                if discarded:
                    sell_price = relic_price_by_rarity[discarded_relic.rarity] // 5
                    player.get_gold(sell_price)
                    sound_effects['jackpot'].play()

                # buy relic
                for i in range(relic_samples):
                    if (not relic_obtained[i]) and player.have_space_for_relic():
                        if check_inside_button(mousepos,shop_relic_button_loc[i],button_side_len_half):  # clicked relic => get relic! (only for one time!)
                            if player.pay_gold(relic_price[i]):  # true, which means the player paid
                                generated_relic = generate_relic_by_class_name(final_relic_name[i])
                                player.pick_up_relic(generated_relic)
                                relic_obtained[i] = True
                                sound_effects['register'].play()
                            else:
                                pass  # notify player that you dont have enough gold! (by blinking gold color e.t.c.)



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


        # draw sell
        write_text(screen, width//2, market_text_level, 'Blackmarket', 30, 'white')

        write_text(screen, width//2, market_text_level + 60, 'Click a relic to sell', 20, 'white')

        player.show_estimated_relic_price(screen, mousepos, (width//2, market_text_level + 100))

        # buy random high tier relic with double price
        write_text(screen, width//2, relic_base_Y_location - 50, 'MERCHANDISE', 20, 'white')
        for i in range(relic_samples):
            if not relic_obtained[i]:  # draw relic info
                final_relic_sample[i].draw(screen, shop_relic_button_loc[i], scaled=True)
                write_text(screen, width//2, shop_relic_button_loc[i][1] + 50, final_relic_sample[i].name, 20, final_relic_sample[i].color)
                write_text(screen, width//2, shop_relic_button_loc[i][1] + 70, final_relic_sample[i].description(), 17, final_relic_sample[i].color)
                write_text(screen, width//2, shop_relic_button_loc[i][1] + 90, "%d g"%relic_price[i] , 17, 'gold')



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
        clock.tick_busy_loop(slow_fps)