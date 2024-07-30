'''
Take random curse(cursed tile etc)
and choose between three random relics


What Alter can give
(+) BLESS
Decrease board reset frequency by 1
Curse or Treat > Board get shuffled every turn end (even fixed tiles are shuffled)
Shrink the board side size by one

Give 1 random fixable tile  (among Attack, Defence, Regen, Skill)
Remove the limitation of placing planar figure outside the board (now net can have less than 6 current tiles including empty ones => 'out_of_board_protection = False' on collect_tile function)
change all tile_type_1 to tile_type_2 (e.g. all attack tiles become defence tiles) where each tiles are one of Attack, Defence, Regen, Skill


(-) CURSE
Delete one skill slot forever
Halve maximum health
Make irregular-shaped board (diag or circle etc.)


options
1. get a CURSE(randomly bad) and choose BLESS among random 3
2. (X) 9:1 probability of getting CURSE: BLESS (both are random)

'''

from util import *
from area_fix_a_tile import *
import copy


altar_text_description_level = 210
altar_bless_reference = ['decrease board reset frequency by one','board get shuffled every turn','shrink the board size by one',
               'obtain one fixable tile','planar figure can escape the board', 'change all tile of type_1 to type_2']
altar_curse_reference = ['delete one skill slot forever','halve maximum health','irregular shaped board'] #['delete one skill slot forever','halve maximum health','irregular shaped board']
altar_bless = copy.deepcopy(altar_bless_reference)
altar_curse = copy.deepcopy(altar_curse_reference)

altar_curse_bless_names = altar_bless_reference + altar_curse_reference
altar_images = dict()
for name in altar_curse_bless_names:
    altar_images[name] = load_image("altar/%s"%name)

def exit_altar():
    pass

def reset_altar():
    global altar_bless,altar_curse
    altar_bless = copy.deepcopy(altar_bless_reference)
    altar_curse = copy.deepcopy(altar_curse_reference)

def go_to_altar(screen,clock, player):
    global altar_bless,altar_curse
    bless_choice_num = min(3, len(altar_bless))
    random.shuffle(altar_bless)
    bless_list = copy.deepcopy(altar_bless[:bless_choice_num])
    curse = altar_curse[random.randint(0,len(altar_curse)-1)]

    # apply curse here!
    if curse == 'delete one skill slot forever':
        player.remove_one_skill_from_highest_index()
        altar_curse.remove(curse)
    elif curse == 'halve maximum health':
        player.set_max_health(player.max_health//2)
    elif curse == 'irregular shaped board':
        player.board.set_irregular_shape('stripe')
        altar_curse.remove(curse) # get this only once!


    altar_image_button_tolerance = 25
    altar_button_spacing = 10
    altar_button_x = 50
    altar_button_y = 560
    altar_bless_button_locations = [
        (altar_button_x, altar_button_y + (4 * altar_image_button_tolerance + altar_button_spacing) * i) for i in range(len(bless_list))]


    game_run = True
    music_Q('tense', True)
    while game_run:
        screen.fill('white')

        events = pygame.event.get()
        # Event handling
        keys = pygame.key.get_pressed()  # 꾹 누르고 있으면 계속 실행되는 것들 # SHOULD BE CALLED AFTER pygame.event.get()!

        if keys[pygame.K_f]:
            pass
        for event in events:
            if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                pass
                # game_run = False
                # return True, False

            if event.type == pygame.MOUSEMOTION:  # player가 마우스를 따라가도록
                mousepos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                sound_effects['confirm'].play()
                mousepos = pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(),mousepos ))

                for i in range(len(altar_bless_button_locations)): # if clicked button, immediately effect!
                    if check_inside_button(mousepos, altar_bless_button_locations[i], altar_image_button_tolerance):
                        bless_name = bless_list[i]
                        if bless_name == 'decrease board reset frequency by one':
                            player.board.change_board_reset_frequency_by(1)
                        elif bless_name == 'board get shuffled every turn':
                            player.board.set_board_shuffle(True)
                            altar_bless.remove(bless_name) # only once
                        elif bless_name == 'shrink the board size by one':
                            player.board.permanently_shrink_the_board_by_one()
                        elif bless_name == 'obtain one fixable tile':
                            altar_fixable_tiles = ['Attack', 'Defence','Regen', 'Skill']
                            tile_to_fix = random.choice(altar_fixable_tiles)
                            fix_a_tile(screen,clock, player, tile_to_fix)
                        elif bless_name == 'planar figure can escape the board':
                            player.board.set_out_of_board_protection(False)
                            altar_bless.remove(bless_name) # only once
                        elif bless_name == 'change all tile of type_1 to type_2':
                            pass
                        elif bless_name == '':
                            pass

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


        # draw effects
        write_text(screen, width//2, 160, 'Altar', 30, 'gold')

        write_text(screen,width//2 , altar_text_description_level, 'You got a curse', 30, 'maroon')
        screen.blit(altar_images[curse], altar_images[curse].get_rect(center=[width//2,altar_text_description_level+75 ]))
        write_text(screen,width//2 , altar_text_description_level+150, curse, 15, 'maroon')


        write_text(screen,width//2 , altar_text_description_level + 300, 'Choose one of the bless and confirm', 15)


        for i in range(len(altar_bless_button_locations)):
            bless_name = bless_list[i]
            screen.blit(altar_images[bless_name], altar_images[ bless_name].get_rect(center=altar_bless_button_locations[i]))
            write_text(screen, altar_bless_button_locations[i][0]+200, altar_bless_button_locations[i][1], bless_name, 15, 'darkgoldenrod')

        # Draw player main info
        player.draw_player_info_top(screen)


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