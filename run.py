from color import Color, hex_list
from annealing import anneal
import matplotlib.pyplot as plt

from common import EXAMPLE_COLORS
from plotting import comparison_palette_plots, line_plot, palette_plot, joint_and_marginal_histogram, scatter_plot

if __name__ == '__main__':
    your_colors = EXAMPLE_COLORS  # ['#hex_code', ..., '#hex_code']
    target_colors = [Color.from_hex(c) for c in your_colors]
    result_colors = anneal(target_colors)

    # plotting
    # convert to hex for plots
    result_colors = hex_list(result_colors)
    combined_colors = result_colors + your_colors
    line_plot(combined_colors)
    palette_plot(combined_colors)
    comparison_palette_plots(target_colors, result_colors)
    joint_and_marginal_histogram(combined_colors)
    scatter_plot(combined_colors)
    plt.show()
