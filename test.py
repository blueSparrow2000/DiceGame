from util import *
import copy
# map = [['void' for x in range(7)] for y in range(7)]
# must_contain_at_least_one = [[False for x in range(7)] for y in range(7)]
# map[0][3] = 'fight'
#
# # insert at-least-contain-one's in neighbors islands
# for c in range(7):
#     for r in range(7):
#         if map[c][r]=='fight':
#             for y in range(-1, 2):
#                 for x in range(-1, 2):
#                     if 0 <= c + y <= 6 and 0 <= r + x <= 6:  # must be inside the map
#                         if x == 0 or y == 0:  # middle parts
#                             must_contain_at_least_one[c + y][r + x] = True  # 나중에 검사할때 하나라도 True인게 있으면 됨
#
# for i in range(7):
#     print(must_contain_at_least_one[i])

# def list_compare(list_a, list_b):
#     k = len(list_a)
#     for i in range(k):
#         if not (list_a[i] == list_b[i]):
#             return False
#     return True
# a = [0,0,0,1]
# b = [0,0,0,0]
# print(list_compare(a,b))
#
#
# blocks = [[[0,0],'Empty'] , [[0,1],'Defence'], [[1,0],'Attack'], [[1,1],'Skill']]
# temp = copy.deepcopy(blocks)
# pcs = [[0.9,0.9], [1,1], [1.1,1.1]]
# side_len_half = 0.5
#
# for pc in pcs:
#     for i in range(len(blocks)):
#         if check_inside_button(pc, blocks[i][0], side_len_half):
#             # add tile
#             temp[i] = [blocks[i][0],'Used']
#
# print(temp)





# for x in [0, -5, -74, -99, -100, -101, -199, -200, -201, -298, -299]:
#     y = abs(x)//100 + 1
#
#     print('%4d'%x, y, "  |%d"%(- (abs(x)%100) ))
#

# with open("foo.txt", "w") as f:
#     information = ["%d sentence "%i for i in range(10)]
#     for info in information:
#         f.write(info+"\n")



# dict_in_str = "{'Attack': 9, 'Regen': 0, 'Defence': 4, 'Skill': 4, 'Joker': 0, 'Karma': 0, 'Empty': 47}"
#
# def get_permanent_tile_dict(dict_in_str):
#     permanent_tile_dict = dict()
#     dict_in_str = dict_in_str[1:-1]
#     tile_info_list = dict_in_str.split(",")
#     for tile_info in tile_info_list:
#         refined_info = tile_info.split(":")
#         # print(refined_info)
#         tile_name = refined_info[0].strip()[1:-1]
#         tile_amount = int(refined_info[1].strip())
#         permanent_tile_dict[tile_name] = tile_amount
#
#     return permanent_tile_dict
#
# print(get_permanent_tile_dict(dict_in_str))
#
#
# list_in_str = "['martial_art', 'head_start', 'sword_storm', 'self_defence', 'Antifragile', 'Excaliber']"
# def string_to_list(list_in_str):
#     result_list = []
#     dict_in_str = list_in_str[1:-1]
#     tile_info_list = dict_in_str.split(",")
#     for tile_info in tile_info_list:
#         refined_info = tile_info.strip()[1:-1]
#         result_list.append(refined_info)
#     return result_list
#
#
#
# print(string_to_list(list_in_str))
#
#
# fixed_tile_info_str = "{ }"
#
# def get_fixed_tile_dict(dict_in_str):
#     permanent_tile_dict = dict()
#     dict_in_str = dict_in_str[1:-1]
#     tile_info_list = dict_in_str.split(",")
#     for tile_info in tile_info_list:
#         refined_info = tile_info.split(":")
#         # print(refined_info)
#         tile_amount = int(refined_info[0])
#         tile_name = refined_info[1].strip()[1:-1]
#
#         permanent_tile_dict[tile_amount] = tile_name
#
#     return permanent_tile_dict
#
# print(get_fixed_tile_dict(fixed_tile_info_str))


# sss = " "
# xx = sss.strip()
# print(xx)
# print(len(xx))

# def str_to_bool(candidate):
#     if candidate=='True':
#         return True
#     elif candidate=='False':
#         return False
#     else:
#         print("ERROR! Input Not boolean!")
#         return False
#
# print(str_to_bool('False'))
#
#
# list_in_str = "[0, 3]"
# def string_to_int_list(list_in_str):
#     result_list = []
#     dict_in_str = list_in_str[1:-1]
#     tile_info_list = dict_in_str.split(",")
#     for tile_info in tile_info_list:
#         refined_info = int(tile_info.strip())
#         result_list.append(refined_info)
#     return result_list
#
# print(string_to_int_list(list_in_str))

# def try_cast_int(candidate):
#     try:
#         return int(candidate)
#     except ValueError:
#         # print("not int")
#         return candidate
#
# depthsss = "LIMIT" #-1#
# print(try_cast_int(depthsss))
