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

class Board():
    def __init__(self,tiles_dict,planar_figure_idx):
        global tile_names,planar_figures,sound_effects,board_Y_level
        self.board_side_length = 8
        self.board = [[None for i in range(self.board_side_length)] for j in range(self.board_side_length)] # 이번 보드에만 영향을 주는건 이것만 바꿈 # has string of tile names
        self.temp_board = [[None for i in range(self.board_side_length)] for j in range(self.board_side_length)]
        self.permanent_board_dict = copy.deepcopy(tiles_dict) # 영구적인 영향을 주는 거면 이거도 바꿈
        tile_count = 0
        for k,v in self.permanent_board_dict.items():
            tile_count+=v
        self.permanent_board_dict['Empty'] = self.board_side_length**2 - tile_count
        self.temporary_board_dict = copy.deepcopy(self.permanent_board_dict) # 이번 전투에만 영향을 주는거면 이거도 바꿈
        # print(self.permanent_board_dict)
        # print(self.temporary_board_dict)
        self.cube_figure = load_image('tiles/cube')

        self.image_dict = dict()
        for tile_name in tile_names:
            self.image_dict[tile_name] = (load_image("tiles/%s" % tile_name))

        self.translation_dict = {}
        self.side_length =  self.image_dict['Attack'].get_height()
        self.board_Y_level = board_Y_level
        self.board_X = width//2 - self.side_length*4
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

    def check_number_of_given_tiles_is_geq_amount_in_permanent(self, given_tile, amount=1):
        return given_tile in self.permanent_board_dict and self.permanent_board_dict[given_tile] >= amount # if such tile exists and is having more than one


    def check_number_of_given_tiles_in_permanent(self, given_tile, amount=1):
        return given_tile in self.permanent_board_dict and self.permanent_board_dict[given_tile] == amount # if such tile exists and is having more than one

    def check_tile_exists_in_permanent(self, given_tile):
        return given_tile in self.permanent_board_dict and self.permanent_board_dict[given_tile] > 0 # if such tile exists and is having more than one



    '''
    Use this function to add a tile permanently
    
    '''
    def permanently_replace_a_blank_tile_to(self, target_tile):
        pass

    '''
    Use this function to delete a tile permanently
    The tile becomes empty tile
    '''
    def permanently_delete_a_tile(self, target_tile):
        pass


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
        # print(self.permanent_board_dict)

    def shrink_recalculate_board_offsets(self):
        self.board_X = width//2 - (self.side_length//2) * self.board_side_length


    def convert_all_tiles_on_board(self,target_tile, convert_tile): # convert target into convert tile
        # loop through current board and change all 'tile_name' tiles into 'Used' tiles
        for i in range(self.board_side_length):
            for j in range(self.board_side_length):
                current_tile = self.board[i][j]
                if current_tile == target_tile:
                    self.temp_board[i][j] = convert_tile # temp 를 바꿔야 변경사항이 적용됨 confirm에서!


    def consume_all_tiles_on_board(self, tile_name): # consume all tiles and return how many are (actually) consumed
        how_many_consumed = 0
        # loop through current board and change all 'tile_name' tiles into 'Used' tiles
        for i in range(self.board_side_length):
            for j in range(self.board_side_length):
                current_tile = self.board[i][j]
                if current_tile == tile_name:
                    self.temp_board[i][j] = 'Used' # temp 를 바꿔야 변경사항이 적용됨 confirm에서!
                    how_many_consumed+=1

        return how_many_consumed

    def count_all_tiles_on_board(self, tile_name): # for lookahead
        how_many = 0
        # loop through current board and change all 'tile_name' tiles into 'Used' tiles
        for i in range(self.board_side_length):
            for j in range(self.board_side_length):
                if self.board[i][j] == tile_name:
                    how_many+=1

        return how_many


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

    def refresh_planar_figure(self):
        self.planar_figure_col = len(self.current_planar_figure)
        self.planar_figure_row = len(self.current_planar_figure[0])
        # change the center pos accordingly
        #self.planar_figure_center = [1,1]

    '''
    reset board & temporary tile dict when the game starts
    '''
    def new_game(self):
        self.current_turn = 0
        self.temporary_board_dict = copy.deepcopy(self.permanent_board_dict)
        self.reset(True)


    def reset(self,enforced = False): # reset the board (each 6 turn)
        if (enforced or self.current_turn % self.board_reset_turn == 0):  # every 6th turn, reset the board
            board_temp = []
            for k,v in self.temporary_board_dict.items():
                tile = k
                for i in range(v):
                    board_temp.append(tile)
            random.shuffle(board_temp)
            # boardify
            self.boardify(board_temp)

            # reset turn
            self.current_turn = 0

        self.current_turn+=1

        # initialize planar figures
        self.init_turn()

    def boardify(self,board_temp): # change images where board is changed to used
        for i in range(self.board_side_length):
            for j in range(self.board_side_length):
                self.board[i][j] = board_temp[i*self.board_side_length+j]
    def draw(self,screen, step, mousepos):
        global write_text
        if step==0:
            for i in range(self.board_side_length):
                for j in range(self.board_side_length):
                    screen.blit(self.image_dict[self.board[i][j]], (self.board_X + j*self.side_length, self.board_Y_level + self.side_length*i))

            turns_remaining_until_board_reset = self.board_reset_turn - self.current_turn + 1
            # draw reset counter
            if turns_remaining_until_board_reset==1:
                write_text(screen, width-40 , self.board_Y_level - 25, "%d"%(turns_remaining_until_board_reset), 20, color = 'red')
            else:
                write_text(screen, width-40, self.board_Y_level - 25, "%d" % (turns_remaining_until_board_reset), 20)

            screen.blit(self.board_reset_icon,self.board_reset_icon.get_rect(center=(width-40, self.board_Y_level - 25)))

            if check_inside_button(mousepos, (width-40, self.board_Y_level - 25), button_side_len_half):
                write_text(screen, width//2, 460, "turns left until board reset", 15)
            else:
                write_text(screen, width//2, 460, "Click: confirm", 15)


        elif step==1:
            pass
        elif step==2:
            pass
    def draw_planar_figure(self,screen,mousepos):
        for c in range(self.planar_figure_col):
            for r in range(self.planar_figure_row):
                if (self.current_planar_figure[c][r])==1: # draw only when exists
                    location = (mousepos[0] + (r - self.planar_figure_center[1])*self.side_length, mousepos[1] + (c - self.planar_figure_center[0])*self.side_length)
                    screen.blit(self.cube_figure, self.cube_figure.get_rect(center=location))

    def rotate_once(self):
        self.current_planar_figure = list(zip(*self.current_planar_figure[::-1]))
        self.refresh_planar_figure()

    def collect_tiles(self,position_on_board): # center tile이 보드의 어느 타일을 가렸는지 준다
        self.temp_board = copy.deepcopy(self.board)
        # tiles = {'Attack':0, 'Defence':0, 'Regen':0, 'Skill':0, 'Used':0, 'Empty':0, 'Unusable':0} # TILES INIT
        tiles = {}
        center_x = position_on_board[0]
        center_y = position_on_board[1]
        for c in range(self.planar_figure_col):
            for r in range(self.planar_figure_row):
                if (self.current_planar_figure[c][r])==1: # draw only when exists
                    row_offset = (r - self.planar_figure_center[1])*self.side_length
                    col_offset = (c - self.planar_figure_center[0])*self.side_length

                    row_board_idx = (center_x+row_offset - self.board_X) // self.side_length
                    col_board_idx = (center_y+col_offset - self.board_Y_level) // self.side_length
                    # check boarder
                    if (row_board_idx < 0 or col_board_idx < 0 or row_board_idx > (self.board_side_length-1) or col_board_idx > (self.board_side_length-1)):
                        print("invalid position: outside the border")
                        return False

                    # collect tiles
                    this_tile = self.board[col_board_idx][row_board_idx]
                    if this_tile in tiles:
                        tiles[this_tile] += 1
                    else: # not in there
                        tiles[this_tile] = 1 # initialize

                    self.temp_board[col_board_idx][row_board_idx] = 'Used'# change to used


        # check whether some unusable tile is inside the planar figure
        # if unusable tile is counted, return False
        if ('Unusable' in tiles) or ('Used' in tiles): # containing these
            print("Invalid position: containing unusable or used tile")
            return False
        # print(tiles)
        return tiles# return tile counts

    def confirm_using_tile(self):
        self.board = self.temp_board




