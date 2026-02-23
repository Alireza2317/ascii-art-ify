from pathlib import Path

import numpy as np


def save_to_file(ascii_mat: np.ndarray, filename: str | Path) -> None:
	"""
	Saves the ASCII art matrix to a text file.

	Args:
		ascii_mat: A 2D NumPy array where each element is an ASCII character.
		filename: The path to the output file.
	"""
	with open(filename, "w") as file:
		output = "\n".join(" ".join(row) for row in ascii_mat) + "\n"
		file.write(output)
