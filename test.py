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
#
# for i in range(10):
#     if i==1:
#         continue
#     print(i)
x = None
if x is not None:
    print("x")
