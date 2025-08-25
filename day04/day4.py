with open("day4_input.txt", newline='\n') as f:
    reader = f.read().splitlines()
    data = list()
    for line in reader:
        if len(line) > 0:
            data.append(line)

draw_order = list(map(int, data[0].split(',')))
grid_size = 5
bingo_boards = list()
for i in range(1, len(data), grid_size):
    board = list()
    for j in range(grid_size):
        board.append(list(map(int, filter(lambda n: n, data[i + j].split(' ')))))
    bingo_boards.append(board)

def print_array(arr):
    for row in arr:
        print(row)

def cache_number_indices(bingo_board):
    res = dict()
    for i in range(grid_size):
        for j in range(grid_size):
            res[bingo_board[i][j]] = (i, j)
    return res

def check_rows(marking_board):
    for i in range(grid_size):
        if sum(marking_board[i]) == grid_size:
            return True
    return False

def check_cols(marking_board):
    for j in range(grid_size):
        if sum([row[j] for row in marking_board]) == grid_size:
            return True
    return False

def get_unmarked_numbers(bingo_board, marking_board):
    res = list()
    for i in range(grid_size):
        for j in range(grid_size):
            if not marking_board[i][j]:
                res.append(bingo_board[i][j])
    return res

def part1(bingo_boards, draw_order):
    marking_boards = [[[0 for j in range(grid_size)] for i in range(grid_size)] for k in range(len(bingo_boards))]
    bingo_boards_cached = [cache_number_indices(board) for board in bingo_boards]
    w_num, w_board = 0, 0
    break_flag = False
    for num in draw_order:
        if break_flag:
            break
        for k in range(len(bingo_boards)):
            if break_flag:
                break
            if num in bingo_boards_cached[k]:
                i, j = bingo_boards_cached[k][num]
                marking_boards[k][i][j] = 1
                if check_rows(marking_boards[k]) or check_cols(marking_boards[k]):
                    w_num = num
                    w_board = k
                    break_flag = True
    unmarked_nums = get_unmarked_numbers(bingo_boards[w_board], marking_boards[w_board])
    return sum(unmarked_nums) * w_num

def part2(bingo_boards, draw_order):
    marking_boards = [[[0 for j in range(grid_size)] for i in range(grid_size)] for k in range(len(bingo_boards))]
    bingo_boards_left = set(range(len(bingo_boards)))
    bingo_boards_cached = [cache_number_indices(board) for board in bingo_boards]
    l_num, l_board = 0, 0
    for num in draw_order:
        if len(bingo_boards_left) == 0:
            break
        for k in range(len(bingo_boards)):
            if len(bingo_boards_left) == 0:
                break
            elif k not in bingo_boards_left:
                continue
            if num in bingo_boards_cached[k]:
                i, j = bingo_boards_cached[k][num]
                marking_boards[k][i][j] = 1
                if check_rows(marking_boards[k]) or check_cols(marking_boards[k]):
                    bingo_boards_left.remove(k)
                    if len(bingo_boards_left) == 0:
                        l_num = num
                        l_board = k
    unmarked_nums = get_unmarked_numbers(bingo_boards[l_board], marking_boards[l_board])
    return sum(unmarked_nums) * l_num

print(f'Part 1: {part1(bingo_boards, draw_order)}')
print(f'Part 2: {part2(bingo_boards, draw_order)}')
