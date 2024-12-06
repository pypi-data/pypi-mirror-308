import numpy as np
from scipy.ndimage import gaussian_filter

def gaussian_blur(image, blur_radius=1):
    """
    Applies Gaussian blur to a given image.
    
    Parameters:
    - image (np.array): Input image as a 2D or 3D numpy array.
    - blur_radius (float): Standard deviation for Gaussian kernel. Higher values increase blur.

    Returns:
    - np.array: Blurred image with the same shape as input.
    """
    return gaussian_filter(image, sigma=blur_radius)
