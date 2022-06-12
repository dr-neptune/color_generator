import random
import matplotlib
matplotlib.use('tkAgg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime
from typing import List

from common import letter_range, EXAMPLE_COLORS, EXTENDED_COLORS


def line_plot(color_palette: List[str]):
    date = datetime.today()
    date_str = f"{date.day} {date.month} {date.year}"
    num_colors = len(color_palette)

    sns.set_theme(style="whitegrid")

    rs = np.random.RandomState(365)
    values = rs.randn(365, num_colors).cumsum(axis=0)
    dates = pd.date_range(date_str, periods=365, freq="D")
    data = pd.DataFrame(values, dates, columns=letter_range(num_colors))
    data = data.rolling(7).mean()

    sns.set_palette(sns.color_palette(color_palette))

    sns.lineplot(data=data, linewidth=2.5)


def palette_plot(pal: List[str], size: int = 1, ax=None):
    """palette plot, but with a fig and ax object"""
    n = len(pal)
    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(n * size, size))
    ax.imshow(np.arange(n).reshape(1, n),
              cmap=matplotlib.colors.ListedColormap(list(pal)),
              interpolation="nearest", aspect="auto")
    ax.set_xticks(np.arange(n) - .5)
    ax.set_yticks([-.5, .5])
    # border between colors
    ax.set_xticklabels(["" for _ in range(n)])
    # set no ticks
    ax.yaxis.set_major_locator(ticker.NullLocator())


def comparison_palette_plots(palette1: List[str], palette2: List[str]):
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
    palette_plot(sns.color_palette(EXAMPLE_COLORS), ax=ax1)
    palette_plot(sns.color_palette(EXTENDED_COLORS), ax=ax2)


def joint_and_marginal_histogram(color_palette: List[str]):
    sns.set_theme(style="ticks")
    sns.set_palette(sns.color_palette(color_palette))

    # Load the planets dataset and initialize the figure
    planets = sns.load_dataset("planets")

    # add binned colors
    palette_len = len(color_palette)
    planets['distance_bin'] = pd.qcut(planets['distance'], palette_len, labels=letter_range(palette_len))

    g = sns.JointGrid(data=planets, x="year", y="distance", marginal_ticks=True)

    # Set a log scaling on the y axis
    g.ax_joint.set(yscale="log")

    # Create an inset legend for the histogram colorbar
    cax = g.figure.add_axes([.15, .55, .02, .2])

    # Add the joint and marginal histogram plots
    g.plot_joint(sns.histplot, discrete=(True, False), hue=planets['distance_bin'])
    g.plot_marginals(sns.histplot, element="step", color=random.choice(color_palette))


def scatter_plot(color_palette):
    sns.set_theme(style="whitegrid")
    c_pal_len = len(color_palette)

    # Load the example planets dataset
    planets = sns.load_dataset("planets")
    planets['distance_bin'] = pd.qcut(planets['distance'], c_pal_len, labels=letter_range(c_pal_len))

    g = sns.relplot(
        data=planets,
        x="distance", y="orbital_period",
        hue="distance_bin", size="mass",
        palette=sns.color_palette(color_palette), sizes=(10, 200),
    )
    g.set(xscale="log", yscale="log")
    g.ax.xaxis.grid(True, "minor", linewidth=.25)
    g.ax.yaxis.grid(True, "minor", linewidth=.25)
    g.despine(left=True, bottom=True)


if __name__ == '__main__':
    line_plot(EXAMPLE_COLORS)
    line_plot(EXTENDED_COLORS)
    comparison_palette_plots(EXAMPLE_COLORS, EXTENDED_COLORS)
    joint_and_marginal_histogram(EXAMPLE_COLORS)
    joint_and_marginal_histogram(EXTENDED_COLORS)
    scatter_plot(EXAMPLE_COLORS)
    scatter_plot(EXTENDED_COLORS)
    plt.show()
