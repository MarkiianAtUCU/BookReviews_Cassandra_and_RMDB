from flask import Flask, jsonify, request, abort, Response
from DataBase.MySQL import MySQL

app = Flask(__name__)


@app.route('/reviews_by_product/<string:product_id>', methods=["GET"])
def reviews_by_product(product_id):
    return jsonify(database.reviews_by_product(product_id)), 200


@app.route('/reviews_by_product_rating/<string:product_id>/<int:star_rating>', methods=["GET"])
def reviews_by_product_rating(product_id, star_rating):
    return jsonify(database.reviews_by_product_rating(product_id, star_rating)), 200


@app.route('/reviews_by_customer/<int:customer_id>', methods=["GET"])
def reviews_by_customer(customer_id):
    return jsonify(database.reviews_by_customer(customer_id)), 200


@app.route('/most_reviewed/<string:date_from>/<string:date_to>/<int:n>', methods=["GET"])
def most_reviewed(date_from, date_to, n):
    return jsonify(database.n_most_reviewed(date_from, date_to,n)), 200


@app.route('/most_productive/<string:date_from>/<string:date_to>/<int:n>', methods=["GET"])
def most_productive(date_from, date_to, n):
    return jsonify(database.n_most_productive(date_from, date_to, n)), 200


@app.route('/n_best/<float:fraction>/<int:n>', methods=["GET"])
def n_best(fraction, n):
    return jsonify(database.n_best(fraction, n)), 200


@app.route('/most_productive_haters/<string:date_from>/<string:date_to>/<int:n>', methods=["GET"])
def most_productive_haters(date_from, date_to, n):
    return jsonify(database.n_most_productive_backers(date_from, date_to, n)), 200


@app.route('/most_productive_backers/<string:date_from>/<string:date_to>/<int:n>', methods=["GET"])
def most_productive_backers(date_from, date_to, n):
    return jsonify(database.n_most_productive_backers(date_from, date_to, n)), 200


if __name__ == "__main__":
    database = MySQL('<usr>', '<password>', '<localhost>')
    app.run()
