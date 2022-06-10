import flask
import requests
from flask import current_app as app
import fnmatch
import os


class Product:
    name = ''
    price = 0
    currency = ''
    info = ''
    short_description = ''
    full_description = ''
    slug = ''


def get_templates_dir():
    return app.static_url_path


def get_products_dir():
    return os.path.join(app.static_url_path, 'products')


def get_product_path(aSlug):
    return os.path.join(app.static_url_path, 'products', aSlug)


def get_files(aPath, ext='json'):
    matches = []
    os.listdir(aPath)
    for root, dirnames, filenames in os.walk(aPath):
        for filename in fnmatch.filter(filenames, '*.' + ext):
            item = os.path.join(root, filename)
            matches.append(item.split('./pub')[1])

    return matches


def get_products():
    return get_files('./pub/static/products', 'json')


def get_slug(aPath, aExt='json'):
    if aPath:
        head, tail = os.path.split(aPath)  # get file name
        return tail.replace('.' + aExt, '')  # remove extension

    return None


def load_product(aJSONPath):

    data = requests.get(flask.request.root_url + aJSONPath).json()

    if not data:
        return None

    product = Product()

    product.name = data["name"]
    product.info = data["info"]
    product.price = int(data["price"])
    product.short_description = data["short_description"]
    product.full_description = data["full_description"]

    product.slug = get_slug(aJSONPath)

    return product


def load_product_by_slug(aSlug):
    aJSONPath = app.static_url_path + '/products/' + aSlug + '.json'
    return load_product(aJSONPath)
