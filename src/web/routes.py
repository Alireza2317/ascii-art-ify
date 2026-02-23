from typing import TYPE_CHECKING

from flask import Blueprint, jsonify, render_template, request

from src.core.pipeline import load_ascii_mat_from_image_file

if TYPE_CHECKING:
	import numpy as np


main_blueprint: Blueprint = Blueprint("main", __name__)


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
		ascii_mat: np.ndarray = load_ascii_mat_from_image_file(
			image_file.stream, max_dim=244
		)

		# The frontend JavaScript will handle the rendering of this json
		return jsonify({"art": ascii_mat.tolist()})

	except IOError as e:
		# Handle specific, expected errors first
		print(f"An error occurred: {e}")
		return jsonify({"error": "Invalid or corrupted image file."}), 400
	except Exception as e:
		# Handle unexpected server errors
		print(f"An error occurred: {e}")
		return (
			jsonify({"error": "Sorry, something went wrong processing your image."}),
			500,
		)
