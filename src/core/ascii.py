import numpy as np


def get_density_index(pixel_value: int, num_gray_levels: int) -> int:
	"""Convert the pixel brightness to an index of the density map."""
	if num_gray_levels > 255:
		raise ValueError("num_gray_levels should be less than 255!")

	return min(int((pixel_value / 255) * num_gray_levels), num_gray_levels - 1)


def char_from_pixel(pixel_value: int) -> str:
	"""Convert the pixel brightness to a single character."""

	density_map: str = (
		"""$@B%8&W#M*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. """
	)

	return density_map[get_density_index(pixel_value, len(density_map))]


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

	return char_from_pixel_vectorized(frame) # type: ignore

