import numpy as np
import math


def pos1_to_pos2(x, h, w):
    row = x // w
    col = x % w
    return [row, col]


def pos2_to_pos1(x2, h, w):
    return x2[0] * w + x2[1]


def create_random_state(h, w):
    t = np.arange(h * w)
    np.random.shuffle(t)
    return [list(t), 0, f_obj(list(t), h, w), []]


def insert_state_tree(tr, nv, parent):
    nd = find_node(tr, parent[0])
    if nd is None:
        return None
    nd[-1].append(nv)
    return tr


def get_successors(t, h, w):
    ret = []
    pos_1d = t.index(0)
    pos_2d = pos1_to_pos2(pos_1d, h, w)
    if pos_2d[0] > 0:
        nv = t.copy()
        aux = nv[pos2_to_pos1([pos_2d[0] - 1, pos_2d[1]], h, w)]
        nv[pos2_to_pos1([pos_2d[0] - 1, pos_2d[1]], h, w)] = 0
        nv[pos_1d] = aux
        ret.append(nv)

    if pos_2d[1] > 0:
        nv = t.copy()
        aux = nv[pos2_to_pos1([pos_2d[0], pos_2d[1] - 1], h, w)]
        nv[pos2_to_pos1([pos_2d[0], pos_2d[1] - 1], h, w)] = 0
        nv[pos_1d] = aux
        ret.append(nv)

    if pos_2d[0] < h - 1:
        nv = t.copy()
        aux = nv[pos2_to_pos1([pos_2d[0] + 1, pos_2d[1]], h, w)]
        nv[pos2_to_pos1([pos_2d[0] + 1, pos_2d[1]], h, w)] = 0
        nv[pos_1d] = aux
        ret.append(nv)

    if pos_2d[1] < w - 1:
        nv = t.copy()
        aux = nv[pos2_to_pos1([pos_2d[0], pos_2d[1] + 1], h, w)]
        nv[pos2_to_pos1([pos_2d[0], pos_2d[1] + 1], h, w)] = 0
        nv[pos_1d] = aux
        ret.append(nv)

    return ret


def expand_tree(tr, n, h, w):
    if n == 0:
        return tr
    suc = get_successors(tr[0], h, w)
    for s in suc:
        tr = insert_state_tree(tr, expand_tree([s, 0, f_obj(s, h, w), []], n - 1, h, w), tr)
    return tr


def count_nodes(tr):
    ret = 0
    if len(tr) > 0:
        for t in tr[-1]:
            ret += count_nodes(t)
        return (1 + ret)
    return ret


def count_leaves(tr):
    ret = 0
    if len(tr) > 0:
        if len(tr[-1]) == 0:
            ret += 1
        for t in tr[-1]:
            ret += count_leaves(t)
        return (ret)
    return ret


def show_board(b, cur_d, h, w):
    print('[%4d]-------------------------------' % cur_d)
    for ih in range(h):
        for iw in range(w):
            print('%d\t' % b[ih * w + iw], end='')
        print('')
    print('-------------------------------------')


def show_tree(tr, cur_d, h, w):
    if len(tr) == 0:
        return
    show_board(tr[0], cur_d, h, w)
    for t in tr[-1]:
        show_tree(t, cur_d + 1, h, w)


def find_node(tr, id):
    if len(tr) == 0:
        return None
    if tr[0] == id:
        return tr
    for t in tr[-1]:
        aux = find_node(t, id)
        if aux is not None:
            return aux
    return None


def is_final_board(b, h, w):
    aux = list(np.arange(1, h * w))
    aux.append(0)
    return b == aux


def f_obj(b, h, w):
    goal = list(np.arange(1, h * w))
    goal.append(0)
    j = 0
    for p in goal:
        g2 = pos1_to_pos2(goal.index(p), h, w)
        b2 = pos1_to_pos2(b.index(p), h, w)
        j += np.sum(np.abs(np.asarray(g2) - np.asarray(b2)))
    return j


def get_father(tr, st):
    if len(tr) == 0:
        return None
    for sun in tr[-1]:
        if sun[0] == st[0]:
            return tr

    for sun in tr[-1]:
        aux = get_father(sun, st)
        if aux is not None:
            return aux

    return None


def minimax(tr, d, max_player, h, w):
    if d == 0 or len(tr[-1]) == 0:
        return tr, f_obj(tr[0], h, w)

    ret = math.inf * pow(-1, max_player)
    ret_nd = tr
    for s in tr[-1]:
        aux, val = minimax(s, d - 1, not max_player, h, w)
        if max_player:
            if val > ret:
                ret = val
                ret_nd = aux
        else:
            if val < ret:
                ret = val
                ret_nd = aux

    return ret_nd, ret


def minimax_alpha_beta(tr, d, max_player, alpha, beta, h, w):
    if d == 0 or len(tr[-1]) == 0:
        return tr, f_obj(tr[0], h, w)

    ret = math.inf * pow(-1, max_player)
    ret_nd = tr
    for s in tr[-1]:
        aux, val = minimax_alpha_beta(s, d - 1, not max_player, alpha, beta, h, w)
        if max_player:
            if val > ret:
                ret = val
                ret_nd = aux
            alpha = max(alpha, ret)
        else:
            if val < ret:
                ret = val
                ret_nd = aux
            beta = min(beta, ret)
        if beta <= alpha:
            break

    return ret_nd, ret


width = 3
height = 3

initial_board = [1, 5, 3, 0, 2, 4, 6, 7, 8]
initial_state = [initial_board, 0, f_obj(initial_board, height, width), []]
# initial_state = create_random_state(height, width)


initial_state = expand_tree(initial_state, 5, height, width)

show_tree(initial_state, 0, height, width)

print('Total nodes: %d' % count_nodes(initial_state))

depth_tree = 5

choice, value = minimax(initial_state, depth_tree, True, height, width)
# choice, value = minimax_alpha_beta(initial_state_alpha_beta, depth_tree, True, -math.inf, math.inf, height, width)

show_board(choice[0], value, height, width)