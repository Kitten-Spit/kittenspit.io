from flask import render_template, request, jsonify, Blueprint
from jinja2 import TemplateNotFound
import stripe
from .util import *
import json

# Opening JSON file
with open('stripe.json') as json_file:
    stripe_key_config = json.load(json_file)

# Stripe Credentials
stripe_keys = {
    "secret_key": stripe_key_config['STRIPE_SECRET_KEY'],
    "publishable_key": stripe_key_config['STRIPE_PUBLISHABLE_KEY'],
    "endpoint_secret": stripe_key_config['STRIPE_ENDPOINT_SECRET']
}

stripe.api_key = stripe_keys["secret_key"]


""" routing """


shop_blueprint = Blueprint("shop", __name__)


@shop_blueprint.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)


@shop_blueprint.route("/success")
def success():
    return render_template("payment-success.j2")


@shop_blueprint.route("/cancelled")
def cancelled():
    return render_template("payment-cancelled.j2")


@shop_blueprint.route("/create-checkout-session/<path>/")
def create_checkout_session(path):
    product = load_product_by_slug(path)

    domain_url = flask.request.root_url
    stripe.api_key = stripe_keys["secret_key"]

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - lets capture the payment later
        # [customer_email] - lets you prefill the email input in the form
        # For full details see https:#stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "name": product.name,
                    "quantity": 1,
                    "currency": 'usd',
                    "amount": product.price * 100,
                }
            ],
            shipping_address_collection={
                'allowed_countries': ['US', 'CA'],
            },
            shipping_options=[
                {
                    'shipping_rate_data': {
                        'type': 'fixed_amount',
                        'fixed_amount': {
                            'amount': 0,
                            'currency': 'usd',
                        },
                        'display_name': 'Free shipping',
                        # Delivers between 5-7 business days
                        'delivery_estimate': {
                            'minimum': {
                                'unit': 'business_day',
                                'value': 5,
                            },
                            'maximum': {
                                'unit': 'business_day',
                                'value': 7,
                            },
                        }
                    }
                },
                {
                    'shipping_rate_data': {
                        'type': 'fixed_amount',
                        'fixed_amount': {
                            'amount': 1500,
                            'currency': 'usd',
                        },
                        'display_name': 'Next day air',
                        # Delivers in exactly 1 business day
                        'delivery_estimate': {
                            'minimum': {
                                'unit': 'business_day',
                                'value': 1,
                            },
                            'maximum': {
                                'unit': 'business_day',
                                'value': 1,
                            },
                        }
                    }
                },
            ],
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403


# Product Index
@shop_blueprint.route('/')
def products_index():

    # Collect Products
    products = []
    d = get_products()

    # Scan all JSONs in `templates/products`
    for aJsonPath in d:

        # Load the product info from JSON
        product = load_product(aJsonPath)

        # Is Valid? Save the object
        if product:
            products.append(product)

    # Render Products Page
    return render_template('products/index.j2', products=products,
                           featured_product=load_product_by_slug('featured'))


# List Product
@shop_blueprint.route('/products/<path>/')
def product_info(path):
    product = load_product_by_slug(path)
    return render_template('products/template.j2', product=product)


@shop_blueprint.route('/<path>')
def index(path):
    try:

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/FILE.j2
        return render_template(path, segment=segment)

    except TemplateNotFound:
        return render_template('page-404.j2'), 404


def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
