import numpy as np


def pos1_to_pos2(x, h, w):
    row = x // w
    col = x % w
    return [row, col]


def pos2_to_pos1(x2, h, w):
    return x2[0] * w + x2[1]

def create_random_state(h, w):
    t = np.arange(h * w)
    np.random.shuffle(t)
    return [list(t), []]


def insert_state_tree(tr, nv, parent):
    nd = find_node(tr, parent[0])
    if nd is None:
        return None
    nd[1].append(nv)
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
        tr = insert_state_tree(tr, expand_tree([s, []], n-1, h, w), tr)
    return tr



def count_nodes(tr):
    ret = 0
    if len(tr) > 0:
        for t in tr[1]:
            ret += count_nodes(t)
        return(1 + ret)
    return ret



def show_tree(tr, cur_d, h, w):
    if len(tr) == 0:
        return
    print('[%d]-------------------------------------' % cur_d)
    for ih in range(h):
        for iw in range(w):
            print('%d\t' % tr[0][ih * w + iw], end='')
        print('')
    print('-------------------------------------')
    for t in tr[1]:
        show_tree(t, cur_d +1, h, w)



def find_node(tr, id):
    if len(tr) == 0:
        return None
    if tr[0] == id:
        return tr
    for t in tr[1]:
        aux = find_node(t, id)
        if aux is not None:
            return aux
    return None



width = 4
height = 4

st = create_random_state(height, width)

st = expand_tree(st, 2, height, width)

show_tree(st, 0, height, width)

print('Total nodes: %d' % count_nodes(st))