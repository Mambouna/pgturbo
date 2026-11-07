"""Generate plots of the tweeners, to include in docs."""

from matplotlib import pyplot as plt
import numpy as np

from pgturbo import animation

from pathlib import Path

OUT_DIR = Path(__file__).parent.resolve() / ".." / "_static" / "animate_plots"

IMAGE_SIZE = 64, 64


def plot(f, filename):
    num_points = 256
    x = np.linspace(0, 1, num_points)
    y = np.vectorize(f)(x)
    plt.figure(figsize=(3, 1.5), dpi=num_points)
    plt.axis('off')
    plt.plot(x, y, color='#3a76a8')
    plt.tight_layout()
    plt.savefig(filename, dpi=num_points)
    plt.close()


if __name__ == '__main__':
    for name, f in animation.TWEEN_FUNCTIONS.items():
        filepath = OUT_DIR / "{}.png".format(name)
        #filename = '_static/animate_plots/{}.png'.format(name)
        plot(f, filepath)
