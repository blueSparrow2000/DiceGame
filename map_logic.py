'''
This is a map logic

TBU

'''
from util import *
import copy
import random

map_tile_names = ['void','base','campfire','fight','ruin','shop','altar','bridge','highlight']
event_tile_names = ['campfire','fight','ruin','shop','altar']
class Map():
    def __init__(self):
        global map_tile_names,event_tile_names
        self.map = [[['void',False] for x in range(7)] for y in range(7)] # tile name, reachability
        self.must_contain_at_least_one = [[False for x in range(7)] for y in range(7)]

        self.image_dict = dict() # load map tile images!
        for tile_name in map_tile_names:
            self.image_dict[tile_name] = (load_image("map_tiles/%s" % tile_name))

        self.side_length = 50 # map tile's length
        self.image_button_tolerance = 25

        self.map_Y_level = 480
        self.map_X = 240 - self.side_length*3 - self.side_length//2
    def random_initialize(self):
        self.map = [[['void',False] for x in range(7)] for y in range(7)]
        self.must_contain_at_least_one = [[[False] for x in range(7)] for y in range(7)] # 해당 픽셀이 must contain이어야 하나, True라면 해당 픽셀이 must contain이게 한 이유가 되는 픽셀 좌표를 넣음

        # spawn island randomly - fight/campfire/shop/boss/ruin/altar
        self.map[1][3] = ['fight',False]
        self.map[2][5] = ['ruin',False]
        self.map[3][3] = ['shop',False]
        self.map[4][2] = ['altar', False]

        # insert at-least-contain-one's in neighbors islands
        for c in range(7):
            for r in range(7):
                if self.map[c][r][0] in event_tile_names: # c,r이 이벤트 타일 위치일때, 그 주변을 전부 must contain으로 만든다
                    for y in range(-1,2):
                        for x in range(-1,2):
                            if 0<=c+y<=6 and 0<=r+x<=6: # must be inside the map
                                if x==0 or y==0: # middle parts
                                    if self.must_contain_at_least_one[c+y][r+x][0]: # 이미 true라면
                                        self.must_contain_at_least_one[c+y][r+x].append((c,r)) # 나중에 검사할때 하나라도 True인게 있으면 됨
                                    else: # 처음
                                        self.must_contain_at_least_one[c+y][r+x] = [True,(c,r)] # 나중에 검사할때 하나라도 True인게 있으면 됨

        # self.map[5][3] must contain this coordinate 5,3
        self.map[6][3] = ['base',False]  # must not contain this!



    def draw(self,screen):
        for i in range(7):
            for j in range(7):
                screen.blit(self.image_dict[self.map[i][j][0]], (self.map_X + j*self.side_length, self.map_Y_level + self.side_length*i))
    def check_tiles(self,position_on_map, board_obj): # center tile이 보드의 어느 타일을 가렸는지 준다
        self.bridge_map = [[False for x in range(7)] for y in range(7)]
        self.reachability_map = [[False for x in range(7)] for y in range(7)]

        tiles = {}
        center_x = position_on_map[0]
        center_y = position_on_map[1]

        at_least_one_flag = False
        must_contain_flag = False
        for c in range(board_obj.planar_figure_col):
            for r in range(board_obj.planar_figure_row):
                if (board_obj.current_planar_figure[c][r])==1: # draw only when exists
                    row_offset = (r - board_obj.planar_figure_center[1])*self.side_length
                    col_offset = (c - board_obj.planar_figure_center[0])*self.side_length

                    # 전개도의 부분 중 해당 위치가 보드의 어느 좌표인지 변환
                    row_board_idx = (center_x+row_offset - self.map_X) // self.side_length
                    col_board_idx = (center_y+col_offset - self.map_Y_level) // self.side_length
                    # check boarder
                    if (row_board_idx < 0 or col_board_idx < 0 or row_board_idx > 6 or col_board_idx > 6):
                        print("invalid position: outside the border")
                        return False

                    # check coordinate
                    if row_board_idx==3 and col_board_idx==5:
                        must_contain_flag = True

                    # collect tiles
                    this_tile = self.map[col_board_idx][row_board_idx][0] # only names
                    if this_tile in tiles:
                        tiles[this_tile] += 1
                    else: # not in there
                        tiles[this_tile] = 1 # initialize

                    if self.must_contain_at_least_one[col_board_idx][row_board_idx][0]:# must contain을 건드렸다면
                        at_least_one_flag = True
                        # update reachability - 해당 픽셀이 must contain인 이유를 찾아올라가서 그 픽셀의 reachability를 업데이트 하삼
                        locations = self.must_contain_at_least_one[col_board_idx][row_board_idx][1:]
                        for loc in locations:
                            self.reachability_map[loc[0]][loc[1]] = True # set reachability to true

                    self.bridge_map[col_board_idx][row_board_idx] = True

        # check must contain atleast ones
        if not at_least_one_flag:
            return False
        if not must_contain_flag:
            return False
        # check whether some unusable tile is inside the planar figure
        if ('base' in tiles): # containing these
            print("Invalid position: containing base tile")
            return False

        # self.map[5][3] must contain this coordinate 5,3
        #### TBU

        ########### confirm #################
        # update reachability info
        for c in range(7):
            for r in range(7):
                if self.reachability_map[c][r]:
                    self.map[c][r][1] = True # set reachability to true

        # bridging
        for c in range(7):
            for r in range(7):
                if self.bridge_map[c][r] and self.map[c][r][0]=='void':
                    self.map[c][r] = ['bridge',False]


        for tttt in range(7):
            print(self.map[tttt])
        return True



    def highlight_reachable_locations(self,screen):
        for c in range(7):
            for r in range(7):
                if self.map[c][r][1]: # reachable
                    screen.blit(self.image_dict['highlight'], (self.map_X + r*self.side_length, self.map_Y_level + self.side_length*c))


    def check_reachable_locations(self, mousepos):
        # collect location of all the reachable map tiles
        for c in range(7):
            for r in range(7):
                if self.map[c][r][1]: # reachable
                    if check_inside_button(mousepos, (self.map_X + r*self.side_length + self.side_length//2, self.map_Y_level + self.side_length*c + self.side_length//2), self.image_button_tolerance): # 이게 버튼 센터가 아닐 수 있음 (self.map_X + r*self.side_length, self.map_Y_level + self.side_length*c)
                        map_tile_name = self.map[c][r][0]
                        print(self.map[c][r])
                        return True, map_tile_name # is_valid, which_event
        return False, False
