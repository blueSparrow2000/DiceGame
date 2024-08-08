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


################################################## planar figures ##########################################################
class Net():
    def __init__(self,planar_figure_idx, side_length, board_Y_selectable):
        global planar_figures
        self.figure_index = 0 # 0 for primary, 1 for secondary
        self.planar_figures = copy.deepcopy(planar_figures)
        self.planar_figure_idx = copy.deepcopy(planar_figure_idx) # absolute variants of planar figures
        self.init_planar_figures = [copy.deepcopy(planar_figures[self.planar_figure_idx[i]]) for i in range(len(self.planar_figure_idx))]
        self.my_planar_figures = [planar_figures[self.planar_figure_idx[i]] for i in range(len(self.planar_figure_idx)) ]
        self.current_planar_figure = self.my_planar_figures[self.figure_index]
        self.planar_figure_col = len(self.current_planar_figure)
        self.planar_figure_row = len(self.current_planar_figure[0])
        self.planar_figure_center = [1,1] # col, row
        self.board_Y_selectable = board_Y_selectable
        self.side_length = side_length
        self.cube_figure = load_image('tiles/cube')


    def draw_net_on_location(self, screen, center, given_shape = None):
        shape = self.current_planar_figure
        if given_shape:
            shape = given_shape

        for c in range(self.planar_figure_col):
            for r in range(self.planar_figure_row):
                if (shape[c][r])==1: # draw only when exists
                    location = (center[0] + (r - self.planar_figure_center[1])*self.side_length, center[1] + (c - self.planar_figure_center[0])*self.side_length)
                    screen.blit(self.cube_figure, self.cube_figure.get_rect(center=location))


    def refresh_planar_figure(self):
        self.planar_figure_col = len(self.current_planar_figure)
        self.planar_figure_row = len(self.current_planar_figure[0])
        # change the center pos accordingly
        #self.planar_figure_center = [1,1]

    def init_turn(self): # initialize planar figure at every turn starts
        self.figure_index = 0
        self.my_planar_figures = [copy.deepcopy(planar_figures[self.planar_figure_idx[i]]) for i in range(len(self.planar_figure_idx))]
        self.current_planar_figure = self.my_planar_figures[self.figure_index]
        self.refresh_planar_figure()

    def change_planar_figure(self, confused):
        if confused:
            return
        self.figure_index = (self.figure_index+1)%len(self.planar_figure_idx)
        self.current_planar_figure = self.my_planar_figures[self.figure_index]
        self.refresh_planar_figure()

    def draw_planar_figure(self,screen,mousepos):
        if mousepos[1] < self.board_Y_selectable:  # not on the board
            return False

        self.draw_net_on_location(screen, mousepos)
        # for c in range(self.planar_figure_col):
        #     for r in range(self.planar_figure_row):
        #         if (self.current_planar_figure[c][r])==1: # draw only when exists
        #             location = (mousepos[0] + (r - self.planar_figure_center[1])*self.side_length, mousepos[1] + (c - self.planar_figure_center[0])*self.side_length)
        #             screen.blit(self.cube_figure, self.cube_figure.get_rect(center=location))

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
BOSS FIGHT PARAMETERS

When reseting the board, it gets 'fragmented'
reset(self, enforced=False, irregular_reset_shape = 'fragmented')

