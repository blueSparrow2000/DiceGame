from util import *

def game_win_screen(screen,clock,player):
    player.board.count_all_permanent_tiles()
    ending_roll_Y_level = height
    ending_roll_capacity = - height - 3000
    credit_Y_level = ending_roll_Y_level + 1900
    run_win_screen = True
    music_Q("EndingCredit")
    mousepos = (0,0)
    time.sleep(0.5)
    while run_win_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 윈도우를 닫으면 종료
                run_win_screen = False
                break
            if event.type == pygame.MOUSEMOTION:  # player가 마우스를 따라가도록
                mousepos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                sound_effects['confirm'].play()
                mousepos = pygame.mouse.get_pos()
                # mouse_particle_list.append((pygame.time.get_ticks(), mousepos))
                if ending_roll_Y_level <= ending_roll_capacity and check_inside_button(mousepos, bottom_center_button, button_side_len_half): # confirmed
                    run_win_screen = False
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # esc 키를 누르면 종료
                    run_win_screen = False
                    break
                elif event.key == pygame.K_RETURN:
                    run_win_screen = False
                    break

        screen.fill('dimgray')

        write_text(screen, width // 2, ending_roll_Y_level, 'CLEARED!', 30, 'gold')
        write_text(screen, width // 2, ending_roll_Y_level + 200, 'Thank you for playing', 20, 'gold')

        write_text(screen, width // 2, ending_roll_Y_level + 300, player.my_name, 30, 'gold')

        if  0 <= ending_roll_Y_level + 350 <= height:
            screen.blit(player.image, player.image.get_rect(center=(width // 2, ending_roll_Y_level + 350)))
        write_text(screen, width // 2, ending_roll_Y_level + 450, "Remaining gold", 20, 'gold')
        write_text(screen, width // 2, ending_roll_Y_level + 500, "%d"%player.golds, 17, 'gold')
        write_text(screen, width // 2, ending_roll_Y_level + 550, "Enemy killed", 20, 'gold')
        write_text(screen, width // 2, ending_roll_Y_level + 600, "%d"%player.killed_enemies, 17, 'gold')
        write_text(screen, width // 2, ending_roll_Y_level + 650, "Obtained relics", 20, 'gold')
        write_text(screen, width // 2, ending_roll_Y_level + 700, "%d"%len(player.relics), 17, 'gold')
        write_text(screen, width // 2, ending_roll_Y_level + 750, "Number of tiles", 20, 'gold')
        write_text(screen, width // 2, ending_roll_Y_level + 800, "%d"%player.board.number_of_permanent_tiles, 17, 'gold')


        write_text(screen, width // 2, credit_Y_level, 'Credits', 30, 'gold')
        write_text(screen, width // 2, credit_Y_level + 200, 'Producer / Creative director', 20, 'gold')
        write_text(screen, width // 2, credit_Y_level + 250, 'SSH', 17, 'gold')
        write_text(screen, width // 2, credit_Y_level + 350, 'Game Design', 20, 'gold')
        write_text(screen, width // 2, credit_Y_level + 400, 'SSH', 17, 'gold')
        write_text(screen, width // 2, credit_Y_level + 500, 'Art Design', 20, 'gold')
        write_text(screen, width // 2, credit_Y_level + 550, 'SSH', 17, 'gold')
        write_text(screen, width // 2, credit_Y_level + 650, 'Programmer', 20, 'gold')
        write_text(screen, width // 2, credit_Y_level + 700, 'SSH', 17, 'gold')
        write_text(screen, width // 2, credit_Y_level + 1000, 'Special thanks', 30, 'gold')
        write_text(screen, width // 2, credit_Y_level + 1100, 'Beta tester', 20, 'gold')
        write_text(screen, width // 2, credit_Y_level + 1150, 'Seyeong Choi', 17, 'gold')


        if ending_roll_Y_level > ending_roll_capacity:
            ending_roll_Y_level -= 1
            credit_Y_level = ending_roll_Y_level + 1900

        if ending_roll_Y_level <= ending_roll_capacity:
            # draw button
            if check_inside_button(mousepos, bottom_center_button, button_side_len_half):
                write_text(screen, bottom_center_button[0], bottom_center_button[1], "back to main menu", 15)
            else:
                screen.blit(confirm_img, confirm_img.get_rect(center=bottom_center_button))

        pygame.display.flip()
        clock.tick(60)