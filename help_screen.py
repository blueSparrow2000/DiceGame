'''
Basic rules

Map progression
- you can progress the map by building a bridge using only one 'click' of planar figure

1) Fight tile
- at a battle, up to 3 enemies can spawn
- player always start first, then enemy does its behavior

- your planar figure must not leave the board, and must not contain used/unusable tiles
- three basic moves (attack, defense, regen) increase in proportion to the power of the number of each tiles drawn
- defence points decays after one turn (Until it comes back to the player's turn)
- there are required tiles for each skill you use

- tile abbreviations (줄임말)
A: Attack
S: Skill
R: Regen
D: Defence
J: Joker
K: Karma

2) Ruin tile
- ruin give you 0~3 choices of relics / note that you could come across a battle before reaching ruin
- you cannot have more than 24 relics, so think carefully to take it or not

3) Altar tile
- altar gives you a curse (with prob 80%) and you can choose one blessing among three

4) Campfire tile (More feature is going to be added)
- campfire will heal 50 hp

5) Shop tile
- you can buy 1 relic / 1 skill / and 3 of each tiles in the shop

Bosses
- there are currently three bosses on depth -100, -200, -300 and one ruin boss at -150

Buffs/Debuffs
- All buffs like poison, toxin, strength, weakness, decay, vulnerability etc. damage does not stack, only the duration is increased

'''

'''
Rename the function go_to_area

'''
from util import *

def update_help_idx(i, deviance):
    return (i+deviance)%5

def help_screen(screen,clock):
    global map_tile_image_dict
    # ['void', 'base', 'campfire', 'fight', 'ruin', 'shop', 'altar', 'bridge', 'highlight', 'boss_fight']

    help_page_idx = 0 # mod 5

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
        draw_toggle_button(screen, mousepos, back_img, back_img_gold, bottom_center_button, button_side_len_half)
        draw_toggle_button(screen, mousepos, right_button, right_button_gold, bottom_right_button, button_side_len_half)
        draw_toggle_button(screen, mousepos, left_button, left_button_gold,bottom_left_button, button_side_len_half)


        # draw effects
        write_text(screen, width//2, 100, 'HELP', 30, 'gold')

        # Draw player main info


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




























