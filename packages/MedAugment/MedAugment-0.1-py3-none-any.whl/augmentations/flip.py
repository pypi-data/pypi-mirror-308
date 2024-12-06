import numpy as np

def flip(image, flip_horizontal=True, flip_vertical=False):
    """
    Flips the image horizontally, vertically, or both, based on the parameters.
    
    Parameters:
    - image (np.array): Input image as a 2D or 3D numpy array.
    - flip_horizontal (bool): If True, applies a horizontal flip.
    - flip_vertical (bool): If True, applies a vertical flip.

    Returns:
    - np.array: Flipped image based on specified parameters.
    """
    if flip_horizontal:
        image = np.fliplr(image)  # Horizontal flip
    if flip_vertical:
        image = np.flipud(image)  # Vertical flip
    return image