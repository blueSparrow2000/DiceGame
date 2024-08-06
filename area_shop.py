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

from area_obtain_skill import *
from area_ruin import *
from skill_book import *


def safe_delete_dict_one_depth_2(dictionary,target_index, target_tile):
    if target_tile in dictionary: # only when exists
        if (dictionary[target_tile][target_index]<=0):
            print("WARNING: possible error in the code (not deleted properly somewhere)\nREASON: Delete entity with amount 0 or less than 0")
        dictionary[target_tile][target_index] -= 1
        if dictionary[target_tile][target_index] <= 0: # delete entry if no longer exist
            del dictionary[target_tile]


shop_text_description_level = 210
shop_text_color = 'black'

def go_to_shop(screen,clock, player):
    global relic_by_rarity_dict
    relic_price_by_rarity = {'common':10, 'rare':20, 'epic':40, 'special':100, 'legendary':200, 'myth':500}
    common_relics = relic_by_rarity_dict['common'] # currently only cell common relics
    random.shuffle(common_relics)
    final_relic_name = common_relics[0][0]
    final_relic_sample = common_relics[0][1]
    relic_obtained = False
    shop_relic_button_loc = [width//2, shop_text_description_level + 550]
    relic_price = relic_price_by_rarity[final_relic_sample.rarity]

    shop_buy_tiles = {'Attack': [3, 10], 'Defence': [3, 10], 'Regen': [3, 15], 'Skill': [3, 20], 'Joker':[3, 40]} # [cell amount until sold out, price of the tile]
    buyable_tiles = list(shop_buy_tiles.keys())

    shop_image_button_tolerance = 25
    shop_button_spacing = 10
    shop_button_x = 50
    shop_button_y = shop_text_description_level + 100
    shop_button_locations = [
        (shop_button_x+ (3*shop_image_button_tolerance + shop_button_spacing + 10) * i, shop_button_y ) for i in range(len(buyable_tiles))]

    shop_skill_button_loc = [width//2, shop_text_description_level + 325]
    skill_list = list(learnable_skill_price_dict.keys())
    skill_to_sell = random.choice(skill_list)
    price_of_skill = learnable_skill_price_dict[skill_to_sell]


    shop_image_dict = dict()
    for tile_name in buyable_tiles:
        shop_image_dict[tile_name] = load_image("tiles/%s" % tile_name)


    game_run = True
    mousepos = (0,0)
    music_Q('Encounter', True)
    while game_run:
        screen.fill('olive')

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
                mousepos= pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(), mousepos))

                if check_inside_button(mousepos, bottom_center_button, button_side_len_half): # confirmed
                    # exit
                    game_run = False
                    break

                # buy immediately a tile
                if player.board.check_tile_exists_in_permanent('Empty'): # only if player has a space to buy a tile
                    for i in range(len(shop_button_locations)):
                        tile_name = buyable_tiles[i]
                        if tile_name in shop_buy_tiles.keys() and check_inside_button(mousepos, shop_button_locations[i], shop_image_button_tolerance): # if there exists remaining tile and clicked
                            price_of_tile = shop_buy_tiles[tile_name][1]
                            if player.pay_gold(price_of_tile): # true, which means the player paid
                                safe_delete_dict_one_depth_2(shop_buy_tiles,0, tile_name) # delete one in the shop
                                player.board.permanently_replace_a_blank_tile_to(tile_name) # add a tile to a player
                            else:
                                pass # notify player that you dont have enough gold! (by blinking gold color e.t.c.)


                # attempt to buy a skill
                if check_inside_button(mousepos, shop_skill_button_loc, shop_image_button_tolerance):
                    if player.can_buy(price_of_skill): #only when player has enough gold - when to pay?
                        bought = obtain_skill(screen, clock, player, skill_to_sell)
                        if bought:
                            player.pay_gold(price_of_skill)

                # buy relic
                if not relic_obtained and check_inside_button(mousepos, shop_relic_button_loc, button_side_len_half): # clicked relic => get relic! (only for one time!)
                    if player.pay_gold(relic_price):  # true, which means the player paid
                        generated_relic = generate_relic_by_class_name(final_relic_name)
                        player.pick_up_relic(generated_relic)
                        relic_obtained = True
                    else:
                        pass # notify player that you dont have enough gold! (by blinking gold color e.t.c.)


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

        # buy tiles
        write_text(screen, width//2, shop_text_description_level+40,
                           "TILES", 20, 'gold')

        for i in range(len(shop_button_locations)):
            tile_name = buyable_tiles[i]
            if tile_name in shop_buy_tiles.keys(): # draw only when corresponding tile exists
                remaining_tiles = shop_buy_tiles[tile_name][0]

                screen.blit(shop_image_dict[tile_name],
                            shop_image_dict[tile_name].get_rect(center=shop_button_locations[i]))
                write_text(screen, shop_button_locations[i][0], shop_button_locations[i][1] + 50,
                           tile_name, 15, shop_text_color)
                price_of_tile = shop_buy_tiles[tile_name][1]
                write_text(screen, shop_button_locations[i][0], shop_button_locations[i][1] + 65,
                           "%d g"%price_of_tile, 15, 'gold')
                write_text(screen, shop_button_locations[i][0], shop_button_locations[i][1] + 80,
                           "%d left"%remaining_tiles, 15, shop_text_color)

            else:
                # draw sold out icon
                screen.blit(sold_out, sold_out.get_rect(center=shop_button_locations[i]))



        # buy a skill (randomly chosen one skill) - but you need to replace a skill for that
        write_text(screen, shop_skill_button_loc[0], shop_skill_button_loc[1] - 50,
                           "SKILLS", 20, 'gold')

        learnable_skills.draw_skill_on_custom_location(screen, skill_to_sell, shop_skill_button_loc)
        write_text(screen, shop_skill_button_loc[0], shop_skill_button_loc[1] + 50,
                           "%s: %d g"%(skill_to_sell, price_of_skill), 17, 'gold')
        write_text(screen, shop_skill_button_loc[0], shop_skill_button_loc[1] + 80,
                           "NOTE: Must be exchanged for previously learned skills", 17, 'white')



        # buy random artifacts
        write_text(screen, shop_relic_button_loc[0], shop_relic_button_loc[1] - 50,
                           "RELICS", 20,'gold')
        if not relic_obtained:  # draw relic info
            final_relic_sample.draw(screen, shop_relic_button_loc, scaled=True)
            write_text(screen, width//2, shop_relic_button_loc[1] + 50, final_relic_sample.name, 20, final_relic_sample.color)
            write_text(screen, width//2, shop_relic_button_loc[1] + 70, final_relic_sample.description(), 17, final_relic_sample.color)
            write_text(screen, width//2, shop_relic_button_loc[1] + 90, "%d g"%relic_price , 17, 'gold')


        # draw effects
        write_text(screen, width//2, area_name_Y_level, 'Shop', 30, 'gold')

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
                pygame.draw.circle(screen, shop_effect_color, position, radi, particle_width_mouse)

        pygame.display.flip()
        clock.tick_busy_loop(game_fps)