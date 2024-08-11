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


relic_probs = {'common':30, 'rare':25, 'epic':20, 'special':15, 'legendary':8, 'myth':2} # % 기준

relic_by_rarity_dict =  {'common':[], 'rare':[], 'epic':[], 'special':[], 'legendary':[], 'myth':[]} # 각 리스트에는 ['Thorn',Thorn()]이런 형태로 들어있음
for relic_class_name in relic_class_names:
    relic = generate_relic_by_class_name(relic_class_name)
    relic_by_rarity_dict[relic.rarity].append([relic_class_name, relic])
# this sorts relics by its rarity!



def determine_rarity():
    chance = random.randint(1, 100)
    rarity = "common"
    if chance <= relic_probs['myth']:
        rarity = 'myth'
    elif chance <= relic_probs['myth'] + relic_probs['legendary']:
        rarity = 'legendary'
    elif chance <= relic_probs['myth'] + relic_probs['legendary'] + relic_probs['special']:
        rarity = 'special'
    elif chance <= relic_probs['myth'] + relic_probs['legendary'] + relic_probs['special'] + relic_probs['rare']:
        rarity = 'epic'
    elif chance <= relic_probs['myth'] + relic_probs['legendary'] + relic_probs['special'] + relic_probs['rare'] + relic_probs['epic']:
        rarity = 'rare'

    return rarity


def go_to_ruin(screen,clock, player, fought): # if player fought with an enemy, 100% change to obtain relic (ruin enemies are like guardians of the relic, so if there is a relic, they would guard)
    ruin_artifact_number_list = [1,2,3]
    ruin_artifact_number_probs = [0.1, 0.4, 0.5]
    ruin_number_choice = simple_choice_maker(ruin_artifact_number_list, ruin_artifact_number_probs, 1)
    ruin_seed = int(ruin_number_choice[0])

    for relic in player.relics:
        if 1 <= relic.fix_artifact_number() <= 3 and ruin_seed < relic.fix_artifact_number(): # 가장 많은 걸 따른다
            ruin_seed = relic.fix_artifact_number()

    relic_gap = 100 # scaled size
    relic_Y_level = 350
    relic_locations = [[width // 2 - (ruin_seed-1)*relic_gap//2 + i*relic_gap, relic_Y_level] for i in range(ruin_seed)]

    ################## chosing a relic ####################
    relic_spawn_chance = random.randint(1, 100)
    for relic in player.relics:
        relic_spawn_chance -= relic.relic_spawn_chance_increaser()

    relic_obtained = True
    if relic_spawn_chance <= 90: # (if no fight) 90% chance to get relic
        relic_obtained = False
    if fought: # after fight, always relic exists
        relic_obtained = False
    for relic in player.relics: # fixing artifact number always makes relic exist
        if 1 <= relic.fix_artifact_number() <= 3:
            relic_obtained = False


    final_relic_names = []
    final_relic_samples = []

    for i in range(ruin_seed):
        final_relic_name = ""
        final_relic_sample = ""

        relic_rarity = determine_rarity()
        relic_candidates = relic_by_rarity_dict[relic_rarity]
        if not len(relic_candidates)==0:
            random.shuffle(relic_candidates)
            final_relic_name = relic_candidates[0][0]
            final_relic_sample = relic_candidates[0][1]

        final_relic_names.append(final_relic_name)
        final_relic_samples.append(final_relic_sample)


    if len(final_relic_names)==0: # no relic left in each rarity
        relic_obtained = True # relic is gone!


    ################## chosing a relic ####################

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
                elif not relic_obtained: # clicked relic => get relic! (only for one time!)
                    if player.have_space_for_relic():  # bag is not full
                        for i in range(ruin_seed):
                            if check_inside_button(mousepos, relic_locations[i], button_side_len_half):
                                generated_relic = generate_relic_by_class_name(final_relic_names[i])
                                player.pick_up_relic(generated_relic)
                                relic_obtained = True

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

        for i in range(ruin_seed):
            screen.blit(scaled_pedestal_img , scaled_pedestal_img .get_rect(center=(relic_locations[i][0], relic_locations[i][1] + 70)))

        # draw relic info
        if not relic_obtained:
            write_text(screen, width // 2, relic_Y_level - 100, 'Found relic', 30, 'gold')
            if player.have_space_for_relic():  # bag is not full
                write_text(screen, width//2, relic_Y_level -60, 'click to obtain', 18, 'gold')
            else:
                write_text(screen, width // 2, relic_Y_level - 60, 'your bag is full!', 18, 'red')

            # relic drawing
            for i in range(ruin_seed):
                # screen.blit(scaled_pedestal_img , scaled_pedestal_img .get_rect(center=(relic_locations[i][0], relic_locations[i][1] + 70)))

                final_relic_sample = final_relic_samples[i]
                final_relic_sample.draw(screen, relic_locations[i], scaled=True)

                final_relic_sample.show_ruin_description(screen, relic_locations[i], [width // 2, relic_Y_level + 180], mousepos)



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