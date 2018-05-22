import fire
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from tqdm import tqdm

import NeuralNetwork as NN


def main(epochs, learnrate, perframe=100, act=None):

    nn = NN.NeuralNetwork(1, 1, [100]*10, act)
    nn.printInfo()

    # Function
    def f(x):
        x = x * 2 * np.pi
        return 0.07 * (x - 3) ** 2 + 0.2 * np.sin(6 * (x - 3))

    # Training data
    xt = np.random.rand(50, 1)
    yt = f(xt)

    costs = []
    x = np.linspace(0, 1, 500)[:, np.newaxis]
    yr = f(x)

    # Init progress pbar
    pbar = tqdm(total=epochs, leave=False)
    # Init graphs
    f, axs = plt.subplots(2)
    cost_line, = axs[0].plot(costs)
    # axs[0].set_xlim(0, epochs)
    axs[0].set_yscale("log")
    axs[0].set_ylabel("Cost")
    axs[0].set_xlabel("Iterations")
    axs[1].plot(x, yr, "r", label="Real")
    axs[1].plot(xt, yt, "oy", label="Training")
    nn_line, = axs[1].plot([], [], "", label="NN")
    axs[1].legend()

    def init():
        return cost_line, nn_line

    def animate(i):
        if i < epochs:
            foo = nn.train(xt, yt, learnrate, perframe)
            costs.extend(foo)
            pbar.update(perframe)
        cost_line.set_data(np.arange(len(costs)), costs)
        axs[0].relim()
        axs[0].autoscale_view()
        y = nn.feedForward(x)
        nn_line.set_data(x, y)
        return cost_line, nn_line

    frames = epochs // perframe
    anim = animation.FuncAnimation(
        f, animate, frames=frames, interval=40, blit=False, repeat=False
    )
    try:
        plt.show()
    finally:
        pbar.close()


if __name__ == "__main__":
    fire.Fire(main)
