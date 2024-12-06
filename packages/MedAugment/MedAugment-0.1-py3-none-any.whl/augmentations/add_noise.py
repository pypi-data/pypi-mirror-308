import numpy as np

def add_noise(image, noise_type='gaussian', noise_intensity=0.05):
    """
    Adds noise to the image to simulate different scanning conditions.
    
    Parameters:
    - image (np.array): Input image as a 2D or 3D numpy array.
    - noise_type (str): Type of noise to add ('gaussian' or 'salt_and_pepper').
    - noise_intensity (float): Intensity of the noise. For Gaussian, it represents std deviation; 
                               for salt_and_pepper, it represents proportion of affected pixels.

    Returns:
    - np.array: Image with added noise.
    """
    if noise_type == 'gaussian':
        # Gaussian noise
        mean = 0
        gauss = np.random.normal(mean, noise_intensity, image.shape)
        noisy_image = image + gauss
        return np.clip(noisy_image, 0, 1)  # Assuming image is in range [0, 1]
    
    elif noise_type == 'salt_and_pepper':
        # Salt-and-pepper noise
        noisy_image = image.copy()
        num_salt = np.ceil(noise_intensity * image.size * 0.5).astype(int)
        num_pepper = np.ceil(noise_intensity * image.size * 0.5).astype(int)

        # Add salt (white pixels)
        coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape]
        noisy_image[tuple(coords)] = 1

        # Add pepper (black pixels)
        coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape]
        noisy_image[tuple(coords)] = 0

        return noisy_image
    
    else:
        raise ValueError("Unsupported noise type. Use 'gaussian' or 'salt_and_pepper'.")
