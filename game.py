import random

class Block:
    def __init__(self, *args, **kwargs):
        self.value = kwargs.get('value', self._random_block_value())
        self.merged = False

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)

    def _random_block_value(self):
        if random.random() <= 0.1:
            return 4
        else:
            return 2

    def merge(self, block):
        if self.can_merge(block):
            self.value = self.value + block.value
            self.merged = True

    def can_merge(self, block):
        return block.value == self.value and not self.merged

    def reset_merge(self):
        self.merged = False



class Game:
    def __init__(self, *args, **kwargs):
        board = kwargs.get('board')

        if board is None:
            self._initialize_board()
        else:
            self.board = board




    def _add_block(self):
        row, col = self._random_location()
        while self.board[row][col] is not None:
            row, col = self._random_location()
        self.board[row][col] = Block()

    def _initialize_board(self):
        self.board = [[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]
        self._add_block()
        self._add_block()

    def _random_location(self):
        return random.randint(0, 3), random.randint(0, 3)

    def _row_is_empty(self, ind):
        return self.board[ind] == [None, None, None, None]

    def _col_is_empty(self, ind):
        for r in [0,1,2,3]:
            if self.board[r][ind] is not None:
                return False
        return True


    def _reset_blocks(self):
        for r in self.board:
            for c in r:
                if c is not None:
                    c.reset_merge()


    def _move_block_left(self, row, col):
        left_col = col-1
        if col > 0:
            block = self.board[row][col]
            if block is not None:
                left = self.board[row][left_col]
                while not left_col == 0 and left is None:
                    left_col -= 1
                    left = self.board[row][left_col]
                self.board[row][col] = None
                if left is not None:
                    if left.can_merge(block):
                        left.merge(block)
                    else:
                        self.board[row][left_col+1] = block
                else:
                    self.board[row][left_col] = block


    def _shift_row_left(self, ind):
        if not self._row_is_empty(ind):
            for c in [0,1,2,3]:
                self._move_block_left(ind, c)


    def _move_block_right(self, row, col):
        right_col = col+1
        if col < 3:
            block = self.board[row][col]
            if block is not None:
                right = self.board[row][right_col]
                while not right_col == 3 and right is None:
                    right_col += 1
                    right = self.board[row][right_col]
                self.board[row][col] = None
                if right is not None:
                    if right.can_merge(block):
                        right.merge(block)
                    else:
                        self.board[row][right_col-1] = block
                else:
                    self.board[row][right_col] = block


    def _shift_row_right(self, ind):
        if not self._row_is_empty(ind):
            for c in [3, 2, 1, 0]:
                self._move_block_right(ind, c)

    def _move_block_down(self, row, col):
        down_row = row+1
        if row < 3:
            block = self.board[row][col]
            if block is not None:
                down = self.board[down_row][col]
                while not down_row == 3 and down is None:
                    down_row += 1
                    down = self.board[down_row][col]
                self.board[row][col] = None
                if down is not None:
                    if down.can_merge(block):
                        down.merge(block)
                    else:
                        self.board[down_row-1][col] = block
                else:
                    self.board[down_row][col] = block

    def _shift_col_down(self, ind):
        if not self._col_is_empty(ind):
            for r in [3, 2, 1, 0]:
                self._move_block_down(r, ind)


    def _move_block_up(self, row, col):
        up_row = row-1
        if row > 0:
            block = self.board[row][col]
            if block is not None:
                up = self.board[up_row][col]
                while not up_row == 0 and up is None:
                    up_row -= 1
                    up = self.board[up_row][col]
                self.board[row][col] = None
                if up is not None:
                    if up.can_merge(block):
                        up.merge(block)
                    else:
                        self.board[up_row+1][col] = block
                else:
                    self.board[up_row][col] = block


    def _shift_col_up(self, ind):
        if not self._col_is_empty(ind):
            for r in [0,1,2,3]:
                self._move_block_up(r, ind)


    def _move_left(self):
        for r in [0,1,2,3]:
            self._shift_row_left(r)


    def _move_right(self):
        for r in [0,1,2,3]:
            self._shift_row_right(r)

    def _move_down(self):
        for c in [0,1,2,3]:
            self._shift_col_down(c)

    def _move_up(self):
        for c in [0,1,2,3]:
            self._shift_col_up(c)

    def print_state(self):
        str = ''
        for r in self.board:
            str = '|'
            for c in r:
                if c is None:
                    str += '{:^6s}'.format(' ') + '|' #'{:10s} {:3d}  {:7.2f}'.format('xxx', 123, 98)
                else:
                    str += '{:^6d}'.format(c.value) + '|'
            print('-' * len(str))
            print(str)
        print('-' * len(str))


    def apply_move(self, move):
        if move == 'LEFT':
            if not self._check_can_move_left():
                return
            self._move_left()
        if move == 'RIGHT':
            if not self._check_can_move_right():
                return
            self._move_right()
        if move == 'DOWN':
            if not self._check_can_move_down():
                return
            self._move_down()
        if move == 'UP':
            if not self._check_can_move_up():
                return
            self._move_up()

        self._add_block()
        self._reset_blocks()

    def _check_full(self):
        for r in self.board:
            for block in r:
                if block is None:
                    return False
        return True

    def _check_can_move_left(self):
        valid = False
        for r in self.board:
            if r == [None,None,None,None]:
                valid = valid or False
            else:
                for c in [0,1,2]:
                    if r[c+1] is not None and r[c] is not None:
                        valid = valid or r[c].can_merge(r[c+1])
                    elif r[c+1] is not None and r[c] is None:
                        valid = True
        return valid

    def _check_can_move_right(self):
        valid = False
        for r in self.board:
            if r == [None,None,None,None]:
                valid = valid or False
            else:
                for c in [3,2,1]:
                    if r[c-1] is not None and r[c] is not None:
                        valid = valid or r[c-1].can_merge(r[c])
                    elif r[c-1] is not None and r[c] is None:
                        valid = True
        return valid

    def _check_can_move_down(self):
        valid = False
        for c in [0,1,2,3]:
            if self._col_is_empty(c):
                valid = valid or False
            else:
                for r in [0,1,2]:
                    if self.board[r][c] is not None and self.board[r+1][c] is not None:
                        valid = valid or self.board[r+1][c].can_merge(self.board[r][c])
                    elif self.board[r][c] is not None and self.board[r+1][c] is None:
                        valid = True
        return valid

    def _check_can_move_up(self):
        valid = False
        for c in [0,1,2,3]:
            if self._col_is_empty(c):
                valid = valid or False
            else:
                for r in [3,2,1]:
                    if self.board[r][c] is not None and self.board[r-1][c] is not None:
                        valid = valid or self.board[r-1][c].can_merge(self.board[r][c])
                    elif self.board[r][c] is not None and self.board[r-1][c] is None:
                        valid = True
        return valid

    def _check_valid_moves(self):
        return self._check_can_move_left() or self._check_can_move_right() or self._check_can_move_up() or self._check_can_move_down()

    def check_loss(self):
        if self._check_full():
            return not self._check_valid_moves()
        return False
