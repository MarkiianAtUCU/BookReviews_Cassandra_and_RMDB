import mysql.connector as sql

class MySQL:
    def __init__(self, user, password, ip):
        conn = sql.connect(host=ip, user=user, password=password, database='bookstore')
        self.cursor = conn.cursor()

    def reviews_by_product(self, product_id):
        res = self.session.execute(f"SELECT * FROM reviews_by_product WHERE product_id='{product_id}';")
        return jsonify(res)

    def reviews_by_product_rating(self, product_id, star_rating):
        res = self.session.execute(
            f"SELECT * FROM reviews_by_product WHERE product_id='{product_id}' AND star_rating={star_rating};")
        return jsonify(res)

    def reviews_by_customer(self, customer_id):
        res = self.session.execute(f"SELECT * FROM reviews_by_customer WHERE customer_id={customer_id};")
        return jsonify(res)

    def n_most_reviewed(self, date_from, date_to, n):
        date_list_formatted = ",".join(date_range_to_list(date_from, date_to))
        res = self.session.execute(
            f"SELECT product_id FROM reviews_by_date_star WHERE review_date IN ({date_list_formatted});")
        result_product_id = ", ".join([f"'{i[0]}'" for i in get_n_most_reviewed(res, n)])
        res = self.session.execute(
            f"SELECT product_id, product_category, product_title FROM bookstore.reviews_by_product WHERE product_id in ({result_product_id}) GROUP BY product_id;")
        return jsonify(res)

    def n_most_productive(self, date_from, date_to, n):
        date_list_formatted = ",".join(date_range_to_list(date_from, date_to))
        res = self.session.execute(
            f"SELECT customer_id FROM reviews_by_date_star WHERE review_date IN ({date_list_formatted}) AND verified_purchase=true;")
        return [{"customer_id": i[0]} for i in get_n_most_productive(res, n)]

    def n_best(self, fraction, n):
        res = self.session.execute(f"SELECT * FROM bookstore.reviews_by_fraction_of_five WHERE fraction_of_five={fraction} LIMIT {n};")
        return jsonify(res)

    def n_most_productive_haters(self, date_from, date_to, n):
        date_list_formatted = ",".join(date_range_to_list(date_from, date_to))
        res = self.session.execute(
            f"SELECT customer_id FROM reviews_by_date_star WHERE review_date IN ({date_list_formatted}) AND verified_purchase in (true, false) AND star_rating <=2;")
        return [{"customer_id": i[0]} for i in get_n_most_productive(res, n)]

    def n_most_productive_backers(self, date_from, date_to, n):
        date_list_formatted = ",".join(date_range_to_list(date_from, date_to))
        res = self.session.execute(
            f"SELECT customer_id FROM reviews_by_date_star WHERE review_date IN ({date_list_formatted}) AND verified_purchase in (true, false) AND star_rating >= 4;")
        return [{"customer_id": i[0]} for i in get_n_most_productive(res, n)]
