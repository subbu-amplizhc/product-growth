import logging

from flask_api import FlaskAPI

from routes import register_routes

logging.basicConfig(level=logging.INFO)


def create_app():
    app = FlaskAPI(__name__)
    register_routes(app)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, threaded=True)