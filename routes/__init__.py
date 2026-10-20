from routes.hospital import hospital_bp


def register_routes(app):
    app.register_blueprint(hospital_bp, url_prefix='/api')