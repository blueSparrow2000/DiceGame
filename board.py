'''
Board를 변경하는 범위엔 3가지가 있다
1. 영구히 보드의 타일 분포를 변경시키는 것 (전투 종료 후에도 영구 지속)
self.permanent_board_dict 영구적인 영향
=> permanent

2. 해당 전투에서 지속적으로 타일 분포를 변경시키는것 (전투 종료시 리셋)
self.temporary_board_dict 이번 전투 중에만 유지되는 타일분포
=> temporary
reset every time game starts (new_game 함수)

3. 보드가 리셋되기 전까지 현재의 보드 판의 타일분포를 변경시키는것 (전투 중에 보드 리셋시 리셋되는)
self.board를 변경하면 됨
=> board
reset every time turn ends (reset 함수)

'''


import random
import copy
from util import *
import math

planar_figures = []

# total 11 but i am lazy
T_shape = [[1,1,1],
           [0,1,0],
           [0,1,0],
           [0,1,0]]

Cross_shape = [[0,1,0],
               [1,1,1],
               [0,1,0],
               [0,1,0]]

Worm_shape =  [[1,1,0],
               [0,1,0],
               [0,1,0],
               [0,1,1]]

Worm_2_shape =[[1,1,0],
               [0,1,1],
               [0,1,0],
               [0,1,0]]

Worm_3_shape =[[1,1,0],
               [0,1,0],
               [0,1,1],
               [0,1,0]]

Cacti_shape = [[0,1,0],
               [1,1,0],
               [0,1,1],
               [0,1,0]]

Diag_shape =  [[1,0,0],
               [1,1,0],
               [0,1,1],
               [0,0,1]]

Diag_2_shape =[[1,0,0],
               [1,1,0],
               [0,1,0],
               [0,1,1]]

Chair_shape = [[0,1,0],
               [0,1,0],
               [1,1,1],
               [1,0,0]]

Chair_2_shape=[[0,0,1],
               [0,1,1],
               [1,1,0],
               [0,1,0]]

