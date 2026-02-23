from flask import Flask

from src.web.routes import main_blueprint


def create_app() -> Flask:
	"""
	Creates and configures the Flask application.
	"""
	app = Flask(__name__)

	# Register the blueprint, which contains all our routes
	app.register_blueprint(main_blueprint)

	return app


if __name__ == "__main__":
	flask_app = create_app()

	flask_app.run(debug=True)
