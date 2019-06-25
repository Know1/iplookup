import os, geoip2.database
from flask import Flask, jsonify, make_response, request

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'GeoLite2-City.mmdb'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        

    # Default Index page
    @app.route('/<ip>')
    def index(ip):
        if ip:
            reader = geoip2.database.Reader(app.config['DATABASE'])
            try:
                response = reader.city(ip)
                return make_response(
                            jsonify({'status': 'success',
                                    'response': response.raw}), 200)            
            except:
                return make_response(
                            jsonify({'status': 'error',
                                    'message': 'Invalid IPv4 or IPv6 Address'}), 400)

        else:
            return make_response(
                        jsonify({'status': 'error',
                                'message': 'You must supply an IP'}), 400)


    # A simple page that returns the status
    #TODO: Add actual status checking
    @app.route('/status')
    @app.route('/ping')
    def status():
        return make_response(
                    jsonify({'status': 'success',
                                'API': 'OK'}), 200)
    
    @app.errorhandler(404)
    def not_found(error):
        return make_response(
                    jsonify({'status': 'error'}), 404)

    return app

# Create Object for Gunicorn WSGI to call
application = create_app()
if __name__ == "__main__":
    application.run()
