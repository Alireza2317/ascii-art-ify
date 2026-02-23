from pathlib import Path

import numpy as np


def load_charset() -> str:
	CHARSET_FILENAME: str = "charset.txt"

	density_map: str
	try:
		CHARSET_PATH = Path(__file__).parent / CHARSET_FILENAME
		with open(CHARSET_PATH, "r") as f:
			density_map = f.read()
	except FileNotFoundError:
		# Fallback to a default string if the file doesn't exist
		print(
			"Warning: 'charset.txt' not found. Using default character set. "
			"Run 'scripts/generate_charset.py' to generate a more accurate one."
		)
		density_map = """BMN@W#8gRQD0HOE96&$qKpGdbmUPA5aeS4Z3XwhkoVF2%IyCun{}1TJtfjsiYzxL[]7vc=l?<>+|)(r/*!_^;:,'-.` """

	return density_map


DENSITY_MAP: str = load_charset()


def get_density_index(pixel_value: int) -> int:
	"""Convert the pixel brightness to an index of the density map."""
	num_gray_levels: int = len(DENSITY_MAP)

	if num_gray_levels > 255:
		raise ValueError("num_gray_levels should be less than 255!")

	return min(int((pixel_value / 255) * num_gray_levels), num_gray_levels - 1)


def char_from_pixel(pixel_value: int) -> str:
	"""Convert the pixel brightness to a single character."""

	return DENSITY_MAP[get_density_index(pixel_value)]


def is_valid_frame(frame: np.ndarray) -> bool:
	is_2d: bool = frame.ndim == 2
	is_3d_and_monochannel: bool = (frame.ndim == 3) and frame.shape[2] == 1

	return is_2d or is_3d_and_monochannel


def frame2ascii(frame: np.ndarray) -> np.ndarray:
	if not is_valid_frame(frame):
		raise ValueError(
			"The input frame should have only 1 color channel! "
			+ "Or should be a 2D array!"
		)

	# convert the frame to 2D
	if frame.ndim == 3:
		frame.squeeze(axis=2)

	char_from_pixel_vectorized = np.vectorize(char_from_pixel, otypes=[str])

	return char_from_pixel_vectorized(frame)  # type: ignore
