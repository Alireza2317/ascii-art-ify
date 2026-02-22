from pathlib import Path

from PIL import Image
from PIL.Image import Image as ImageType


def load_image(path: Path | str) -> ImageType:
	image_path: Path = Path(path)
	if not image_path.exists():
		raise FileNotFoundError(f"{image_path} does not exist!")

	try:
		return Image.open(image_path)

	except Exception as e:
		raise FileNotFoundError(f"Failed to open {image_path}! : {e}")
