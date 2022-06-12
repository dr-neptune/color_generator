from __future__ import annotations

import numpy as np
import matplotlib

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_diff import delta_e_cie2000
from colormath.color_conversions import convert_color

from typing import Tuple, List

from common import clip_values


class Color:
    def __init__(self, red: float, green: float, blue: float):
        """
        Represents a color. Provides functionality for using both RGB values in [0, 255]
        or a hex as an initializer.

        For hex initialization, use Color.from_hex("#your_hex_value")

        Args:
            red: A float in [0, 255] representing the amount of red in the color
            green: A float in [0, 255] representing the amount of green in the color
            blue: A float in [0, 255] representing the amount of blue in the color
        """
        self.rgb = np.array([red, green, blue])
        self.rgb = np.array([clip_values(val) for val in [red, green, blue]])
        self.hex = self.to_hex()
        self.lab_color = convert_color(sRGBColor(*self.rgb), LabColor)

    @classmethod
    def from_hex(cls, hex_value: str) -> Color:
        """
        Initialize a color object using a hex value

        Args:
             hex_value: A string containing a hex value, e.g. '#ffffff'

        Returns:
            A Color object for the given color
        """
        rgb = np.array(matplotlib.colors.to_rgb(hex_value)) * 255
        return Color(*rgb)

    @classmethod
    def random_color(cls) -> Color:
        """
        A classmethod that returns a random color

        Usage:
             > Color.random_color()
        """
        rgb = np.random.choice(range(1, 256), 3)
        return Color(*rgb)

    def to_hex(self) -> str:
        """
        returns a hex value for the given RGB value
        """
        return matplotlib.colors.to_hex(self.rgb / 255)

    def delta_e(self, other_color: Color) -> float:
        """
        Returns the ΔE value for the distance between 2 colors. Uses the CIEDE2000 definition

        Args:
            other_color: Another color object to compare against

        Returns:
            A float showing the 'distance' between the colors

        Notes:
            > https://en.wikipedia.org/wiki/Color_difference#CIEDE2000
        """
        return delta_e_cie2000(self.lab_color, other_color.lab_color)

    def get_closest_color(self, color_list: List[Color]) -> Tuple[Color, float]:
        """
        Given a color list, get the color which is closest to the Color object calling this method via ΔE.

        Args:
            color_list: A list of Color objects to compare

        Returns:
             A tuple containing the closest color's Color object and the ΔE value
        """
        distances = [self.delta_e(other_color) for other_color in color_list]
        min_val = np.argmin(distances)
        return color_list[min_val], distances[min_val]

    def nearby_color(self, drift_control: float = 0.1) -> Color:
        """
        Returns a 'nearby' color. Essentially takes a color, chooses a value in [R, G, B]
        and adds some random drift to it

        Args:
            drift_control: How much to allow randomness to affect the value update

        Returns:
            Returns a new Color object that is slightly different from the current color
        """
        index = np.random.choice(range(3), 1)
        new_rgb = self.rgb.copy()
        new_val = (new_rgb[index] / 255.) + np.random.rand() * drift_control - 0.05

        if new_val > 1:
            new_val = 1
        elif new_val < 0:
            new_val = 0

        new_rgb[index] = new_val * 255

        return Color(*new_rgb)

def average_color_distances_from_target(color_list: List[Color], target_colors: List[Color]) -> float:
    """
    Given 2 color lists, get the average distance between the colors

    Args:
        color_list: the input color list
        target_colors: the color list to compare it to. These arguments have arbitrary order

    Returns:
        The average distance value (ΔE)
    """
    distances = list(map(lambda c: c.get_closest_color(target_colors)[1], color_list))
    return np.average(distances)

def color_distance(color1: Color, color2: Color) -> float:
    """
    Given 2 colors, get the ΔE distance between them

    Args:
        color1: A Color object
        color2: A Color object

    Returns the ΔE distance
    """
    return delta_e_cie2000(color1.lab_color, color2.lab_color)


def hex_list(color_list: List[Color]) -> List[str]:
    """
    Given a list of Color objects, return a list of the hex codes

    Args:
        color_list: A list of Color objects

    Returns:
        A list of hex strings, i.e. ['#ffffff', '#000000']
    """
    return [c.to_hex() for c in color_list]