# Thunder_shape=[[1,0,0], # out of range
#                [1,0,0],
#                [1,1,0],
#                [0,1,0],
#                [0,1,0]]
planar_figures.extend([T_shape, Cross_shape, Worm_shape, Worm_2_shape, Worm_3_shape, Cacti_shape, Diag_shape, Diag_2_shape, Chair_shape, Chair_2_shape])
'''
BOSS FIGHT PARAMETERS

When reseting the board, it gets 'fragmented'
reset(self, enforced=False, irregular_reset_shape = 'fragmented')

Out of board protection becomes false! => more free space to use
collect_tiles(self,mousepos, out_of_board_protection = False)
'''
class Board():
    def __init__(self,tiles_dict,planar_figure_idx):
        global tile_names,planar_figures,sound_effects,board_Y_level
        self.board_side_length = 8
        self.board = [] # 이번 보드에만 영향을 주는건 이것만 바꿈 # has string of tile names
        self.temp_board = []
        self.permanent_board_dict = copy.deepcopy(tiles_dict) # 영구적인 영향을 주는 거면 이거도 바꿈
        tile_count = 0
        for k,v in self.permanent_board_dict.items():
            tile_count+=v
        self.permanent_board_dict['Empty'] = self.board_side_length**2 - tile_count
        self.temporary_board_dict = copy.deepcopy(self.permanent_board_dict) # 이번 전투에만 영향을 주는거면 이거도 바꿈
        self.cube_figure = load_image('tiles/cube')

        self.image_dict = dict()
        for tile_name in tile_names:
            self.image_dict[tile_name] = (load_image("tiles/%s" % tile_name))

        self.translation_dict = {}
        self.side_length =  self.image_dict['Attack'].get_height()
        self.board_Y_level = board_Y_level + self.side_length//2
        self.board_Y_selectable = board_Y_level - self.side_length
        self.board_X = width//2 - self.side_length*4 + self.side_length//2
        #self.rect = pygame.Rect((self.board_X,self.board_Y_level), (self.side_length*8,self.side_length*8))

        self.figure_index = 0 # 0 for primary, 1 for secondary
        self.planar_figures = copy.deepcopy(planar_figures)
        self.planar_figure_idx = copy.deepcopy(planar_figure_idx) # absolute variants of planar figures
        self.init_planar_figures = [copy.deepcopy(planar_figures[self.planar_figure_idx[0]]),copy.deepcopy(planar_figures[self.planar_figure_idx[1]])]
        self.my_planar_figures = [planar_figures[self.planar_figure_idx[0]],planar_figures[self.planar_figure_idx[1]]]
        self.current_planar_figure = self.my_planar_figures[self.figure_index]
        self.planar_figure_col = len(self.current_planar_figure)
        self.planar_figure_row = len(self.current_planar_figure[0])
        self.planar_figure_center = [1,1] # col, row

        self.board_reset_turn = 6
        self.current_turn = 0
        self.board_reset_icon = load_image("icons/reset")


    ################################################## permenant changes ##################################################

    '''
    You can change board reset frequency by calling the below function. Initially it is 6 turns.
    '''
    def change_board_reset_frequency_to(self, reset_turns):
        self.board_reset_turn = reset_turns

    '''
    Re calculate # of empty tiles
    '''
    def reset_permanent_board_dict(self):
        tile_count = 0
        for k,v in self.permanent_board_dict.items():
            if k != 'Empty': # count non-empty tiles only
                tile_count+=v
        self.permanent_board_dict['Empty'] = self.board_side_length**2 - tile_count # reset empty tiles

    '''
    Are there more than given amount of tiles?
    '''
    def check_number_of_given_tiles_is_geq_amount_in_permanent(self, given_tile, amount=1):
        return given_tile in self.permanent_board_dict and self.permanent_board_dict[given_tile] >= amount # if such tile exists and is having more than one
    '''
    Is there exactly given amount of tiles?
    '''
    def check_number_of_given_tiles_in_permanent(self, given_tile, amount=1):
        return given_tile in self.permanent_board_dict and self.permanent_board_dict[given_tile] == amount # if such tile exists and is having more than one

    '''
    Is there at least one tile?
    '''
    def check_tile_exists_in_permanent(self, given_tile):
        return given_tile in self.permanent_board_dict and self.permanent_board_dict[given_tile] > 0 # if such tile exists and is having more than one


    '''
    Use this function to add a tile permanently
    '''
    def permanently_replace_a_blank_tile_to(self, target_tile):
        if not self.check_tile_exists_in_permanent('Empty'):
            print("My tiles are full!!! Can not add more!")
            return
        safe_tile_add_one(self.permanent_board_dict, target_tile)
        self.reset_permanent_board_dict() # recalculate the empty tiles

    '''
    Use this function to delete a tile permanently
    The deleted tile becomes empty tile
    '''
    def permanently_delete_a_tile(self, target_tile):
        safe_delete_dict(self.permanent_board_dict, target_tile)
        self.reset_permanent_board_dict() # recalculate the empty tiles

    ''' Altar
    when shrinking board to 7 by 7
    check whether there are at least 14 blank tiles
    '''
    def permanently_shrink_the_board_by_one(self):
        if not self.check_number_of_given_tiles_is_geq_amount_in_permanent('Empty', (self.board_side_length)*2 - 1):
            print("Not enough space to shrink the tiles")
            return False

        self.board_side_length -= 1
        self.shrink_recalculate_board_offsets()
        self.reset_permanent_board_dict()


    def shrink_recalculate_board_offsets(self):
        self.board_X = width//2 - (self.side_length//2) * self.board_side_length + self.side_length//2 # centerize

    ################################################## permenant changes ##################################################


    ################################################## planar figures ##########################################################

    def refresh_planar_figure(self):
        self.planar_figure_col = len(self.current_planar_figure)
        self.planar_figure_row = len(self.current_planar_figure[0])
        # change the center pos accordingly
        #self.planar_figure_center = [1,1]

    def init_turn(self): # initialize planar figure at every turn starts
        self.figure_index = 0
        self.my_planar_figures = [copy.deepcopy(planar_figures[self.planar_figure_idx[0]]), copy.deepcopy(planar_figures[self.planar_figure_idx[1]])]
        self.current_planar_figure = self.my_planar_figures[self.figure_index]
        self.refresh_planar_figure()

    def change_planar_figure(self, confused):
        if confused:
            return
        self.figure_index = (self.figure_index+1)%2
        self.current_planar_figure = self.my_planar_figures[self.figure_index]
        self.refresh_planar_figure()

    def draw_planar_figure(self,screen,mousepos):
        if mousepos[1] < self.board_Y_selectable:  # not on the board
            return False

        for c in range(self.planar_figure_col):
            for r in range(self.planar_figure_row):
                if (self.current_planar_figure[c][r])==1: # draw only when exists
                    location = (mousepos[0] + (r - self.planar_figure_center[1])*self.side_length, mousepos[1] + (c - self.planar_figure_center[0])*self.side_length)
                    screen.blit(self.cube_figure, self.cube_figure.get_rect(center=location))


    def get_center_locations_planar_figure(self, mousepos):
        center_locations = []
        for c in range(self.planar_figure_col):
            for r in range(self.planar_figure_row):
                if (self.current_planar_figure[c][r])==1: # draw only when exists
                    location = (mousepos[0] + (r - self.planar_figure_center[1])*self.side_length, mousepos[1] + (c - self.planar_figure_center[0])*self.side_length)
                    center_locations.append(location)
        return center_locations

    def rotate_once(self):
        self.current_planar_figure = list(zip(*self.current_planar_figure[::-1]))
        self.refresh_planar_figure()

    ################################################## planar figures ##########################################################


    '''
    reset board & temporary tile dict when the game starts
    '''
    def new_game(self):
        self.current_turn = 0
        self.temporary_board_dict = copy.deepcopy(self.permanent_board_dict)
        self.reset(True)

    def confirm_using_tile(self):
        self.board = self.temp_board

    def reset(self, enforced=False, irregular_reset_shape = None):  # reset the board (each 6 turn)
        '''
        This function only resets content of current board

        Location is determined in the boardify function!

        board_temp = list of tile names (no location information when creating)
        '''

        self.init_turn() # initialize planar figures

        if (enforced or self.current_turn % self.board_reset_turn == 0):  # every 6th turn, reset the board
            ############### RESET BOARD ###############
            self.clear_board()  # empty the board only when reset
            board_temp = []
            for k, v in self.temporary_board_dict.items(): # fetch board content to an array
                tile = k
                for i in range(v):
                    board_temp.append(tile)
            random.shuffle(board_temp)  # randomize

            if irregular_reset_shape:
                self.irregular_shapify(board_temp, irregular_reset_shape)
            else:
                self.boardify(board_temp) # set up a board
            ############### RESET BOARD ###############
            self.current_turn = 0 # reset turn

        self.current_turn += 1

    def clear_board(self):
        self.board = [] # initialize board


    ############################################################################################################ BOARD INDIRECTION 수정은 여기부터! ############################################################################################################
    def convert_all_tiles_on_board(self,target_tile, convert_tile): # convert target tile into convert tile
        # loop through current board and change all 'tile_name' tiles into 'Used' tiles
        for i in range(len(self.board)):
            board_tile_name = self.board[i][1]
            if board_tile_name == target_tile:
                self.temp_board[i][1] = convert_tile  # temp 를 바꿔야 변경사항이 적용됨 confirm에서!


    def consume_all_tiles_on_board(self, target_tile): # consume all tiles and return how many are (actually) consumed
        how_many_consumed = 0
        for i in range(len(self.board)):
            current_tile_name = self.board[i][1]
            if current_tile_name == target_tile:
                self.temp_board[i][1] = 'Used'  # temp 를 바꿔야 변경사항이 적용됨 confirm에서!
                how_many_consumed += 1
        return how_many_consumed

    def count_all_tiles_on_board(self, target_tile): # for lookahead
        how_many = 0
        for i in range(len(self.board)):
            current_tile_name = self.board[i][1]
            if current_tile_name == target_tile:
                how_many += 1
        return how_many


    def irregular_shapify(self, board_temp, irregular_reset_shape = 'stripe'):
        # calculate irregular locations!
        if irregular_reset_shape=='stripe':
            for i in range(self.board_side_length):
                for j in range(self.board_side_length):
                    board_tile = [[self.board_X + j * self.side_length, self.board_Y_level + self.side_length * i * 1.1], board_temp[i*self.board_side_length + j] ]
                    self.board.append(board_tile)

        elif irregular_reset_shape=='fragmented':
            spiral_coeff = 1
            distance_coeff = 5
            amount = len(board_temp)
            FRAGMENTED_offsets = []
            for i in range(amount): #-self.board_side_length//2 + (self.board_side_length+1)%2, self.board_side_length//2
                    theta = spiral_coeff * i
                    deviance = [ round(distance_coeff * theta*math.cos(theta) ), round(distance_coeff *  theta* math.sin(theta) )]
                    purturvation = [0,0]#[ random.randint(-10,10), random.randint(-10,10)]
                    FRAGMENTED_offsets.append([deviance[0] + purturvation[0],deviance[1] + purturvation[1] ])
            for i in range(len(FRAGMENTED_offsets)):
                fragment = FRAGMENTED_offsets[i]
                board_tile = [[width//2 + fragment[0], (height//4)*3 + fragment[1]], board_temp[i] ]
                self.board.append(board_tile)
        elif irregular_reset_shape=='diamond':
            pass
        elif irregular_reset_shape == 'circular':
            pass

    def boardify(self,board_temp): # change images where board is changed to used
        '''
        boardifying with grid shape centered middle vertical line

        IMPORTANT: assigns location and tile information here!!!!!
        '''
        for i in range(self.board_side_length):
            for j in range(self.board_side_length):
                board_tile = [[self.board_X + j * self.side_length, self.board_Y_level + self.side_length * i], board_temp[i*self.board_side_length + j] ]
                self.board.append(board_tile)

    def draw(self,screen, step, mousepos):
        global write_text
        if step==0:
            ### draw board
            for i in range(len(self.board)):
                board_tile_location = self.board[i][0]
                board_tile_name = self.board[i][1]
                tile_img = self.image_dict[board_tile_name]
                screen.blit(tile_img,tile_img.get_rect(center=board_tile_location))
            ### draw board

            turns_remaining_until_board_reset = self.board_reset_turn - self.current_turn + 1
            # draw reset counter
            if turns_remaining_until_board_reset==1:
                write_text(screen, width-40 , self.board_Y_level - self.side_length, "%d"%(turns_remaining_until_board_reset), 20, color = 'red')
            else:
                write_text(screen, width-40, self.board_Y_level - self.side_length, "%d" % (turns_remaining_until_board_reset), 20)

            screen.blit(self.board_reset_icon,self.board_reset_icon.get_rect(center=(width-40, self.board_Y_level - self.side_length)))

            if check_inside_button(mousepos, (width-40, self.board_Y_level - self.side_length), button_side_len_half):
                write_text(screen, width//2, 460, "turns left until board reset", 15)
            else:
                write_text(screen, width//2, 460, "Click: confirm", 15)

        elif step==1:
            pass
        elif step==2:
            pass

    def check_tile_sum_to_6(self,tiles):
        amount_of_tiles = 0
        for tile_name, amount in tiles.items():
            amount_of_tiles += amount
        # print(amount_of_tiles)
        return amount_of_tiles == 6

    def collect_tiles(self,mousepos, out_of_board_protection = True): # center tile이 보드의 어느 타일을 가렸는지 준다
        if mousepos[1] < self.board_Y_selectable:  # not on the board
            return False

        planar_figure_center_locations = self.get_center_locations_planar_figure(mousepos)
        self.temp_board = copy.deepcopy(self.board) # temp board is an exact copy (also deep copy) of self.board : use the same method to access

        tiles = dict() # current tile collection
        for pc in planar_figure_center_locations:
            for i in range(len(self.board)):
                board_tile_location = self.board[i][0]
                board_tile_name = self.board[i][1]
                if check_inside_button(pc, board_tile_location, self.side_length//2): # whether ith tile is inside in one sector of planar figure
                    safe_tile_add_one(tiles,board_tile_name)  # add a tile to the current tile collection
                    self.temp_board[i] = [board_tile_location, 'Used']
                    #break # only one tile can be inside a pc

        if out_of_board_protection and (not self.check_tile_sum_to_6(tiles)): # detect whether planar figure is outside a board when clicking the board: BOSS FIGHT 에서는 out_of_board_protection = False로 줄거임
            return False

        # check whether some unusable tile is inside the planar figure
        if ('Unusable' in tiles) or ('Used' in tiles):        # if unusable tile is included, return False
            print("Invalid position: containing unusable or used tile")
            return False

        return tiles# return tile counts




