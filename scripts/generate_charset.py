from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as ImageType
from PIL.ImageDraw import ImageDraw as ImageDrawType
from PIL.ImageFont import FreeTypeFont

# The set of characters to be sorted by density.
ASCII_CHARS = """ `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"""


def get_font_density_map(
	characters: str, font_path: str, font_size: int = 32
) -> dict[str, int]:
	"""
	Renders characters using a font and calculates their pixel density.
	"""
	try:
		font: FreeTypeFont = ImageFont.truetype(font_path, font_size)
	except IOError:
		raise FileNotFoundError(
			f"Error: Font file not found at '{font_path}'. Please make sure it exists.\n"
			+ "You can download 'DejaVuSansMono.ttf' from the official site\n"
			+ "https://dejavu-fonts.github.io/"
		)

	density_map = {}

	for char in characters:
		canvas_size: tuple[int, int] = (font_size, int(font_size * 1.3))
		image: ImageType = Image.new(mode="L", size=canvas_size, color=0)
		draw: ImageDrawType = ImageDraw.Draw(image)
		draw.text(xy=(0, 0), text=char, font=font, fill=255)

		density: int = np.sum(np.array(image))
		density_map[char] = density
	return density_map


def generate_charset_file(
	font_path: Path, output_path: Path, force: bool = False
) -> None:
	"""Generates and saves the sorted character set if it doesn't exist."""
	if (not force) and output_path.exists():
		print(f"Character set already exists at '{output_path}'. Skipping generation.")
		return

	if not font_path.exists():
		print(f"Font not found at '{font_path}'")
		print("Please download 'DejaVuSansMono.ttf' into the 'fonts' directory.")
		print("Download from: https://dejavu-fonts.github.io/")
		return

	print("Calculating character densities...")
	char_densities = get_font_density_map(ASCII_CHARS, str(font_path))

	if char_densities:
		sorted_chars = sorted(
			char_densities.keys(), key=lambda char: char_densities[char],
			reverse=True
		)
		sorted_ascii_string = "".join(sorted_chars)

		# Ensure the parent directory exists
		output_path.parent.mkdir(exist_ok=True)
		with open(output_path, "w") as f:
			f.write(sorted_ascii_string)

		print(f"Successfully generated and saved character set to '{output_path}'")


if __name__ == "__main__":
	# Paths are relative to the project root for consistency
	PROJECT_ROOT = Path(__file__).parent.parent
	FONT_PATH = PROJECT_ROOT / "fonts" / "DejaVuSansMono.ttf"
	CHARSET_OUTPUT_PATH = PROJECT_ROOT / "src" / "core" / "charset.txt"

	generate_charset_file(FONT_PATH, CHARSET_OUTPUT_PATH, force=True)
