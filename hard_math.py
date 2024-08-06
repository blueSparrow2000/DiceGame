import numpy.random as np
import math
import copy
import random

def fast_norm_pdf(x, mean, sd): # that differs by constant multiple (about 2*pi = 6 times larger)
    var = sd**2
    num = math.exp(-(x-mean)**2/(2*var))
    return num / sd

def weight(current_depth, mean_depth, spreadness):
    my_prob = fast_norm_pdf(current_depth, mean_depth, spreadness)
    return my_prob

def normalizer(this_list):
    ndigit = 3
    total = sum(this_list)

    result = [round(x / total, ndigit) for x in this_list]
    if sum(result)>1:
        delta = sum(result) - 1 # > 0

        max_pivot = 0
        for k in range(len(result)):
            if result[k] > result[max_pivot]:
                max_pivot = k
        if result[max_pivot] >= delta:
            result[max_pivot] -= delta # subtract margin

        else:
            print("Max prob is smaller than the total prob! this is problematic!!")
            for k in range(len(result)):
                cur_prob = result[k]
                if cur_prob > 0:
                    if delta >= cur_prob: # large delta
                        result[k] = 0
                        delta -= cur_prob
                    else: # remaining delta
                        result[k] -= delta
                        delta = 0


    else:
        delta = 1 - sum(result)
        result[0] += delta # add margin
    return result

def choice_maker(enemy_list, probs):
    max_capacity = 3
    empty_threshold = 0.35
    result = []
    for i in range(max_capacity):
        if random.random() < empty_threshold: # pass
            continue
        choice = np.choice(enemy_list, size = 1, p = probs)
        result.append(str(choice[0]))
    if result == []: # empty => choose at least one!
        choice = np.choice(enemy_list, size = 1, p = probs)
        result.append(str(choice[0]))
    return result



def get_request(current_depth,current_enemies,dist_params):
    d = current_depth
    player_depth = abs(d)  # 0 to -100
    # current_enemies = ['mob', 'fragment', 'lenz', 'mine', 'embryo', 'norm', 'scout', 'observer', 'sentinel']
    # dist_params = [[25, 8.6], [30, 6.8], [50, 6.2], [50, 6.2], [80, 4.4], [80, 4.4], [73, 6.3], [80, 4.4],
    #                [80, 4.4]]

    probs = []
    for i in range(len(current_enemies)):
        cur_param = dist_params[i]
        probs.append(weight(player_depth, cur_param[0], cur_param[1]))

    probs = normalizer(probs)
    enemy_request = choice_maker(current_enemies, probs)

    print('%4d: ' % d, enemy_request)

    return enemy_request

# get_request(-74,['mob', 'fragment', 'lenz', 'mine', 'embryo', 'norm', 'scout', 'observer', 'sentinel'], [[25, 8.6] , [30, 6.8],[50, 6.2],[50, 6.2],[80,5.4],[80,5.4],[73,6.3],[80,5.4],[80,5.4] ])

######################################## TEST ####################################################
# depths = [-i*5 for i in range(20)]
# for d in depths:
#     player_depth =abs(d) # 0 to -100
#     current_enemies = ['mob', 'fragment', 'lenz', 'mine', 'embryo', 'norm', 'scout', 'observer', 'sentinel']
#     dist_params = [[25, 8.6] , [30, 6.8],[50, 6.2],[50, 6.2],[80,5.4],[80,5.4],[73,6.3],[80,5.4],[80,5.4] ]
#
#
#     probs = []
#     for i in range(len(current_enemies)):
#         cur_param = dist_params[i]
#         probs.append(weight(player_depth, cur_param[0] , cur_param[1]))
#
#     probs = normalizer(probs)
#     enemy_request = choice_maker(current_enemies, probs)
#
#     print('%4d: '%d,enemy_request)


