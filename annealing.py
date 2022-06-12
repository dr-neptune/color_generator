from cytoolz import merge, curry
import numpy as np
from textwrap import dedent
from typing import List, Callable

from bretel import corrected_color_distances
from color import average_color_distances_from_target, Color, hex_list


def obj_fn(state: List[Color], target_colors: List[Color]) -> float:
    """
    An objective function that measures the distance between the current state (list of colors)
    and the target state (target_colors). Tweak the weights to change the output.

    From the original documentation:

    A higher
        > normal weight will result in colors that are more differentiable from each other
        > range weight will result in colors that are more uniformly spread through color space
        > target weight will result in colors that are closer to the target colors specified with targetColors
        > protanopia weight will result in colors that are more differentiable to people with protanopia
        > deuteranopia weight will result in colors that are more differentiable to people with deuteranopia
        > tritanopia weight will result in colors that are more differentiable to people with tritanopia

    Args:
        state: A list of colors representing the current iteration of the state of your optimization function
        target_colors: A list of colors representing the goal to work towards for your optimization function

    Returns:
        A float representing the 'score' of the current state
    """
    weights = {'Normal': 1,
               'Range': 1,
               'Target': 1,
               'Protanopia': 0.33,
               'Deuteranopia': 0.33,
               'Tritanopia': 0.33}

    # get distances of state from target w.r.t each of the different color blindness measures
    distances = {n: corrected_color_distances(state, n)
                 for n in ['Normal', 'Protanopia', 'Deuteranopia', 'Tritanopia']}

    # generate the 'scores'
    scores = merge(
        {n: 100 - np.average(distances[n])
         for n in ['Normal', 'Protanopia', 'Deuteranopia', 'Tritanopia']},
        {'Range': np.max(distances['Normal']) - np.min(distances['Normal']),
         'Target': average_color_distances_from_target(state, target_colors)})

    return (weights['Normal'] * scores['Normal'] +
            weights['Target'] * scores['Target'] +
            weights['Range'] * scores['Range'] +
            weights['Protanopia'] * scores['Protanopia'] +
            weights['Deuteranopia'] * scores['Deuteranopia'] +
            weights['Tritanopia'] * scores['Tritanopia'])


def anneal(input_colors: List[Color], result_count: int = 5,
           temperature: float = 1000., cooling_rate: float = 0.99, cutoff: float = .0001,
           objective_function: Callable = obj_fn,
           verbose: bool = True) -> List[Color]:
    """
    A simulated annealing hill climbing algorithm that attempts to minimize the distance from
    the input colors and random set of colors as measured by the objective_function

    Args:
        input_colors: A list of target colors to optimize toward
        result_count: How many colors to return
        temperature:  starting point temperature of the algorithm; higher temperature means that
                      early iterations are more likely to be randomly-chosen than optimized.
        cooling_rate: decrease in temperature at each iteration. A lower cooling rate will result in more iterations.
        cutoff:       temperature at which the algorithm will stop optimizing and return results
        objective_function: the objective function with which to measure success. Defaults to obj_fn
                            requires a target_colors parameter to accept the goal state
        verbose: print out the current temperature and cost?
                 Also prints out the (target, starting, final) color lists and (starting, final, difference) costs

    Side Effect:
        If verbose, prints to the console

    Returns:
        A list of the final resulting colors (in Color objects)
    """
    # get a random set of initial colors
    colors = [Color.random_color() for _ in range(result_count)]

    # set the objective function
    obj_fn = curry(objective_function, target_colors=input_colors)

    start_colors = colors.copy()
    start_cost = obj_fn(colors)

    while temperature > cutoff:
        for i in range(len(colors)):
            # copy colors
            new_colors = colors.copy()
            # move the current color randomly
            new_colors[i] = new_colors[i].nearby_color()
            # get objective function difference
            delta = obj_fn(new_colors) - obj_fn(colors)
            # choose between current and new state
            probability = np.exp(-delta / temperature)
            if np.random.rand() < probability:
                colors[i] = new_colors[i]

        if verbose:
            print(f"current cost:\t\t{obj_fn(colors)}")
            print(f"current temperature:\t{temperature}")

        temperature *= cooling_rate

    final_cost = obj_fn(colors)

    if verbose:
        print(dedent(f"""
                      Original Colors:\t{hex_list(input_colors)}
                      Starting Colors:\t{hex_list(start_colors)}
                      Final Colors:\t\t{hex_list(colors)}
                      Starting Cost:\t\t{start_cost}
                      Final Cost:\t\t{final_cost}
                      Cost Difference:\t{final_cost - start_cost}
                      """))

    return colors
