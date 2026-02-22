import numpy as np

from src.core.ascii import frame2ascii
from src.sources.image import ImageType, img2np, load_image, resize_img


def pretty_print(mat: np.ndarray) -> None:
	for row in mat:
		for char in row:
			print(char, end=" ")
		print()


if __name__ == "__main__":
	original_img: ImageType = load_image("images/pic.png", grayscale=True)
	resized_img: ImageType = resize_img(original_img, 24)
	mat: np.ndarray = img2np(resized_img) * 1.3

	ascii_mat: np.ndarray = frame2ascii(frame=mat)

	pretty_print(ascii_mat)
