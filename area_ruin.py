'''
60% change of not fighting an enemy
40% change of fighting elite enemy


20% chance of getting a relic
80% chance of nothing
'''

from area_fight import *
from relic import *

def generate_relic_by_class_name(relic_class_name):
    relic = getattr(__import__("relic"), relic_class_name)()
    return relic


relic_probs = {'common':60, 'rare':20, 'epic':10, 'special':6, 'legendary':3, 'myth':1} # % 기준

relic_by_rarity_dict =  {'common':[], 'rare':[], 'epic':[], 'special':[], 'legendary':[], 'myth':[]} # 각 리스트에는 ['Thorn',Thorn()]이런 형태로 들어있음
for relic_class_name in relic_class_names:
    relic = generate_relic_by_class_name(relic_class_name)
    relic_by_rarity_dict[relic.rarity].append([relic_class_name, relic])
# this sorts relics by its rarity!




def go_to_ruin(screen,clock, player):
    ################## chosing a relic ####################
    chance = random.randrange(1, 100)
    relic_rarity = "common"
    if chance <= relic_probs['myth']:
        relic_rarity = 'myth'
    elif chance <= relic_probs['myth'] + relic_probs['legendary']:
        relic_rarity = 'legendary'
    elif chance <= relic_probs['myth'] + relic_probs['legendary'] + relic_probs['special']:
        relic_rarity = 'special'
    elif chance <= relic_probs['myth'] + relic_probs['legendary'] + relic_probs['special'] + relic_probs['rare']:
        relic_rarity = 'epic'
    elif chance <= relic_probs['myth'] + relic_probs['legendary'] + relic_probs['special'] + relic_probs['rare'] + relic_probs['epic']:
        relic_rarity = 'rare'

    relic_candidates = relic_by_rarity_dict[relic_rarity]
    random.shuffle(relic_candidates)
    final_relic_name = relic_candidates[0][0]
    final_relic_sample = relic_candidates[0][1]

    relic_spawn_chance = random.randrange(1, 100)
    for relic in player.relics:
        relic_spawn_chance -= relic.relic_spawn_chance_increaser()

    relic_obtained = True
    if relic_spawn_chance <= 50:
        relic_obtained = False
    ################## chosing a relic ####################



    relic_Y_level = 350
    relic_location=[width//2,relic_Y_level]



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
                mousepos = pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(), mousepos))
                if check_inside_button(mousepos, bottom_center_button, button_side_len_half): # confirmed
                    # exit
                    game_run = False
                    break
                elif not relic_obtained and check_inside_button(mousepos, relic_location, button_side_len_half): # clicked relic => get relic! (only for one time!)
                    generated_relic = generate_relic_by_class_name(final_relic_name)
                    player.pick_up_relic(generated_relic)
                    relic_obtained = True
                    pass

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

        # draw button
        if check_inside_button(mousepos, bottom_center_button, button_side_len_half):
            write_text(screen, bottom_center_button[0], bottom_center_button[1], "confirm", 15)
        else:
            screen.blit(confirm_img, confirm_img.get_rect(center=bottom_center_button))


        # draw relic info
        if not relic_obtained:
            write_text(screen, width // 2, relic_Y_level - 50, 'Found relic', 30, 'gold')
            final_relic_sample.draw(screen, relic_location, scaled=True)
            write_text(screen, width//2, relic_Y_level + 50, final_relic_sample.name, 20, final_relic_sample.color)
            write_text(screen, width//2, relic_Y_level + 77, final_relic_sample.description(), 17, final_relic_sample.color)
            write_text(screen, width//2, relic_Y_level + 110, 'click to obtain', 15, 'gold')


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