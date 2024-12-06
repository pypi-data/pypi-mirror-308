# yuxin_helpers/color_utils.py

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def rgb_to_hex(r: int, g: int, b: int) -> str:
    '''
    Convert an RGB color to a hexadecimal color.
    
    Parameters
    ----------
    r : int
        The red component.
    g : int
        The green component.
    b : int
        The blue component. 
    
    Returns
    -------
    str
        The hexadecimal color.
    '''
    return '#%02x%02x%02x' % (r, g, b)


def hex_to_rgb(hex: str) -> tuple[int, int, int]:
    '''
    Convert a hexadecimal color to an RGB color.
    
    Parameters
    ----------
    hex : str
        The hexadecimal color.
    
    Returns
    -------
    tuple[int, int, int]
        The RGB color.
    '''
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))



def truncate_colormap(cmap, min_val=0.0, max_val=1.0, n=100):
    """
    Truncate a colormap to a specified range of values.

    Parameters
    ----------
    cmap : matplotlib.colors.Colormap
        The colormap to be truncated.
    minval : float, optional
        The starting value of the colormap range (default is 0.0).
    maxval : float, optional
        The ending value of the colormap range (default is 1.0).
    n : int, optional
        The number of colors in the truncated colormap (default is 100).

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        The truncated colormap.

    Notes
    -----
    The function uses the `np.linspace` to create an evenly spaced array 
    of color values between the specified `minval` and `maxval`.
    """
    new_cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        f'trunc({cmap.name},{min_val},{max_val})',
        cmap(np.linspace(min_val, max_val, n)))

    return new_cmap


def create_cmap_from_data(data, seg_value=0, cmap='coolwarm'):
    """
    Create a custom colormap based on the given colormap name, with a specified segment value.

    Parameters
    ----------
    data : array-like
        The data array to determine the min and max values for normalization.
    seg_value : float, optional
        The value at which to segment the colormap. Default is 0.
    cmap : str, optional
        The name of the colormap to use as the base. Default is 'coolwarm'.

    Returns
    -------
    LinearSegmentedColormap
        A custom colormap with the specified segmentation.
    """
    # Get the colormap
    base_map = plt.get_cmap(cmap)
    base_colors = base_map(np.linspace(0, 1, 256))

    # Calculate the segment position
    min_val = data.min()
    max_val = data.max()
    seg = abs(seg_value - min_val) / (max_val - min_val)

    # Create the new color list
    colors = []

    # Distribute the first half of the colormap evenly from [0, seg]
    for i in range(128):
        colors.append((i / 128 * seg, base_colors[i]))

    # Distribute the second half of the colormap evenly from [seg, 1]
    for i in range(128, 256):
        colors.append((seg + (i - 128) / 128 * (1 - seg), base_colors[i]))

    # Ensure the start and end points are 0 and 1
    colors[0] = (0, base_colors[0])
    colors[-1] = (1, base_colors[-1])

    # Create the custom colormap
    custom_cmap = matplotlib.colors.LinearSegmentedColormap.from_list('custom_cmap', colors)
    return custom_cmap
