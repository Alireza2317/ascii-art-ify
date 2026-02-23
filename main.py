from pathlib import Path

import numpy as np

from src.core.ascii import frame2ascii
from src.display.terminal import display_ascii_art
from src.sources.image import ImageType, enhance_image, img2np, load_image, resize_img


def save_to_file(ascii_mat: np.ndarray, filename: str | Path) -> None:
	with open(filename, "w") as file:
		file.write("\n".join(" ".join(row) for row in ascii_mat) + "\n")


def load_ascii_mat_from_image_file(image_path: Path | str, max_dim: int) -> np.ndarray:
	original_img: ImageType = load_image(image_path, grayscale=True)
	resized_img: ImageType = resize_img(original_img, max_dim)
	enhanced_img: ImageType = enhance_image(resized_img)

	mat: np.ndarray = img2np(enhanced_img)
	ascii_mat: np.ndarray = frame2ascii(frame=mat)

	return ascii_mat


if __name__ == "__main__":
	ascii_mat: np.ndarray = load_ascii_mat_from_image_file("images/pic.png", 24)
	display_ascii_art(ascii_mat)
