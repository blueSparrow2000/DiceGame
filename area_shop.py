'''
What shop can give
> buy tiles
> buy a skill (randomly chosen one skill) - but you need to replace a skill for that
> buy random artifacts

TBU
> erase (= change to empty tile) a tile for some gold? (자리없을듯..)



If there is space in your tile list (empty tiles are more than one)
- can buy each of these tiles with cost of gold
{'Attack':5, 'Defence':5, 'Regen':10, 'Skill':10, 'Joker':20, } # 'Karma' is not buyable
- can by artifacts (random)
- can erase any 'one' tile with cost of gold: 50




'''

from util import *
from area_obtain_skill import *

shop_text_description_level = 210






def go_to_shop(screen,clock, player):
    shop_buy_tiles = {'Attack': 3, 'Defence': 3, 'Regen': 3, 'Skill': 3, 'Joker': 3}
    buyable_tiles = list(shop_buy_tiles.keys())

    shop_image_button_tolerance = 25
    shop_button_spacing = 10
    shop_button_x = 50
    shop_button_y = shop_text_description_level + 100
    shop_bless_button_locations = [
        (shop_button_x, shop_button_y + (4 * shop_image_button_tolerance + shop_button_spacing) * i) for i in range(len(buyable_tiles))]


    shop_image_dict = dict()
    for tile_name in buyable_tiles:
        shop_image_dict[tile_name] = load_image("tiles/%s" % tile_name)


    game_run = True
    music_Q('Encounter', True)
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

            if event.type == pygame.MOUSEBUTTONUP:
                sound_effects['confirm'].play()
                (xp, yp) = pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(), (xp, yp)))
                # do fight logic on player's turn

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                    game_run = False
                    break
                elif event.key == pygame.K_RETURN:
                    game_run = False
                    break


        if not game_run:
            break


        # draw effects
        write_text(screen, width//2, area_name_Y_level, 'Shop', 30, 'gold')

        # Draw player main info
        player.draw_player_info_top(screen)



        # buy tiles
        # shop_text_description_level




        # buy a skill (randomly chosen one skill) - but you need to replace a skill for that







        # buy random artifacts - TBU



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