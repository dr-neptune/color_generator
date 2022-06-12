# adapted from https://github.com/ilikescience/category-colors
# Brettel et al method for simulating color vision deficiency
# Adapted from https://github.com/MaPePeR/jsColorblindSimulator
# In turn adapted from libDaltonLens https://daltonlens.org (public domain)
import logging
import numpy as np
from itertools import combinations
from typing import List

from color import Color, color_distance


def sRGB_to_lRGB(sRGB: float) -> float:
    """
    sRGB color to linearRGB translation

    Args:
        sRGB: A float representing part of a color in sRGB format (R, G, or B) in [0, 255]

    Returns:
        a float in lRGB format in [0, 1]

    Notes:
        Extended constants from https://entropymine.com/imageworsener/srgbformula/
    """
    fv = sRGB / 255.
    if fv < 0.0404482362771082:
        return fv / 12.92
    else:
        return ((fv + 0.055) / 1.055) ** 2.4

def lRGB_to_sRGB(lRGB: float) -> float:
    """
    linearRGB to sRGB translation

    Args:
        lRGB: A float representing part of a color in sRGB format (R, G, or B) in [0, 1]

    Returns:
        a float in sRGB format in [0, 255]

    Extended constants from https://entropymine.com/imageworsener/srgbformula/
    """
    if lRGB <= 0:
        return 0
    elif lRGB >= 1:
        return 255
    elif lRGB <= 0.00313066844250063:
        return 0.5 + lRGB * 12.92 * 255
    else:
        return 255 * (lRGB ** (1.0 / 2.4))


def monochrome_with_severity(sRGB: List[float], severity: float) -> List[float]:
    """
    Adjusts given sRGB R, G, B values to account for monochrome color blindness

    Args:
        sRGB: A float representing a color in sRGB format
        severity: A float in [0, 1] representing the severity of condition to account for

    Returns:
       A list of updated R, G, B values in sRGB space [0, 255]
    """
    z = round(sRGB[0] * 0.299 + sRGB[1] * 0.587 + sRGB[2] * 0.114)
    r = z * severity + (1. - severity) * sRGB[0]
    g = z * severity + (1. - severity) * sRGB[1]
    b = z * severity + (1. - severity) * sRGB[2]
    return [r, g, b]


class Brettel:

    BRETTEL_PARAMS = {
        'protan': {
            'rgb_cvd_from_rgb1': [0.1451, 1.20165, -0.34675, 0.10447, 0.85316, 0.04237, 0.00429, -0.00603, 1.00174],
            'rgb_cvd_from_rgb2': [0.14115, 1.16782, -0.30897, 0.10495, 0.8573, 0.03776, 0.00431, -0.00586, 1.00155],
            'separation_plane_normal': [0.00048, 0.00416, -0.00464]},
        'deutan': {
            'rgb_cvd_from_rgb1': [0.36198, 0.86755, -0.22953, 0.26099, 0.64512, 0.09389, -0.01975, 0.02686, 0.99289],
            'rgb_cvd_from_rgb2': [0.37009, 0.8854, -0.25549, 0.25767, 0.63782, 0.10451, -0.0195, 0.02741, 0.99209],
            'separation_plane_normal': [-0.00293, -0.00645, 0.00938]
            },
        'tritan': {
            'rgb_cvd_from_rgb1': [1.01354, 0.14268, -0.15622, -0.01181, 0.87561, 0.13619, 0.07707,0.81208, 0.11085],
            'rgb_cvd_from_rgb2': [0.93337, 0.19999, -0.13336, 0.05809, 0.82565, 0.11626, -0.37923, 1.13825, 0.24098],
            'separation_plane_normal': [0.0396, -0.02831, -0.01129]
            },
        }

    def __init__(self, sRGB: List[float]):
        """
        Changes sRGB ranges to account for color blindness types and severity

        Usage:
            Access the various functions through their attributes. For example:
            > Brettel(sRGB_value).Deuteranomaly

        Args:
            sRGB: A list of floats representing a color in sRGB format [R, G, B]
        """
        self.Normal = sRGB
        self.Protanopia = self.brettel(sRGB, 'protan', 1.0)
        self.Protanomaly = self.brettel(sRGB, 'protan', 0.6)
        self.Deuteranopia = self.brettel(sRGB, 'deutan', 1.0)
        self.Deuteranomaly = self.brettel(sRGB, 'deutan', 0.6)
        self.Tritanopia = self.brettel(sRGB, 'tritan', 1.0)
        self.Tritanomaly = self.brettel(sRGB, 'tritan', 0.6)
        self.Achromatopsia = monochrome_with_severity(sRGB, 1.0)
        self.Achromatomaly = monochrome_with_severity(sRGB, 0.6)

    def brettel(self, sRGB: List[float], cb_type: str, severity: float) -> List[float]:
        """
        Brettel adjustment to a given color

        Args:
            sRGB: A list of [R, G, B] values comprising a color
            cb_type: color blindness type to account for
            severity: the severity of the color blindness to account for

        Returns:
            A list of floats in sRGB space transformed to account for the color blindness type in [0, 255] space

        Notes:
            > http://vision.psychol.cam.ac.uk/jdmollon/papers/Dichromatsimulation.pdf
        """
        rgb = [sRGB_to_lRGB(v) for v in sRGB]
        params = Brettel.BRETTEL_PARAMS[cb_type]
        separation_plane_normal = params['separation_plane_normal']

        # check on which plane we should project by comparaing with the separation plane normal
        sep_plane_dot = np.dot(rgb, separation_plane_normal)
        rgb_cvd_from_rgb = params['rgb_cvd_from_rgb1'] if sep_plane_dot >= 0 else params['rgb_cvd_from_rgb2']

        # transform to the full dichromat projection plane
        rgb_cvd = [np.dot(rgb_cvd_from_rgb[:3], rgb),
                   np.dot(rgb_cvd_from_rgb[3:6], rgb),
                   np.dot(rgb_cvd_from_rgb[6:9], rgb)]

        # apply the severity factor as a linear interpolation
        rgb_cvd[0] = rgb_cvd[0] * severity + rgb[0] * (1.0 - severity);
        rgb_cvd[1] = rgb_cvd[1] * severity + rgb[1] * (1.0 - severity);
        rgb_cvd[2] = rgb_cvd[2] * severity + rgb[2] * (1.0 - severity);

        # return sRGB values
        return [lRGB_to_sRGB(v) for v in rgb_cvd]


def corrected_color_distances(color_list: List[Color], vision_space = 'Normal') -> List[float]:
    """
    makes an array of distances between all points in a color list after applying the vision_space color transformation to it

    Args:
        color_list: A list of Color objects
        vision_space: A Brettel function for determining a vision space

    Returns:
        A list of distances
    """
    # convert color space
    try:
        colors = [Color(*getattr(Brettel(c.rgb), vision_space)) for c in color_list]
    except AttributeError:
        logging.warning(f'Expected attribute in Brettel class. Got {vision_space}')
        raise

    # get combinations
    color_combos = combinations(colors, 2)

    # get distances between each combination of colors
    return [color_distance(*c) for c in color_combos]
