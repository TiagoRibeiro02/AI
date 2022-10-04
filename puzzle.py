import random

L=4
W=4

def create_random_state(L, W):
    state = []
    for n in range(L*W):
        state.append(n)
    random.shuffle(state)
    return state

def show_state(state, L, W):
    for i in range(L*W):
        if i % L == 0 and i > 0:
            print("")
        print(str(state[i]) + " ", end = "")

def valid_state(state, L, W):
    for i in range(len(state)):
        if state.count(i) != 1:
            valid = -1
    if len(state) != L*W or valid == -1:
        print("Invalid State")

    else:
        return state

def pos1D_to_2D(p,L,W):
    return ([p//W, p%W])

def pos2d_to_1D(p,L,W):
    return (p[0]*W + p[1])

def sucessors(state, L, W):
    pos = state.index(0)
    pos_2d = pos1D_to_2D(pos, L, W)
    suc = []
    if(pos_2d[0] != 0): #norte
        nv = state.copy()
        aux = state[pos2d_to_1D((pos_2d[0]-1, pos_2d[1]), L, W)]
        nv[pos] = aux
        nv[pos2d_to_1D((pos_2d[0]-1, pos_2d[1]), L, W)] = 0
        suc.append(nv)
    if (pos_2d[0] != L-1): #sul
        nv = state.copy()
        aux = state[pos2d_to_1D((pos_2d[0] + 1, pos_2d[1]), L, W)]
        nv[pos] = aux
        nv[pos2d_to_1D((pos_2d[0] + 1, pos_2d[1]), L, W)] = 0
        suc.append(nv)
    if (pos_2d[1] != 0): #direita
        nv = state.copy()
        aux = state[pos2d_to_1D((pos_2d[0], pos_2d[1] + 1), L, W)]
        nv[pos] = aux
        nv[pos2d_to_1D((pos_2d[0], pos_2d[1] + 1), L, W)] = 0
        suc.append(nv)
    if (pos_2d[1] != W-1): #esquerda
        nv = state.copy()
        aux = state[pos2d_to_1D((pos_2d[0], pos_2d[1] - 1), L, W)]
        nv[pos] = aux
        nv[pos2d_to_1D((pos_2d[0], pos_2d[1] - 1), L, W)] = 0
        suc.append(nv)

    return suc

def find_node (Tree, Tab):
    if len(Tree) == 0:
        return None
    if Tree[0] == Tab: ##Tree[0] = tabuleiro
        return Tab
    for t in Tree[1]: ##Tree[1] = lista dos filhos
        aux = find_node(Tree, Tab)
        if aux is not None:
            return aux
    return None
def insert_tree(Tree, New, Father):
    nd = find_node(Tree, Father)
    if nd is None:
        return nd
    nd[1].insert(New, -1)
    return Tree
def show_tree(Tree, L, W):
    if len(Tree) == 0:
        return
    show_state(Tree[0], L, W)
    for t in Tree[1]:
        show_tree(t)
def count_tree(Tree):
    ret = 0
    if len(Tree) > 0:
        for t in Tree[1]:
            ret += count_tree(t)
        return (1 + ret)
    return ret
def expand_tree(Tree, N):


state = create_random_state(L, W)
show_state(state, L, W)
print("\nsucessores", sucessors(state, L, W))


