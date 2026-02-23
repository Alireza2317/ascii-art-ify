from pathlib import Path
from typing import IO

import numpy as np

from src.core.ascii import frame2ascii
from src.sources.image import ImageType, enhance_image, img2np, load_image, resize_img


def load_ascii_mat_from_image_file(
	image_source: Path | str | IO[bytes], max_dim: int
) -> np.ndarray:
	"""
	Processes an image from a file path or file-like object into an ASCII character matrix.

	Args:
		image_source: The source of the image (Path, string, or file-like object).
		max_dim: The maximum dimension (width or height) for the resized image.

	Returns:
		A 2D NumPy array containing ASCII characters representing the image.
	"""

	original_img: ImageType = load_image(image_source, grayscale=True)
	resized_img: ImageType = resize_img(original_img, max_dim)
	enhanced_img: ImageType = enhance_image(resized_img)

	mat: np.ndarray = img2np(enhanced_img)
	ascii_mat: np.ndarray = frame2ascii(frame=mat)

	return ascii_mat
