from pathlib import Path

import numpy as np

from src.core.ascii import frame2ascii
from src.display.terminal import display_ascii_art
from src.sources.image import ImageType, enhance_image, img2np, load_image, resize_img


def save_to_file(ascii_mat: np.ndarray, filename: str | Path) -> None:
	with open(filename, "w") as file:
		file.write("\n".join(" ".join(row) for row in ascii_mat) + "\n")


if __name__ == "__main__":
	original_img: ImageType = load_image("images/pic.png", grayscale=True)
	resized_img: ImageType = resize_img(original_img, 24)

	enhanced_img: ImageType = enhance_image(resized_img)
	mat: np.ndarray = img2np(enhanced_img)
	ascii_mat: np.ndarray = frame2ascii(frame=mat)
	display_ascii_art(ascii_mat)
