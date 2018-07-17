import colorsys
import webcolors
from operator import itemgetter


class ColorException(Exception):
    pass        


def get_hue_name(hue):
    """Get the name of a hue.

    Args:
        hue (int): The value of a hue from a HSV tuple.

    Returns:
        str: The color name from the hue value.
    """
    if 0 <= hue <= 15:
        return 'red'
    elif 15 < hue <= 45:
        return 'orange'
    elif 45 < hue <= 70:
        return 'yellow'
    elif 70 < hue <= 90:
        return 'lime'
    elif 90 < hue <= 145:
        return 'green'
    elif 145 < hue <= 160:
        return 'turquoise'
    elif 160 < hue <= 185:
        return 'cyan'
    elif 185 < hue <= 210:
        return 'lightblue'
    elif 210 < hue <= 260:
        return 'blue'
    elif 260 < hue <= 275:
        return 'purple'
    elif 275 < hue <= 300:
        return 'magenta'
    elif 300 < hue <= 330:
        return 'pink'
    elif 330 < hue <= 360:
        return 'red'


def get_color(rgb):
    """Get the name of a color for a RGB value.

    Resolve the human readable names for a RBG value. This method is a great
    speed increase over the `get_most_likely_colors` method, however it assumes
    that the hue is the exact color name and is limited to 16 colors (for now).

    Args:
        rgb (list of int): The Red, Green, Blue triplet.

    Returns:
        set of str: The color name from the RGB value.
    """
    hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    hue = int(hsv[0] * 360)
    saturation = hsv[1]
    brightness = hsv[2] / 255
    color_name = get_hue_name(hue)
    print(hue, saturation, brightness)

    if brightness < 0.3:
        color = 'black'
    elif saturation < 0.05 and brightness > 0.95:
        color = 'white'
    elif (saturation < 0.05 and brightness > 0.30) or (saturation < 0.1 and brightness < 0.50):
        color = 'grey'
    elif brightness < 0.75:
        color = 'dark-' + color_name
    elif saturation < 0.75 and brightness > 0.95:
        color = 'light-' + color_name
    else:
        color = color_name

    return set([color])


def get_most_likely_colors(rgb):
    """Get the name of a color for a RGB value.

    Resolve the three closest human readable names for a RBG value.

    Args:
        rgb (list of int): The Red, Green, Blue triplet.

    Returns:
        set of str: The closest color names from the RGB value.
    """
    min_colors = {}

    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb[0]) ** 2
        gd = (g_c - rgb[1]) ** 2
        bd = (b_c - rgb[2]) ** 2
        min_colors[(rd + gd + bd)] = name

    # Sort the keys based on the minimum values, indicating liklihood.
    min_colors = [min_colors[key] for key in sorted(
        min_colors.keys(), reverse=False)]

    # Return the 3 most likely colors in order of likelihood.
    return set(min_colors[:3])


def update_color_freq(color_freq, current_colors, depth):
    """Update the color local freq Counter.

    Track the frequency of a color for the given depth and direction, and
    multiply it by the likelihood that the correct color was identified.
    
    Args:
        color_freq (Counter): The freq of colors.
        current_colors (tuple): The next pixel's color.
        depth (str): Whether this is for inner or outer colours.

    Returns:
        color_freq (Counter): The freq of colors.
    """
    for i, color in enumerate(reversed(list(current_colors))):
        i += 1
        if color in color_freq[depth].keys():
            color_freq[depth][color] += 1 * i
        else:
            color_freq[depth][color] = 1 * i

    return color_freq
