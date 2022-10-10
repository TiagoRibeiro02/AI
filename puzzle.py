import numpy as np

L=4
W=4

def create_random_state(h, w):
    t = np.arange(h * w)
    np.random.shuffle(t)
    return [list(t), []]

def show_state(state, L, W):
    for i in range(L*W):
        if i % L == 0 and i > 0:
            print("")
        print(str(state[i]) + " ", end = "")

def valid_state(state, L, W):
    valid =0
    for i in range(len(state)):
        if state.count(i) != 1:
            valid = -1
    if len(state) != L*W or valid == -1:
        print("Invalid State")

    else:
        return state

def pos1D_to_pos2D(x,l,w):
    row = x // w
    col = x % w
    return [row, col]

def pos2D_to_pos1D(x2,l,w):
    return x2[0] * w + x2[1]


def successors(state, h, w):
    pos_0 = state.index(0)
    pos0_2D = pos1D_to_pos2D(pos_0, h, w)
    suc = []
    if pos0_2D[0] != 0:  # mover para cima
        mv = state.copy()
        aux = state[pos2D_to_pos1D([pos0_2D[0] - 1, pos0_2D[1]], h, w)]
        mv[pos_0] = aux
        mv[pos2D_to_pos1D((pos0_2D[0] - 1, pos0_2D[1]), h, w)] = 0
        suc.append(mv)
    if pos0_2D[1] != w - 1:  # mover para a direita
        mv = state.copy()
        aux = state[pos2D_to_pos1D([pos0_2D[0], pos0_2D[1] + 1], h, w)]
        mv[pos_0] = aux
        mv[pos2D_to_pos1D((pos0_2D[0], pos0_2D[1] + 1), h, w)] = 0
        suc.append(mv)
    if pos0_2D[0] != h - 1:  # mover para baixo

        mv = state.copy()
        aux = state[pos2D_to_pos1D([pos0_2D[0] + 1, pos0_2D[1]], h, w)]
        mv[pos_0] = aux
        mv[pos2D_to_pos1D((pos0_2D[0] + 1, pos0_2D[1]), h, w)] = 0
        suc.append(mv)
    if pos0_2D[1] != 0:  # mover para esquerda
        mv = state.copy()
        aux = state[pos2D_to_pos1D([pos0_2D[0], pos0_2D[1] - 1], h, w)]
        mv[pos_0] = aux
        mv[pos2D_to_pos1D((pos0_2D[0], pos0_2D[1] - 1), h, w)] = 0
        suc.append(mv)

    return suc

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
def insert_tree(Tree, New, Father):
    nd = find_node(Tree, Father[0])
    if nd is None:
        return None
    nd[1].append(New)
    return Tree

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
        show_tree(t, cur_d + 1, h, w)

def count_tree(Tree):
    ret = 0
    if len(Tree) > 0:
        for t in Tree[1]:
            ret += count_tree(t)
        return (1 + ret)
    return ret
def expand_tree(tr, n, h, w):
    if n == 0:
        return tr
    suc = successors(tr[0], h, w)
    for s in suc:
        tr = insert_tree(tr, expand_tree([s, []], n-1, h, w), tr)
    return tr

st = create_random_state(L, W)

st = expand_tree(st, 2, L, W)

show_tree(st, 0, L, W)

print('Total nodes: %d' % count_tree(st))


