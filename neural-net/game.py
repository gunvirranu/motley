import numpy as np

from pong import Pong, GUIPong
from NeuralNetwork import NeuralNetwork, GeneticNetworkPool


def make_move(game, nn):
    ball_x, ball_y = game.get_ball_pos()
    b = np.array((ball_x / game.width, ball_y / game.height))
    raw_x = nn.feedForward(b)[0]
    px = int(raw_x * game.width)
    game.set_paddle_x(px)

def evaluate(game, nn):
    game.reset_score()
    for i in range(1000):
        game.update()
        make_move(game, nn)
    return game.get_score()


pong = Pong(500, 400)
nn = NeuralNetwork(2, 1, [20, 20])
pool = GeneticNetworkPool(nn, 10, lambda x: evaluate(pong, x))

nn.printInfo()

for i in range(10):
    print(pool.evaluate_all())
    pool.randomize_pool()

