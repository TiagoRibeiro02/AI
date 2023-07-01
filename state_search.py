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
    return [list(t), 0, f_obj(list(t), h, w), []]


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
        for t in tr[-1]:
            ret += count_nodes(t)
        return(1 + ret)
    return ret


def count_leaves(tr):
    ret = 0
    if len(tr) > 0:
        if len(tr[-1]) == 0:
            ret += 1
        for t in tr[-1]:
            ret += count_leaves(t)
        return(ret)
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
        show_tree(t, cur_d+1, h, w)


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
    aux = list(np.arange(1, h*w))
    aux.append(0)
    return b == aux


def pos1_to_pos2(x, h, w):
    row = x // w
    col = x % w
    return [row, col]


def f_obj(b, h, w):
    goal = list(np.arange(1, h*w))
    goal.append(0)
    j = 0
    for p in goal:
        g2 = pos1_to_pos2(goal.index(p), h, w)
        b2 = pos1_to_pos2(b.index(p), h, w)
        j += np.sum(np.abs(np.asarray(g2)-np.asarray(b2)))
    return j

def f_obj2(b, h, w):
    goal = list(np.arange(1, h * w))
    goal.append(0)
    return np.sum(np.asarray(b) != np.asarray(goal))




def successors(tr, st, h, w):
    suc = get_successors(st[0], h, w)
    for b in suc:
        aux = find_node(tr, b)
        if aux is None:
            st[-1].append([b, st[1]+1, f_obj(b, h, w) + st[1]+1, []])
    return st


def board_in_list(b, lst):
    return b in lst


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


def get_path(tr, st):
    path = [st[0]]
    while True:
        fa = get_father(tr, st)
        if fa is not None:
            path.insert(0, fa[0])
            st = fa
            continue
        break
    return path


def show_path(path, h, w):
    print('PATH TO SOLUTION:')
    cnt = 0
    for b in path:
        show_board(b, cnt, h, w)
        cnt += 1


def insert_sorted(lst, nv):
    index = len(lst)
    for i in range(len(lst)):
        if lst[i][2] > nv[2]:
            index = i
            break

    if index == len(lst):
        return lst[:index] + [nv]
    return lst[:index] + [nv] + lst[index:]



def search(st, h, w, type_search):
    # type_search: 1=breadth first; 2=depth first; 3=A*
    done = []
    todo = [st]
    while len(todo) > 0:
        cur = todo.pop(0)
        if is_final_board(cur[0], h, w):
            return st, cur

        cur = successors(st, cur, h, w)
        for s in cur[-1]:
            if board_in_list(s[0], done):
                continue
            if type_search == 1:
                todo.insert(-1, s)
            elif type_search == 2:
                todo.insert(0, s)
            else:
                todo = insert_sorted(todo, s)

        done.insert(-1, cur[0])
        print('f()=%d=(g()=%d + h()=%d), done=%d, todo=%d' % (cur[2], cur[1], f_obj(cur[0], h, w), len(done), len(todo)))
    return st, None


width = 3
height = 3

initial_board = [1, 5, 3, 0, 2, 4, 6, 7, 8]
initial_state = [initial_board, 0, f_obj(initial_board, height, width), []]
initial_state = create_random_state(height, width)

type_search = 3  # 1: BFS, 2: DFS, 3: A*
initial_state, result = search(initial_state, height, width, type_search)


#show_tree(initial_state, 0, height, width)

if result is not None:
    path = get_path(initial_state, result)
    show_path(path, height, width)

print('Done. Total states generated: %d. Total paths generated: %d' % (count_nodes(initial_state), count_leaves(initial_state)))

#st = expand_tree(st, 2, height, width)

#show_tree(st, 0, height, width)

#print('Total nodes: %d' % count_nodes(st))

