import copy
import time


def is_square(move, lines, state):
    # check for repetitious lines
    for j in range(len(lines)):
        for i in range(len(lines)):
            if i != j and (lines[i] == lines[j] or lines[i] == tuple(reversed(lines[j]))):
                return False

    for line in lines:
        if line == move or line == tuple(reversed(move)):
            continue
        elif not (line in state or tuple(reversed(line)) in state):
            return False
    return True


class Ai:
    def __init__(self, shape):
        self.shape = shape
        self.X = shape[0]
        self.Y = shape[1]

    def decide(self, state):
        all_length = 2 * self.X * (self.X - 1)
        legal_length = len(self.get_legal_moves(state))
        depth = 2
        # print('the legal length: ', legal_length)
        if self.X == 10:
            if 0 <= legal_length <= 5:
                depth = 10
            elif 5 < legal_length <= 6:
                depth = 5
            elif 6 < legal_length <= 8:
                depth = 4
            elif 8 < legal_length <= 9:
                depth = 3
            elif 9 < legal_length <= 10:
                depth = 4
            elif 10 < legal_length <= 43:
                depth = 2
            else:
                depth = 1
        elif self.X == 8:
            if legal_length <= 6:
                depth = 8
            elif 6 < legal_length <= 9:
                depth = 4
            elif 9 < legal_length <= 17:
                depth = 3
            else:
                depth = 2
        else:
            if legal_length <= 7:
                depth = 7
            elif 7 < legal_length <= 9:
                depth = 5
            elif 9 < legal_length <= 12:
                depth = 4
            elif 12 < legal_length <= 26:
                depth = 3
            else:
                depth = 2

        # print('depth: ', depth)
        _, move = self.minimax(depth, state, True)
        return move

    def minimax(self, depth, state, max_player, myScore=0, rivalScore=0):
        legal_moves = self.get_legal_moves(state)
        if not legal_moves or depth == 0:
            return myScore - rivalScore, None

        datas = dict()
        if max_player:
            state2 = copy.deepcopy(state)
            for move in legal_moves:
                new_state = state2 + [move]
                num = self.check_square_and_score(new_state, move, max_player)
                if num > 0:
                    key, value = self.minimax(depth - 1, new_state, True, myScore + num, rivalScore)
                else:
                    key, value = self.minimax(depth - 1, new_state, False, myScore + num, rivalScore)
                datas[key] = move
            # print('1', datas)
            max_eval = max(datas.keys())
            best_move = datas[max_eval]
            return max_eval, best_move

        else:
            state2 = copy.deepcopy(state)
            for move in legal_moves:
                new_state = state2 + [move]
                num = self.check_square_and_score(new_state, move, max_player)
                if num > 0:
                    key, value = self.minimax(depth - 1, new_state, False, myScore, rivalScore + num)
                else:
                    key, value = self.minimax(depth - 1, new_state, True, myScore, rivalScore + num)
                datas[key] = move
            # print('2', datas)
            min_eval = min(datas.keys())
            best_move = datas[min_eval]
            return min_eval, best_move

    def get_legal_moves(self, state):
        legal_moves = []
        for x in range(self.X - 1):
            for y in range(self.Y):
                move = ((x, y), (x + 1, y))
                if move not in state and move[::-1] not in state:
                    legal_moves.append(move)

        for x in range(self.X):
            for y in range(self.Y - 1):
                move = ((x, y), (x, y + 1))
                if move not in state and tuple(reversed(move)) not in state:
                    legal_moves.append(move)

        return legal_moves

    def check_square_and_score(self, state, move, flag):
        point1, point2 = move
        x0, y0 = point1
        x1, y1 = point2

        myScore = 0
        rivalScore = 0
        # case1
        if x0 != 0 and x1 != 0:
            lines = [
                ((x0, y0), (x1, y1)),
                ((x0, y0), (x0 - 1, y0)),
                ((x1, y1), (x1 - 1, y1)),
                ((x0 - 1, y0), (x1 - 1, y1))
            ]
            if is_square(move, lines, state) and (move in lines or tuple(reversed(move)) in lines):
                if flag:
                    myScore += 1
                else:
                    rivalScore += 1
        # case2
        if x0 + 1 != self.X and x1 + 1 != self.X:
            lines = [
                ((x0, y0), (x1, y1)),
                ((x0, y0), (x0 + 1, y0)),
                ((x1, y1), (x1 + 1, y1)),
                ((x0 + 1, y0), (x1 + 1, y1))
            ]
            if is_square(move, lines, state) and (move in lines or tuple(reversed(move)) in lines):
                if flag:
                    myScore += 1
                else:
                    rivalScore += 1
        # case3
        if y0 != 0 and y1 != 0:
            lines = [
                ((x0, y0), (x1, y1)),
                ((x0, y0), (x0, y0 - 1)),
                ((x1, y1), (x1, y1 - 1)),
                ((x1, y1 - 1), (x0, y0 - 1))
            ]
            if is_square(move, lines, state) and (move in lines or tuple(reversed(move)) in lines):
                if flag:
                    myScore += 1
                else:
                    rivalScore += 1
        # case4
        if y0 + 1 != self.Y and y1 + 1 != self.Y:
            lines = [
                ((x0, y0), (x1, y1)),
                ((x0, y0), (x0, y0 + 1)),
                ((x1, y1), (x1, y1 + 1)),
                ((x1, y1 + 1), (x0, y0 + 1))
            ]
            if is_square(move, lines, state) and (move in lines or tuple(reversed(move)) in lines):
                if flag:
                    myScore += 1
                else:
                    rivalScore += 1

        if flag:
            return myScore
        else:
            return rivalScore


# a = Ai((5, 5))
# arr = [((0, 0), (0, 1)), ((0, 1), (0, 2)), ((0, 2), (0, 3)), ((0, 3), (0, 4)), ((0, 2), (1, 2)), ((1, 2), (2, 2)),
#        ((2, 2), (3, 2)), ((3, 2), (4, 2)), ((4, 0), (4, 1)), ((4, 1), (4, 2)), ((4, 2), (4, 3)), ((4, 3), (4, 4)),
#        ((2, 2), (2, 1)), ((2, 2), (2, 3)), ((1, 1), (1, 0)), ((1, 0), (2, 0)), ((2, 0), (3, 0)), ((3, 0), (3, 1)),
#        ((1, 3), (1, 4)), ((1, 4), (2, 4)), ((2, 4), (3, 4)), ((3, 3), (3, 4))]
# t1 = time.time()
# print(a.decide(arr))
# print(time.time() - t1)
