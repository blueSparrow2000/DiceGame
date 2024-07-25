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


def hihi():
    print(x)
x = 10
hihi()
