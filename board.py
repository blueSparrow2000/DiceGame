import random
import pygame
from image_processor import *
from music import *
import copy
from variables import *

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
        global tile_names,planar_figures,sound_effects
        self.board = [[None for i in range(8)] for j in range(8)] # 이번 보드에만 영향을 주는건 이것만 바꿈 # has string of tile names
        self.temp_board = [[None for i in range(8)] for j in range(8)]
        self.board_original_dict = tiles_dict # 영구적인 영향을 주는 거면 이거도 바꿈
        tile_count = 0
        for k,v in self.board_original_dict.items():
            tile_count+=v
        self.board_original_dict['Empty'] = 64 - tile_count
        self.board_dict = self.board_original_dict # 이번 전투에만 영향을 주는거면 이거도 바꿈
        self.cube_figure = load_image('tiles/cube')

        self.image_dict = dict()
        for tile_name in tile_names:
            self.image_dict[tile_name] = (load_image("tiles/%s" % tile_name))

        self.translation_dict = {}
        self.side_length =  self.image_dict['Attack'].get_height()
        self.board_Y_level = 480
        self.board_X = 240 - self.side_length*4
        #self.rect = pygame.Rect((self.board_X,self.board_Y_level), (self.side_length*8,self.side_length*8))

        self.figure_index = 0 # 0 for primary, 1 for secondary
        self.planar_figure_idx = planar_figure_idx # absolute variants of planar figures
        self.init_planar_figures = [copy.deepcopy(planar_figures[self.planar_figure_idx[0]]),copy.deepcopy(planar_figures[self.planar_figure_idx[1]])]
        self.my_planar_figures = [planar_figures[self.planar_figure_idx[0]],planar_figures[self.planar_figure_idx[1]]]
        self.current_planar_figure = self.my_planar_figures[self.figure_index]
        self.planar_figure_col = len(self.current_planar_figure)
        self.planar_figure_row = len(self.current_planar_figure[0])
        self.planar_figure_center = [1,1] # col, row

        self.board_reset_turn = 6
        self.current_turn = 0

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

    def new_game(self):
        self.board_dict = self.board_original_dict

    def reset(self,enforced = False): # reset the board (each 6 turn)
        if (enforced or self.current_turn % self.board_reset_turn == 0):  # every 6th turn, reset the board
            board_temp = []
            for k,v in self.board_dict.items():
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
        for i in range(8):
            for j in range(8):
                self.board[i][j] = board_temp[i*8+j]
    def draw(self,screen, step):
        if step==0:
            for i in range(8):
                for j in range(8):
                    screen.blit(self.image_dict[self.board[i][j]], (self.board_X + j*self.side_length, self.board_Y_level + self.side_length*i))
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
                    if (row_board_idx < 0 or col_board_idx < 0 or row_board_idx > 7 or col_board_idx > 7):
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




