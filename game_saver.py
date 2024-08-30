from variables import *
import os, sys
from player import Player
from board import *
from util import *
from skill_book import *
from relic import *
from map_logic import Map
from area_ruin import generate_relic_by_class_name

# f = open("./Tutorial.txt", 'r')
# lines = f.readlines()
#
# LocationName = ""
# index = 1
# request1 = ""
# request2 = ""
#
# for line in lines:
#     line = line.strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
#     content = line.split(',')
#     if (len(content) == 1): #this is a name
#         words = content[0].split('-')
#         if (len(words)==3):
#             index = 1 # reset index when meet other location name
#             LocationName = words[0].strip()
#             request1 = words[1].strip()
#             request2 = words[2].strip()
#     if (len(content)==2):
#         # request:['gun','random']
#         print("'%s%s':{row:%s, col:%s, request:['%s','%s']},"%(LocationName,index,content[1],content[0], request1,request2)) # switch row col
#         index+=1
#
# f.close()


'''
플레이어 기본 최대체력 및 현재 체력
플레이어 시드

permanent 타일 리스트
fixed 타일 리스트
planar figure 정보 


유물 리스트 (다시 만들어줘야 함)
축복 및 저주 리스트 (다시 적용시켜줘야함)
현재 깊이 및 타일 배치 정보


기본 스킬 북
스킬 종류 (스킬 바뀔 수 있음)


'''

GAME_SAVE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))+"/saved_game/"

def save_game(slot_num, player):
    print("Saved game on slot %d"%slot_num)
    full_path = os.path.join(GAME_SAVE_PATH, 'slot%s.txt' % slot_num)

    information = [
        ################################################# PLAYER VARIABLES ########################################################
        # 축복/저주 효과는 간접적으로 저장/ 로드됨 (그 효과의 결과들만 저장)
        player.my_name,  # 이것만 알면 스킬북은 로딩에서 생성하면 된다
        player.my_seed,  # 시드 저장
        player.max_health,
        player.health,
        player.current_skills,  # 현재 스킬 리스트 이거 저장 후 덮어씌워야 함

        ### game variables
        player.current_depth,
        player.golds,
        player.items,
        player.killed_enemies,
        player.boss_stage,
        player.killed_watcher,

        ################################################# BOARD VARIABLES ########################################################
        # player.board
        # 보드 리셋주기
        # 보드 리셔플 여부
        # 보드사이즈
        # 고정타일
        # 전개도가 보드 탈출가능 여부
        # 보드 이레귤러 셰이프 여부
        player.board.planar_figure_idx,

        player.board.board_side_length,

        player.board.permanent_board_dict,

        player.board.board_reset_turn,

        ##################### FIXED TILE ######################
        player.board.permanently_fixed_tiles,
        ##################### FIXED TILE ######################

        player.board.out_of_board_protection,
        player.board.irregular_shape,
        player.board.board_shuffle_every_turn,

        ################################################# RELIC VARIABLES ########################################################
        #player.relics 의 class name들을 리스트로 저장
        [relic.class_name for relic in player.relics]

    ]

    with open(full_path, "w") as f:
        for info in information:
            f.write(str(info) + "\n")


def string_to_list(list_in_str):
    result_list = []
    dict_in_str = list_in_str[1:-1]

    if len(dict_in_str.strip()) == 0: # empty
        return []
    tile_info_list = dict_in_str.split(",")
    for tile_info in tile_info_list:
        refined_info = tile_info.strip()[1:-1]
        result_list.append(refined_info)
    return result_list

def string_to_int_list(list_in_str):
    result_list = []
    dict_in_str = list_in_str[1:-1]
    if len(dict_in_str.strip()) == 0: # empty
        return []
    tile_info_list = dict_in_str.split(",")
    for tile_info in tile_info_list:
        refined_info = int(tile_info.strip())
        result_list.append(refined_info)
    return result_list


