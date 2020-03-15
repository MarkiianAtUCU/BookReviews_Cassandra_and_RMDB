from flask import Flask, jsonify, request, abort, Response
from DataBase.Cassandra import Cassandra


app = Flask(__name__)


@app.route('/reviews_by_product/<string:product_id>', methods=["GET"])
def reviews_by_product(product_id):
    pass


@app.route('/reviews_by_product_rating/<string:product_id>/<int:star_rating>', methods=["GET"])
def reviews_by_product_rating(product_id, star_rating):
    pass


@app.route('/reviews_by_customer/<int:customer_id>', methods=["GET"])
def reviews_by_customer(customer_id):
    pass


@app.route('/most_reviewed/<string:date_from>/<string:date_to>/<int:n>', methods=["GET"])
def most_reviewed(date_from, date_to, n):
    pass


@app.route('/most_productive/<string:date_from>/<string:date_to>/<int:n>', methods=["GET"])
def most_productive(date_from, date_to, n):
    pass


@app.route('/n_best/<float:fraction>/<int:n>', methods=["GET"])
def n_best(fraction, n):
    pass


@app.route('/most_productive_haters/<string:date_from>/<string:date_to>/<int:n>', methods=["GET"])
def most_productive_haters(date_from, date_to, n):
    pass


@app.route('/most_productive_backers/<string:date_from>/<string:date_to>/<int:n>', methods=["GET"])
def most_productive_backers(date_from, date_to, n):
    pass


if __name__ == "__main__":
    app.run()