Out of board protection becomes false! => more free space to use
collect_tiles(self,mousepos, out_of_board_protection = False)
'''
class Board():
    def __init__(self,tiles_dict,planar_figure_idx):
        global tile_names,sound_effects,board_Y_level
        self.board_side_length = 8
        self.board = [] # 이번 보드에만 영향을 주는건 이것만 바꿈  # 각 원소의 형태 = [location , tile name , fixed_or_not boolean ]
        self.temp_board = []
        self.permanent_board_dict = copy.deepcopy(tiles_dict) # 영구적인 영향을 주는 거면 이거도 바꿈
        tile_count = 0
        for k,v in self.permanent_board_dict.items():
            tile_count+=v
        self.permanent_board_dict['Empty'] = self.board_side_length**2 - tile_count
        # temporary board dict also preserves tiles like permanent one
        self.temporary_board_dict = copy.deepcopy(self.permanent_board_dict) # 이번 전투에만 영향을 주는거면 이거도 바꿈

        self.image_dict = dict()
        for tile_name in tile_names:
            self.image_dict[tile_name] = (load_image("tiles/%s" % tile_name))

        self.translation_dict = {}
        self.side_length = self.image_dict['Attack'].get_height()
        self.board_Y_level = board_Y_level + self.side_length//2
        self.board_Y_selectable = board_Y_level - self.side_length
        self.board_X = width//2 - self.side_length*4 + self.side_length//2

        self.board_reset_turn = 6
        self.current_turn = 0
        self.board_reset_icon = load_image("icons/reset")

        ##################### FIXED TILE ######################
        self.permanently_fixed_tiles = dict()
        self.temp_permanently_fixed_tiles = dict()
        self.fixed_board = [['Empty' for i in range(self.board_side_length)] for j in range(self.board_side_length)]
        self.permanent_fix_exist_flag = False
        ##################### FIXED TILE ######################

        self.out_of_board_protection = True
        self.irregular_shape = False #'stripe'#False#'stripe'
        self.board_shuffle_every_turn = False

        ############# planar figure ##############
        self.net = Net(planar_figure_idx,self.side_length ,self.board_Y_selectable)
        ############# planar figure ##############

        self.number_of_permanent_tiles = 0 # used in ending credit

    def set_out_of_board_protection(self, bool_input):
        self.out_of_board_protection = bool_input

    def set_irregular_shape(self, shape):
        self.irregular_shape = shape

    def set_board_shuffle(self, bool_input):
        self.board_shuffle_every_turn = bool_input
    '''
    You can change board reset frequency by calling the below function. Initially it is 6 turns.
    '''
    def change_board_reset_frequency_by(self, reset_turns=1):
        if self.board_reset_turn <= reset_turns:
            print("cannot decrease board reset turn")
            return
        self.board_reset_turn -= reset_turns

    def count_all_permanent_tiles(self):
        number_of_tiles = 0
        for tile_name,tile_amount in self.permanent_board_dict.items():
            if tile_name != 'Empty':
                number_of_tiles += tile_amount

        self.number_of_permanent_tiles = number_of_tiles


    ################################################## permenant changes ##################################################

    ##################### FIXED TILE ######################

    '''
    How to use(outside the board function):
    
    player.board.permenantly_add_fixed_tile_location(player.board.get_index_from_pos(mousepos), tile_name_to_fix)
    '''

    def fixed_boardify(self,board_temp): # change images where board is changed to used
        fixed_board = [[None for i in range(self.board_side_length)] for j in range(self.board_side_length)]
        for i in range(self.board_side_length):
            for j in range(self.board_side_length):
                fixed_board[i][j] = board_temp[i*self.board_side_length+j]
        return fixed_board
    def update_fixed_board(self): # called only when clicking / or reseting (back button)
        temp_board = ['Empty' for j in range(self.board_side_length**2)]
        for fixed_tile_idx,tile_name in self.temp_permanently_fixed_tiles.items():
            temp_board[fixed_tile_idx] = tile_name
        # update fixed board
        self.fixed_board = self.fixed_boardify(temp_board)

    def draw_fixed_board(self,screen):
        for i in range(self.board_side_length):
            for j in range(self.board_side_length):
                img = self.image_dict[self.fixed_board[i][j]]
                screen.blit(img,img.get_rect(center=(self.board_X + j*self.side_length, self.board_Y_level + self.side_length*i)))

    def get_index_from_pos(self, mousepos): # (65,505) very first elem?
        center_x = mousepos[0]
        center_y = mousepos[1]

        # 전개도의 부분 중 해당 위치가 보드의 어느 좌표인지 변환: 보드가 중앙을 기준으로 가운데 맞춤 되어 있을 때의 경우이다!!
        row_board_idx = (center_x - (self.board_X - self.side_length//2)) // self.side_length
        col_board_idx = (center_y - (self.board_Y_level - self.side_length//2)) // self.side_length

        if (row_board_idx < 0 or col_board_idx < 0 or row_board_idx > (self.board_side_length - 1) or col_board_idx > (
                self.board_side_length - 1)):
            # print("invalid position: outside the border")
            return -1 # improper location index

        return col_board_idx*self.board_side_length + row_board_idx


    ''' 
    Can fix a tile!
    How to use:
    Make an interface to fix a tile (self.board_side_length by self.board_side_length grid, click on the mouse and get the location)
     - check it is a valid location:
        > permanent tiles should have at least one empty slot to accept a fixed tile
        > it should not crash with other fixed tile location
        > location index should be properly given (not False)
    WHEN USING RETURN VALUE OF THIS FUNCTION if this function returned false, it should get a player mouse position again for proper fixed tile location
    it returns true when adding fixed tile succeed
     
     
     WARNING: when adding a fixed tile into the fixed tile list, that tile should also be added to a permanent tile (and call self.permanently_replace_a_blank_tile_to(tile_name))
     
     
     
    When reseting the board, exclude the number of fixed tiles from the self.temporary_board_dict when generating random set
    Then add a fixed tile into the desired index calculated when it is made
    보드 리셋 할때만 고정된거, 아닌거 두개를 구분해 주면 되는거니까! 
    
    형태
    fixed_tile = {location : tile_name, ...  } 
    tile_name: string ('Attack' etc..)
    location: integer (called location_index) => calculated value corresponding to clicked tile's location in 1D array ( = col*self.board_side_length + row )
    '''
    def permenantly_add_fixed_tile_location(self, location_index, tile_name):
        if not self.check_tile_exists_in_permanent('Empty'):
            print("My tiles are full!!! Can not add more!")
            return False

        if location_index==-1: # when given improper location index
            # print("invalid location index")
            return False

        # check whether the tile collides location with existing tiles
        for fixed_tile_idx in self.permanently_fixed_tiles.keys():
            if location_index == fixed_tile_idx:
                print("tile already exists in that location!")
                return  False

        self.reset_fixing_tile()
        # add one!
        self.temp_permanently_fixed_tiles[location_index] = tile_name
        self.permanent_fix_exist_flag = True
        self.update_fixed_board()
        # print("P ",self.permanently_fixed_tiles)
        # print("T ", self.temp_permanently_fixed_tiles)
        return True # success

    def update_temp_fixed(self,mousepos, tile_name_to_fix):
        self.permenantly_add_fixed_tile_location(self.get_index_from_pos(mousepos), tile_name_to_fix)

    def confirm_fixing_tile(self,tile_name_to_fix):
        if self.permanent_fix_exist_flag:
            self.permanently_fixed_tiles = copy.deepcopy(self.temp_permanently_fixed_tiles)
            # also add one to the permanent tiles!
            self.permanently_replace_a_blank_tile_to(tile_name_to_fix)
            print("Fixed a tile permanently!")
            self.reset_fixing_tile()

    def reset_fixing_tile(self):
        self.temp_permanently_fixed_tiles = copy.deepcopy(self.permanently_fixed_tiles)
        self.permanent_fix_exist_flag = False
        self.update_fixed_board()
    ##################### FIXED TILE ######################
    '''
    return a dictionary:
    permanent_tiles - number of fixed tiles for each tiles
    
    Because we need to randomized location of non-fixed tiles! (excluding fixed tiles!)
    
    NOTE: fixed tile's values (strings) are subset of permanent tiles' keys, so theres always exist a tile in temporary_board_dict that fixed_tiles has 
    '''
    def get_non_fixed_tiles(self, reference_dict = None):
        if reference_dict is None:
            reference_dict = self.temporary_board_dict


        temp_board_dict_excluding_fixed_tiles = copy.deepcopy(reference_dict)

        fixed_tile_names = list(self.permanently_fixed_tiles.values()) # get list of tile names
        for tile_name, tile_amount in reference_dict.items():
            for i in range(fixed_tile_names.count(tile_name)):
                safe_delete_dict_one(temp_board_dict_excluding_fixed_tiles, tile_name) # get rid of amount of fixed tiles in the temp_excluded_fixed array

        return temp_board_dict_excluding_fixed_tiles



    def display_tile(self,screen,tile_name, location):
        img = self.image_dict[tile_name]
        screen.blit(img, img.get_rect(center=location))



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
    Convert all non-fixed tile of type1 to type2
    
    '''
    def permanently_convert_tile1_to_tile2(self, tile_1,tile_2):
        not_fixed_permanent_tiles = self.get_non_fixed_tiles(self.permanent_board_dict)
        # if tile_1 exists in nfpt and higher than 0
        # then get its count n
        # delete a tile_1 n times in permanent
        # add a tile_2 n times in permanent
        if tile_1 in not_fixed_permanent_tiles and not_fixed_permanent_tiles[tile_1] > 0:
            number_to_convert = not_fixed_permanent_tiles[tile_1]
            for i in range(number_to_convert):
                safe_tile_add_one(self.permanent_board_dict, tile_2)
                safe_delete_dict_one(self.permanent_board_dict, tile_1)

        # print(self.temporary_board_dict)
        # print(self.permanent_board_dict)

        self.reset_permanent_board_dict() # recalculate the empty tiles


    '''
    Use this function to delete a tile permanently
    The deleted tile becomes empty tile
    '''
    def permanently_delete_a_tile(self, target_tile):
        safe_delete_dict_one(self.permanent_board_dict, target_tile)
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
        for fixed_tile_idx in list(self.permanently_fixed_tiles.keys()):# if index goes beyond, then delete the tile
            if fixed_tile_idx > (self.board_side_length)**2:
                del self.permanently_fixed_tiles[fixed_tile_idx]

        self.reset_permanent_board_dict()




    def shrink_recalculate_board_offsets(self):
        self.board_X = width//2 - (self.side_length//2) * self.board_side_length + self.side_length//2 # centerize

    ################################################## permenant changes ##################################################

    '''
    Is there at least one tile?
    '''
    def check_tile_exists_in_temporal(self, given_tile):
        return given_tile in self.temporary_board_dict and self.temporary_board_dict[given_tile] > 0 # if such tile exists and is having more than one

    '''
    Re calculate # of empty tiles for temporal board
    '''
    def reset_temporal_board_dict(self):
        tile_count = 0
        for k,v in self.temporary_board_dict.items():
            if k != 'Empty': # count non-empty tiles only
                tile_count+=v
        self.temporary_board_dict['Empty'] = self.board_side_length**2 - tile_count # reset empty tiles

    '''
    Use this function to add a tile on a battle (but not permanently)
    '''
    def temporarily_replace_a_blank_tile_to(self, target_tile):
        if not self.check_tile_exists_in_temporal('Empty'):
            print("My tiles are full!!! Can not add more!")
            return
        safe_tile_add_one(self.temporary_board_dict, target_tile)
        self.reset_temporal_board_dict() # recalculate the empty tiles


    '''
    reset board & temporary tile dict when the game starts
    '''
    def new_game(self):
        self.current_turn = 0
        self.temporary_board_dict = copy.deepcopy(self.permanent_board_dict)
        self.clear_board()
        self.temp_board = copy.deepcopy(self.board)

    def confirm_using_tile(self): # this should be called before player.end_my_turn
        self.board = self.temp_board

    def turn_end_shuffle(self):
        # check to reshuffle or not - just shuffle the contents!
        if self.board_shuffle_every_turn:
            self.shuffle_board()

    def turn_end_check(self, player,copy_of_current_tile): # do something with player's current board at the turn end
        # shuffle if needed
        self.turn_end_shuffle()

        # do stuffs at my turn end

        # for current tiles, count number of spikes that deals damage to my self
        for tile_name, amount in copy_of_current_tile.items():
            if tile_name=="Spike": # deal damage
                sound_effects['hard_hit'].play()
                spike_damage = 10*amount
                player.take_damage(None, spike_damage)


    def shuffle_board(self):
        not_fixed_tile_index = []
        locations_to_shuffle = []
        # get locations to shuffle
        for i in range(len(self.board)):
            tile_location, tile_name, is_fixed = self.board[i]
            if is_fixed:
                continue
            not_fixed_tile_index.append(i)
            locations_to_shuffle.append(tile_location)

        random.shuffle(locations_to_shuffle)

        # assign new location to designated places
        cnt = 0
        for i in not_fixed_tile_index:
            self.board[i][0] = locations_to_shuffle[cnt]
            cnt += 1


    def check_a_tile_is_a_fixed_tile_with_index(self, location_index):
        # check this index is for fixed tile or not
        if location_index in self.permanently_fixed_tiles.keys():
            return True
        return False


    def tile_effects_on_board_reset(self, player):
        proliferation_amount = 0
        for i in range(len(self.board)):
            board_tile_name = self.board[i][1]
            if board_tile_name == 'Proliferation':
                proliferation_amount += 5


        if proliferation_amount > 0:
            sound_effects['water'].play()
            player.take_damage(None, proliferation_amount)



    def replicate_tile(self, replication_info):
        board_index = replication_info[0]
        tile_name = replication_info[1]
        # for each neighbors on my board, find empty tile
        # then replace it to tile_name
        self.board[board_index][1] = tile_name
        # self.temp_board[board_index][1] = tile_name

    def find_empty_spot_idx_in_neighbor(self, my_location):
        # [self.board_X + j * self.side_length, self.board_Y_level + self.side_length * i]

        my_neighbors = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if (i==0 or j==0) and not (i==0 and j==0):
                    location = [my_location[0] + i*self.side_length, my_location[1] + j*self.side_length]
                    my_neighbors.append(location)

        irregular_shaped_board_randomizer = []
        for board_index in range(len(self.board)):
            tile_location = self.board[board_index][0]
            tile_name = self.board[board_index][1]
            is_fixed = self.board[board_index][2]
            if tile_name=='Empty': # can proliferate
                # it should be either up down left right of my location (on irregular board, replicate to random location)
                if tile_location in my_neighbors: # if this tile is neighbor with my current tile
                    return board_index
                irregular_shaped_board_randomizer.append(board_index)


        if self.irregular_shape:  # get any random non-empty location (no need to be a neighbor)
            random.shuffle(irregular_shaped_board_randomizer)
            board_index = irregular_shaped_board_randomizer[0]
            return board_index

        return None

    def force_reset_next_turn(self):
        self.current_turn = 0

    def reset(self, player = None):  # reset the board (each 6 turn) right after the end of the player's turn
        '''
        This function only resets content of current board

        Location is determined in the boardify function!

        board_temp = list of tile names (no location information when creating)
        '''

        self.net.init_turn() # initialize planar figures

        if (self.current_turn % self.board_reset_turn == 0):  # every 6th turn, reset the board
            if player: # when player is given, consider reset panalties
                self.tile_effects_on_board_reset(player)

            ############### RESET BOARD ###############
            self.clear_board()  # empty the board only when reset
            board_temp = []

            ######### fixed tile handling ##########
            non_fixed_tile_to_use = self.get_non_fixed_tiles()
            for k, v in non_fixed_tile_to_use.items(): # fetch board content to an array
                tile = k
                for i in range(v):
                    board_temp.append(tile)
            random.shuffle(board_temp)  # randomize

            # add fixed tiles in appropriate index (which will be calculated in boardify or shapify)
            fixed_locations = list(self.permanently_fixed_tiles.keys())
            fixed_locations.sort() # sort 해야 insert할시 작은 순서 인덱스부터 차곡차곡 들어가서 맞는 결과 나옴
            for fixed_tile_idx in fixed_locations:
                board_temp.insert(fixed_tile_idx,self.permanently_fixed_tiles[fixed_tile_idx])
            ######### fixed tile handling ##########

            if self.irregular_shape:
                self.irregular_shapify(board_temp)
            else:
                self.boardify(board_temp) # set up a board
            ############### RESET BOARD ###############
            self.current_turn = 0 # reset turn
        else:
            ############################ replication ##############################
            replication_queue = []  # self.board의 index, tile_name to replicate
            for board_index in range(len(self.board)):
                tile_location = self.board[board_index][0]
                tile_name = self.board[board_index][1]
                # is_fixed = self.board[board_index][2]

                if tile_name == "Karma" or tile_name == "Proliferation":
                    board_idx_to_replicate = self.find_empty_spot_idx_in_neighbor(
                        tile_location)  # check for adjacent empty tiles and dup
                    if board_idx_to_replicate is not None:  # if there is a spot to replicate
                        replication_queue.append([board_idx_to_replicate, tile_name])

            # replication - proliferate / karma
            for replication_tile in replication_queue:
                self.replicate_tile(replication_tile)
            ############################ replication ##############################


        # print(self.board)
        self.current_turn += 1


    def clear_board(self):
        self.board = [] # initialize board

    ############################################################################################################ BOARD INDIRECTION 수정은 여기부터! ############################################################################################################
    '''
    Insert a tile into the board (randomly) only if there is a space (which is an empty tile)    
    '''
    def insert_a_tile_on_board(self, tile_name):
        self.replace_a_tile_on_board('Empty', tile_name)
        # random.shuffle(self.board)
        # self.temp_board = copy.deepcopy(self.board) # temp board is an exact copy (also deep copy) of self.board : use the same method to access
        # for i in range(len(self.board)):
        #     board_tile_name = self.board[i][1]
        #     if board_tile_name == 'Empty': # change the names!
        #         self.board[i][1] = tile_name
        #         self.temp_board[i][1] = tile_name
        #         break # insert one tile!

    def replace_a_tile_on_board(self, replaced_tile, replacing_tile):
        random.shuffle(self.board)
        self.temp_board = copy.deepcopy(self.board) # temp board is an exact copy (also deep copy) of self.board : use the same method to access
        for i in range(len(self.board)):
            board_tile_name = self.board[i][1]
            if board_tile_name == replaced_tile: # change the names!
                self.board[i][1] = replacing_tile
                self.temp_board[i][1] = replacing_tile
                return # insert one tile! # break

        print("replacing failed while trying to add %s: no tile named '%s'"%(replacing_tile, replaced_tile))

    def convert_all_tiles_on_board(self,target_tile, convert_tile): # convert target tile into convert tile after confirmation
        # loop through current board and change all 'tile_name' tiles into 'Used' tiles
        for i in range(len(self.board)):
            board_tile_name = self.board[i][1]
            if board_tile_name == target_tile:
                self.temp_board[i][1] = convert_tile  # temp 를 바꿔야 변경사항이 적용됨 confirm에서!
                self.temp_board[i][2] = False  # not fixed tile

    def convert_all_tiles_on_board_immediately(self,target_tile, convert_tile): # convert target tile into convert tile immediately
        # loop through current board and change all 'tile_name' tiles into 'Used' tiles
        for i in range(len(self.board)):
            board_tile_name = self.board[i][1]
            if board_tile_name == target_tile:
                self.board[i][1] = convert_tile  # temp 를 바꿔야 변경사항이 적용됨 confirm에서!
                self.board[i][2] = False  # not fixed tile


    def consume_all_tiles_on_board(self, target_tile): # consume all tiles and return how many are (actually) consumed
        how_many_consumed = 0
        for i in range(len(self.board)):
            current_tile_name = self.board[i][1]
            if current_tile_name == target_tile:
                self.temp_board[i][1] = 'Used'  # temp 를 바꿔야 변경사항이 적용됨 confirm에서!
                self.temp_board[i][2] = False # not fixed tile
                how_many_consumed += 1
        return how_many_consumed

    def count_all_tiles_on_board(self, target_tile): # for lookahead
        how_many = 0
        for i in range(len(self.board)):
            current_tile_name = self.board[i][1]
            if current_tile_name == target_tile:
                how_many += 1
        return how_many


    def irregular_shapify(self, board_temp):
        # calculate irregular locations!
        if self.irregular_shape=='stripe':
            for i in range(self.board_side_length):
                for j in range(self.board_side_length):
                    board_tile = [[self.board_X + j * self.side_length, self.board_Y_level + self.side_length * i * 1.1], board_temp[i*self.board_side_length + j] ,False] # False: not a fixed tile
                    if self.check_a_tile_is_a_fixed_tile_with_index(i*self.board_side_length + j):
                        board_tile[2]=True
                    self.board.append(board_tile)

        elif self.irregular_shape=='fragmented':
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
                board_tile = [[width//2 + fragment[0], (height//4)*3 + fragment[1]], board_temp[i], False]
                if self.check_a_tile_is_a_fixed_tile_with_index(i):
                    board_tile[2] = True

                self.board.append(board_tile)
        elif self.irregular_shape=='diamond':
            pass
        elif self.irregular_shape == 'circular':
            pass

    def boardify(self,board_temp): # change images where board is changed to used
        '''
        boardifying with grid shape centered middle vertical line

        IMPORTANT: assigns location and tile information here!!!!!
        '''
        for i in range(self.board_side_length):
            for j in range(self.board_side_length):
                board_tile = [[self.board_X + j * self.side_length, self.board_Y_level + self.side_length * i], board_temp[i*self.board_side_length + j],False ]
                if self.check_a_tile_is_a_fixed_tile_with_index(i * self.board_side_length + j):
                    board_tile[2] = True
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

    def collect_tiles(self,mousepos): # center tile이 보드의 어느 타일을 가렸는지 준다
        if mousepos[1] < self.board_Y_selectable:  # not on the board
            return False

        planar_figure_center_locations = self.net.get_center_locations_planar_figure(mousepos)
        self.temp_board = copy.deepcopy(self.board) # temp board is an exact copy (also deep copy) of self.board : use the same method to access

        tiles = dict() # current tile collection
        for pc in planar_figure_center_locations:
            for i in range(len(self.board)):
                board_tile_location = self.board[i][0]
                board_tile_name = self.board[i][1]
                if check_inside_button(pc, board_tile_location, self.side_length//2): # whether ith tile is inside in one sector of planar figure
                    safe_tile_add_one(tiles,board_tile_name)  # add a tile to the current tile collection
                    self.temp_board[i] = [board_tile_location, 'Used',False] # it becomes not fixed after used
                    #break # only one tile can be inside a pc

        # print(tiles)

        if self.out_of_board_protection and (not self.check_tile_sum_to_6(tiles)): # detect whether planar figure is outside a board when clicking the board: BOSS FIGHT 에서는 out_of_board_protection = False로 줄거임
            return False

        # check whether some unusable tile is inside the planar figure
        if ('Unusable' in tiles) or ('Used' in tiles):        # if unusable tile is included, return False
            print("Invalid position: containing unusable or used tile")
            return False

        return tiles# return tile counts



