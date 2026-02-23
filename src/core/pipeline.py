from pathlib import Path

import numpy as np

from src.core.ascii import frame2ascii
from src.sources.image import ImageType, enhance_image, img2np, load_image, resize_img


def load_ascii_mat_from_image_file(image_path: Path | str, max_dim: int) -> np.ndarray:
	"""
	Loads an image from a file path, processes it, and converts it into 
	a numpy array of ASCII characters.

	Args:
		image_path: The path to the image file.
		max_dim: The maximum dimension (width or height) for the resized image.

	Returns:
		A 2D NumPy array containing ASCII characters representing the image.
	"""

	original_img: ImageType = load_image(image_path, grayscale=True)
	resized_img: ImageType = resize_img(original_img, max_dim)
	enhanced_img: ImageType = enhance_image(resized_img)

	mat: np.ndarray = img2np(enhanced_img)
	ascii_mat: np.ndarray = frame2ascii(frame=mat)

	return ascii_mat
