import game


live = True
game2048 = game.Game()
commands = {
    'a': 'LEFT',
    's': 'DOWN',
    'w': 'UP',
    'd': 'RIGHT'
}

def score_board(board):
    score = 0
    for r in board:
        for c in r:
            if c is not None:
                score += c.value
    # We need to score the board in a better way, highest value in corner should double the score
    # all blocks next to same score block * 2
    # all blocks next to block half the score * 1.5
    # *2 if 4 highest blocks are in same row or column
    return score

while live:
    print(score_board(game2048.board))
    game2048.print_state()
    keypress = input("Press Enter to continue...\n")
    action = commands.get(keypress, None)
    if action is None:
        print('No Valid Action')
    else:
        game2048.apply_move(action)

    if game2048.check_loss():
        game2048.print_state()
        live=False
        print('YOU LOSE')

