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
2. 9:1 probability of getting CURSE: BLESS (both are random)

'''

from util import *
import random


def go_to_altar(screen,clock, player):
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
        write_text(screen, width//2, 240, 'Altar', 30, 'gold')

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