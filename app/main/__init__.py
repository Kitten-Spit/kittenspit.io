from flask import Flask
from os import environ
from .shop.util import get_products, load_product, load_product_by_slug
from .shop.routes import shop_blueprint


def create_app():

    # Flask Config
    app = Flask(__name__)

    app.config.from_pyfile("config/config.cfg")

    # this is where jinja templates live:
    app.template_folder = "../../pub/templates/"

    # this is where jinja templates live:
    app.static_folder = "../../pub/static/"

    environ["TZ"] = app.config["TIMEZONE"]

    app.register_blueprint(shop_blueprint, url_prefix="/")

    # fetch static at the root of the application:
    @app.route("/<f>/", methods=["GET"])
    def appclcfx(f):
        print(f)
        return app.send_static_file(f)

    return app
