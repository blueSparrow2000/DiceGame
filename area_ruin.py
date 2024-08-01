'''
60% change of getting random relics
40% change of fighting elite enemy


'''

from area_fight import *
from relic import *

def generate_relic_by_class_name(relic_class_name):
    relic = getattr(__import__("relic"), relic_class_name)()
    return relic



relic_by_rarity_dict =  {'common':[], 'rare':[], 'epic':[], 'special':[], 'legendary':[], 'myth':[]}
for relic_class_name in relic_class_names:
    relic = generate_relic_by_class_name(relic_class_name)
    relic_by_rarity_dict[relic.rarity].append(relic_class_name)
# this sorts relics by its rarity!




def go_to_ruin(screen,clock, player):


    game_run = True
    mousepos = (0,0)
    while game_run:
        # screen.fill('olivedrab')
        screen.fill('darkolivegreen')
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
        write_text(screen, width//2, area_name_Y_level, 'Ruin', 30, 'gold')

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
        clock.tick_busy_loop(game_fps)