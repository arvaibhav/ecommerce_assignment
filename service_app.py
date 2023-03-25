from flask_cors import CORS
from flask import Flask
import flask_restful as restful
from controller.product import Product
from controller.category import ProductCategory


def load_routes(app):
    sample_api = restful.Api(app, prefix='/api/v1/sample')
    sample_api.add_resource(ProductCategory, 'category/', 'category/<int:category_id>')
    sample_api.add_resource(Product, 'product/', 'product/<int:product_id>')


def create_app(app, debug=False):
    if not debug:
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevConfig')

    cors_allow_headers = ', '.join(app.config.get(
        'CORS_ALLOW_HEADERS',
        ["*", "authorization", 'Content-Type',
         'Client-Code', 'Accept-Language', 'Authorization'])
    )
    cors_allow_origins = ', '.join(app.config.get('CORS_ALLOW_ORIGINS', ["*"]))
    cors_allow_methods = ', '.join(app.config.get('CORS_ALLOW_METHODS', ["*"]))
    CORS(
        app, resources={
            r"/api/*": {
                "origins": "*",
                'Access-Control-Allow-Headers': cors_allow_headers,
                'Access-Control-Allow-Origin': cors_allow_origins,
                'Access-Control-Allow-Methods': cors_allow_methods
            }
        }
    )
    load_routes(app)
    return app


if __name__ == '__main__':
    local_app = create_app(Flask(__name__), debug=True)
    local_app.run(host="0.0.0.0", port=8000, debug=True)
else:
    gunicorn_app = create_app(Flask(__name__), debug=False)
