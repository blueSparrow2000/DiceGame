'''
This is a map logic

TBU

'''
from util import *
import copy
import random

map_tile_names = ['void','base','campfire','fight','ruin','shop','altar','bridge','highlight','boss_fight']
event_tile_names = ['campfire','fight','ruin','shop','altar']
class Map():
    def __init__(self):
        global map_tile_names,event_tile_names
        self.map = [[['void',False] for x in range(7)] for y in range(7)] # tile name, reachability
        self.must_contain_at_least_one = [[False for x in range(7)] for y in range(7)]

        self.map_save = copy.deepcopy(self.map) # for reset

        self.image_dict = dict() # load map tile images!
        for tile_name in map_tile_names:
            self.image_dict[tile_name] = (load_image("map_tiles/%s" % tile_name))

        self.side_length = 50 # map tile's length
        self.image_button_tolerance = 25

        self.map_Y_level = 480
        self.map_X = 240 - self.side_length*3 - self.side_length//2

        # animation variables
        self.moving_X = 0
        self.moving_Y = 0
        self.block_paths = [] # 거리 단위임에 유의
        self.target = [0,0] # c,r
        self.move_index = 0
        self.imaginary_location = [5,3] # 5,3에서 시작
        self.path_finder_fail = False

        self.move_speed = 2 # must divide self.side_length

        self.break_limit = False

        self.debug_mode = False

    def random_initialize(self, player):
        self.moving_X = 0
        self.moving_Y = 0
        self.block_paths = [] # 거리 단위임에 유의
        self.target = [0,0]
        self.move_index = 0
        self.imaginary_location = [5,3] # 5,3에서 시작
        self.path_finder_fail = False


        self.map = [[['void',False] for x in range(7)] for y in range(7)]
        self.must_contain_at_least_one = [[[False] for x in range(7)] for y in range(7)] # 해당 픽셀이 must contain이어야 하나, True라면 해당 픽셀이 must contain이게 한 이유가 되는 픽셀 좌표를 넣음

        ################# init ###################
        '''
        주의: 마지막 column에서는 스폰시키지 마 (base랑 같은 위치의 타일의 경우 스폰 X)
        즉 self.map[6][x]는 건드리지 마!! c=6
        
        '''
        if self.break_limit or player.current_depth=='LIMIT' or player.current_depth <= -100: # only boss fight tile is given
            self.map[1][3] = ['fight',False]
            self.break_limit = True
        else:
            # spawn island randomly - fight/campfire/shop/boss/ruin/altar
            self.map[1][3] = ['fight',False]
            self.map[2][5] = ['ruin',False]
            self.map[3][3] = ['shop',False]
            self.map[4][2] = ['altar', False]
            self.map[4][5] = ['campfire', False]

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

        self.map_save = copy.deepcopy(self.map)

    def reset(self):
        self.map = copy.deepcopy(self.map_save)

    def draw(self,screen):
        global top_down_player
        for i in range(7):
            for j in range(7):
                if self.map[i][j][0]=='fight':
                    if self.break_limit:  # boss fight
                        screen.blit(self.image_dict['boss_fight'], (self.map_X + j*self.side_length, self.map_Y_level + self.side_length*i))
                        continue
                screen.blit(self.image_dict[self.map[i][j][0]], (self.map_X + j*self.side_length, self.map_Y_level + self.side_length*i))


        screen.blit(top_down_player,(self.map_X + 3 * self.side_length, self.map_Y_level + self.side_length * 6))

    def is_not_void(self,c,r):
        return not self.map[c][r][0]=='void'

    def is_bridge(self,c,r):
        return self.map[c][r][0]=='bridge'


    def update_target(self, location):
        self.target = location
        
    def find_path(self):
        '''
        도중에 bridge가 아닌 다른 타일을 거치게 된다면 => 그 타일이 목적지로 재설정 된다!!


        '''
        fail_counter = 0 # 아직 ㄷ자 형으로된 경로의 경우 이런 알고리즘으로는 가는게 불가능함. 카운터가 너무 크면 그냥 바로 이동시켜
        fail_limit = 20
        hard_fail = False


        if self.debug_mode:
            self.print_map()
        # go up one block (start position)

        self.block_paths.append([0,0,0,50]) # 일단 한칸 앞으로는 항상 가야함 [+x, -x, +y, -y]의 amount로 저장해두기 right lefft down up

        # 택시 기하 거리
        delta = abs(self.target[0]- self.imaginary_location[0]) + abs(self.target[1]- self.imaginary_location[1])
        while delta > 1: # 한칸 앞둔 경우엔 델타에 따라 넣으면 끝
            fail_counter+= 1

            if (not self.is_bridge(self.imaginary_location[0],self.imaginary_location[1])) and self.is_not_void(self.imaginary_location[0],self.imaginary_location[1]): # 현재 내가 밟고 있는 위치가 브릿지가 아니고 보이드도 아닐때
                # 현재 위치를 타깃으로 재설정한다!
                # 그리고 실행할거를 바꿔야함
                self.target = [self.imaginary_location[0],self.imaginary_location[1]]
                return self.map[self.imaginary_location[0]][self.imaginary_location[1]][0], 6-self.imaginary_location[0] # 더이상 패스파인팅 할 필요 없음


            y_checked = False

            if (self.target[0]- self.imaginary_location[0]) < 0 and self.is_not_void(self.imaginary_location[0] - 1,self.imaginary_location[1]): # y remaining & there is a bridge
                self.imaginary_location[0] -= 1
                self.block_paths.append([0, 0, 0, 50]) # go up
                y_checked = True
                if self.debug_mode:
                    print("up")
            if (self.target[0]- self.imaginary_location[0]) > 0 and self.is_not_void(self.imaginary_location[0] + 1,self.imaginary_location[1]): # y remaining
                self.imaginary_location[0] += 1
                self.block_paths.append([0, 0, 50, 0]) # go down
                y_checked = True
                if self.debug_mode:
                    print("down")

            if not y_checked: # change x accordingly
                if (self.target[1] - self.imaginary_location[1]) > 0 :
                    self.imaginary_location[1] += 1
                    self.block_paths.append([50, 0, 0, 0])  # go right
                    if self.debug_mode:
                        print("right")
                if (self.target[1] - self.imaginary_location[1]) < 0 :
                    self.imaginary_location[1] -= 1
                    self.block_paths.append([0, 50, 0, 0])  # go left
                    if self.debug_mode:
                        print("left")
            # update delta
            delta = abs(self.target[0] - self.imaginary_location[0]) + abs(self.target[1] - self.imaginary_location[1])
            ########## check fail ###########
            if fail_counter >= fail_limit:
                fail_counter = 0 # reset counter
                if hard_fail:
                    self.path_finder_fail = True
                    break
                # not void 인 타일 아무거나로 이동해라 right up left순서로 찾기
                if self.is_not_void(self.imaginary_location[0],self.imaginary_location[1] + 1) :
                    self.imaginary_location[1] += 1
                    self.block_paths.append([50, 0, 0, 0])  # go right
                    if self.debug_mode:
                        print("right")
                elif self.is_not_void(self.imaginary_location[0] - 1,self.imaginary_location[1]):
                    self.imaginary_location[0] -= 1
                    self.block_paths.append([0, 0, 0, 50])  # go up
                    if self.debug_mode:
                        print("up")
                elif self.is_not_void(self.imaginary_location[0],self.imaginary_location[1] - 1):
                    self.imaginary_location[1] -= 1
                    self.block_paths.append([0, 50, 0, 0])  # go left
                    if self.debug_mode:
                        print("left")

                hard_fail = True


            ########## find path ###########



        # last one step
        if (self.target[1] - self.imaginary_location[1]) > 0:
            self.block_paths.append([50, 0, 0, 0])  # go
        elif (self.target[1] - self.imaginary_location[1]) < 0:
            self.block_paths.append([0, 50, 0, 0])  # go
        elif (self.target[0] - self.imaginary_location[0]) > 0:
            self.block_paths.append([0, 0, 50, 0])  # go
        elif (self.target[0] - self.imaginary_location[0]) < 0:
            self.block_paths.append([0, 0, 0, 50])  # go

        if self.debug_mode:
            print(self.block_paths)

        return False, 0

    def list_compare(self,list_a,list_b):
        k = len(list_a)
        for i in range(k):
            if not (list_a[i]==list_b[i]):
                return False
        return True
    def update_move(self): # block_paths에 나온대로 움직이면 됨
        '''
        if block path is empty => return True (end)

        else: block path is not empty
        get block_path[0]
        move accordingly, and increment/decrement block path
        if it becomes [0,0] => remove 0th one
        return False


        '''
        # 일단 한칸 앞으로는 항상 가야함 [+x, -x, +y, -y]의 amount로 저장해두기 right lefft down up

        if self.path_finder_fail:# path finder가 fail했을 경우 그냥 다이렉트로 간다
            return True


        if self.block_paths == []:
            return True

        move = self.block_paths[0]
        if move[0]>0: #
            self.moving_X += self.move_speed
            self.block_paths[0][0] -= self.move_speed
        elif move[1]>0:
            self.moving_X -= self.move_speed
            self.block_paths[0][1] -= self.move_speed
        elif move[2]>0:
            self.moving_Y += self.move_speed
            self.block_paths[0][2] -= self.move_speed
        elif move[3]>0:
            self.moving_Y -= self.move_speed
            self.block_paths[0][3] -= self.move_speed

        if self.list_compare( self.block_paths[0], [0,0,0,0]):
            # delete the block path
            self.block_paths.pop(0)
        return False

        #
        # # update direction following the bridges and finish when reaching goal tile
        # # self.moving_X += 1
        # self.moving_Y -= 1
        #
        # if self.moving_Y < -100: # end of animation when block moves is gone
        #     return True
        # return False


    def animate_draw(self,screen):
        global top_down_player
        flag = self.update_move()

        for i in range(7):
            for j in range(7):
                if self.map[i][j][0]=='fight':
                    if self.break_limit:  # boss fight
                        screen.blit(self.image_dict['boss_fight'], (self.map_X + j*self.side_length - self.moving_X, self.map_Y_level + self.side_length*i - self.moving_Y))
                        continue
                screen.blit(self.image_dict[self.map[i][j][0]], (self.map_X + j*self.side_length - self.moving_X, self.map_Y_level + self.side_length*i - self.moving_Y))


        screen.blit(top_down_player,(self.map_X + 3 * self.side_length, self.map_Y_level + self.side_length * 6))
        return flag


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



        return True

    def print_map(self):
        for tttt in range(7):
            print(self.map[tttt])

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
                        # print("current map tile choice: "+self.map[c][r])
                        self.update_target([c,r])
                        return True, map_tile_name , 6-c # is_valid, which_event, depth = 6-c
        return False, False , 0
