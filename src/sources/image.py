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

