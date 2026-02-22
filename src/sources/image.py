from pathlib import Path

import numpy as np
from PIL import Image
from PIL.Image import Image as ImageType


def load_image(path: Path | str, grayscale: bool = False) -> ImageType:
	image_path: Path = Path(path)
	if not image_path.exists():
		raise FileNotFoundError(f"{image_path} does not exist!")

	try:
		if grayscale:
			return Image.open(image_path).convert("L")
		else:
			return Image.open(image_path)

	except Exception as e:
		raise FileNotFoundError(f"Failed to open {image_path}! : {e}")


def img2np(img: ImageType) -> np.ndarray:
	return np.array(img)


def resize_img(img: ImageType, max_dim: int) -> ImageType:
	"""
	Resize image, so that the maximum dimension(width or height) is max_dim
	"""
	width, height = img.size
	ar: float = width / height

	new_height: int
	new_width: int

	# portrait image
	if height > width:
		new_height = max_dim
		new_width = int(ar * new_height)
	else:  # landscape image
		new_width = max_dim
		new_height = int(new_width / ar)

	resized_img: ImageType = img.resize(
		(new_width, new_height), Image.Resampling.LANCZOS
	)

	return resized_img
