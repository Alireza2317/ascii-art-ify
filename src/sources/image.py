from pathlib import Path
from typing import IO

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from PIL.Image import Image as ImageType


def load_image(source: Path | str | IO[bytes], grayscale: bool = False) -> ImageType:
	"""
	Loads an image from a file path or a file-like object (e.g., from an upload).
	"""
	try:
		image: ImageType = Image.open(source)
		if grayscale:
			return image.convert("L")

		return image

	except FileNotFoundError:
		raise FileNotFoundError(f"File not found at `{source}`")
	except Exception as e:
		raise IOError(f"Failed to open {source}! : {e}")


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


def enhance_image(
	img: ImageType,
	contrast_factor: float = 1.5,
	autocontrast: bool = True,
	equalize: bool = True,
	sharpen: bool = True,
) -> ImageType:

	if autocontrast:
		img = ImageOps.autocontrast(img)

	if equalize:
		img = ImageOps.equalize(img)

	# Adjust contrast
	img = ImageEnhance.Contrast(img).enhance(contrast_factor)

	if sharpen:
		img = img.filter(ImageFilter.SHARPEN)

	return img
