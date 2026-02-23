from flask import Blueprint, render_template, request

from src.core.pipeline import load_ascii_mat_from_image_file

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
	return render_template("index.html")


@main_blueprint.route("/upload", methods=["POST"])
def upload():
	# Check if an image was uploaded
	if "image" not in request.files:
		return "No image selected!", 400

	image_file = request.files["image"]

	# Check if the file is empty
	if image_file.filename == "":
		return "No image selected!", 400

	try:
		ascii_mat = load_ascii_mat_from_image_file(image_file.stream, max_dim=200)

		ascii_str: str = "\n".join(" ".join(row) for row in ascii_mat) + "\n"
		# The <pre> tag preserves whitespace and uses a monospace font.
		return f'<pre style="font-size:2pt;">{ascii_str}</pre>'

	except Exception as e:
		# It's good practice to handle potential errors during processing
		print(f"An error occurred: {e}")
		return "Sorry, something went wrong while processing your image.", 500
