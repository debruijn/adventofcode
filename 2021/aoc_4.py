import numpy as np

with open('aoc_4_data1') as f:
    data_draws = f.readlines()

with open('aoc_4_data2') as f:
    data_boards = f.readlines()

data_boards = [[int(y) for y in x.split(' ') if len(y) > 0] for x in data_boards if x != '\n']


class Board:

    def __init__(self, raw_board):

        self.board = np.array(raw_board)
        self.checked = np.zeros_like(self.board)
        self.skip = False

    def check_rows(self):
        return True if any(self.checked.all(axis=1)) else False

    def check_cols(self):
        return True if any(self.checked.all(axis=0)) else False

    def check(self):
        if not self.skip:
            return True if self.check_rows() or self.check_cols() else False
        else:
            return False

    def mark_num(self, num):
        self.checked[np.where(self.board == num)] = 1

    def sum_unmarked(self):
        return self.board[np.where(1 - self.checked)].sum()

    def score(self, num):
        self.set_fully_checked()
        return self.sum_unmarked() * num

    def apply_draw(self, num):
        self.mark_num(num)
        return self.check()

    def set_fully_checked(self):
        self.skip = True


boards_raw = []
for i in range(int(np.ceil(len(data_boards)/5))):
    boards_raw.append(data_boards[5*i:5*(i+1)])

boards = [Board(board_raw) for board_raw in boards_raw]

draws = [int(x) for x in data_draws[0].split(',')]

done = False
for draw in draws:
    if not done:
        status = [x.apply_draw(draw) for x in boards]
        if any(status):
            print(f'Score first part: {boards[np.where(status)[0].item(0)].score(draw)}, draw: {draw}')
            done = True


# part 2

boards = [Board(board_raw) for board_raw in boards_raw]
for draw in draws:
    status = [x.apply_draw(draw) for x in boards]
    if any(status):
        indices = np.where(status)[0]
        for index in indices:
            print(f'Score: {boards[index.item(0)].score(draw)}, draw: {draw}, index: {index.item(0)}')

print(f'Score second part: see above')  # TODO: better output