def get_fixed_tile_dict(dict_in_str):
    permanent_tile_dict = dict()
    dict_in_str = dict_in_str[1:-1]
    if len(dict_in_str.strip()) == 0: # empty
        return dict()
    tile_info_list = dict_in_str.split(",")
    for tile_info in tile_info_list:
        refined_info = tile_info.split(":")
        # print(refined_info)
        tile_amount = int(refined_info[0])
        tile_name = refined_info[1].strip()[1:-1]

        permanent_tile_dict[tile_amount] = tile_name

    return permanent_tile_dict

def get_permanent_tile_dict(dict_in_str):
    permanent_tile_dict = dict()
    dict_in_str = dict_in_str[1:-1]
    if len(dict_in_str.strip()) == 0: # empty
        return dict()
    tile_info_list = dict_in_str.split(",")
    for tile_info in tile_info_list:
        refined_info = tile_info.split(":")
        # print(refined_info)
        tile_name = refined_info[0].strip()[1:-1]
        tile_amount = int(refined_info[1].strip())
        permanent_tile_dict[tile_name] = tile_amount

    return permanent_tile_dict


def str_to_bool(candidate):
    if candidate=='True':
        return True
    elif candidate=='False':
        return False
    else:
        print("ERROR! Input Not boolean!")
        return candidate


def try_cast_int(candidate):
    try:
        return int(candidate)
    except ValueError:
        # print("not int")
        return candidate

def load_game(slot_num):
    full_path = os.path.join(GAME_SAVE_PATH, 'slot%s.txt' % slot_num)

    information = []
    with open(full_path, "r") as f:
        lines = f.readlines()
        information = [line.strip() for line in lines]# 줄 끝의 줄 바꿈 문자를 제거한다.

    if len(information)==0:
        print("No data is loaded in slot %d"%slot_num)
        return None
    print("Loading game in slot %d"%slot_num)

    character_name = information[0]
    planar_figure_idx = string_to_int_list(information[11])

    ################################################# BOARD VARIABLES ########################################################
    character_skills = character_skill_dictionary[character_name]
    character_tiles = character_tile_dictionary[character_name]
    loaded_board = Board(character_tiles, planar_figure_idx)

    ### board modifications here
    loaded_board_side_length = int(information[12])
    loaded_board.permanent_board_dict = get_permanent_tile_dict(information[13])

    shrinked_amount = 8 - loaded_board_side_length
    for i in range(shrinked_amount):
        loaded_board.permanently_shrink_the_board_by_one()

    loaded_board.board_reset_turn = int(information[14])

    loaded_board.permanently_fixed_tiles = get_fixed_tile_dict(information[15])
    # for loaded_fixed_tile_name in get_fixed_tile_dict(information[15]).values(): # 이미 반영된 결과다
    #     loaded_board.permanently_replace_a_blank_tile_to(loaded_fixed_tile_name)

    loaded_board.out_of_board_protection = str_to_bool(information[16])
    loaded_board.irregular_shape = str_to_bool(information[17])
    loaded_board.board_shuffle_every_turn = str_to_bool(information[18])
    ###


    player = Player(character_name, character_skills, loaded_board)
    ################################################# PLAYER VARIABLES ########################################################
    player.my_seed = int(information[1])
    player.max_health = int(information[2])
    player.health = int(information[3])
    player.current_skills = string_to_list(information[4])
    player.max_num_of_skills = len(player.current_skills)
    player.current_depth = try_cast_int(information[5])
    player.golds = int(information[6])
    player.items = [] # currently none # information[7]
    player.killed_enemies = int(information[8])
    player.boss_stage = int(information[9])
    player.killed_watcher = str_to_bool(information[10])

    ################################################# RELIC VARIABLES ########################################################
    # 리스트로 저장된 클래스 네임들을 다시 불러와서 플레이어가 픽업하게 하기
    #### 주의: 서펀트 하트같은 최대체력 변형하는 유물의 경우 turn off하기 (최대체력은 저주가 반영된 상태의 최종 HP를 바로 불러오기 함)
    # player.pick_up_relic(generate_relic_by_class_name, True) # effect off
    saved_relics = string_to_list(information[19])
    for relic_class_name in saved_relics:
        player.pick_up_relic(generate_relic_by_class_name(relic_class_name), True)


    return player










