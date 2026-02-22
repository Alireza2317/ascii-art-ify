import sys
from time import sleep

import numpy as np


def clear_screen() -> None:
	"""Clear the terminal screen."""
	sys.stdout.write("\033[2J")


def display_ascii_art(
	ascii_frame: np.ndarray, frame_time: float = 0.05, clear: bool = True
) -> None:
	"""
	Clears the terminal and prints the ASCII art frame.
	"""
	if clear:
		clear_screen()
	else:
		# Move cursor to top-left corner
		sys.stdout.write("\033[H")
		sys.stdout.flush()

	# Join rows with newlines and print in one go
	output: str = "\n".join(" ".join(row) for row in ascii_frame) + "\n"
	sys.stdout.write(output)
	sys.stdout.flush()

	sleep(frame_time)
