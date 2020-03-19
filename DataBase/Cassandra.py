from dse.cluster import Cluster
from dse.auth import PlainTextAuthProvider
from collections import Counter
from datetime import datetime, timedelta


def get_n_most_reviewed(res, n):
    return Counter(map(lambda x: x.product_id, res)).most_common(n)


def get_n_most_productive(res, n):
    return Counter(map(lambda x: x.customer_id, res)).most_common(n)


def jsonify(row_list):
    res = []
    for i in row_list:
        res.append(dict(i._asdict()))
    for i in res:
        if 'review_date' in i:
            i['review_date'] = str(i['review_date'])
    return res


def date_range_to_list(date_from, date_to):
    res = []
    dt_date_from = datetime.strptime(date_from, '%Y-%m-%d')
    dt_date_to = datetime.strptime(date_to, '%Y-%m-%d')
    step = timedelta(days=1)

    while dt_date_from <= dt_date_to:
        res.append("'" + str(dt_date_from.date()) + "'")
        dt_date_from += step
    return res


class Cassandra:
    def __init__(self, user, password, ips):
        auth_provider = PlainTextAuthProvider(user, password)
        cluster = Cluster(ips, auth_provider=auth_provider)
        self.session = cluster.connect(keyspace="bookstore")

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
            f"SELECT product_id FROM reviews_by_date_star WHERE review_date IN ({date_list_formatted});"
        )
        result_product_id = ", ".join([f"'{i[0]}'" for i in get_n_most_reviewed(res, n)])
        res = self.session.execute(
            f"SELECT product_id, product_category, product_title FROM bookstore.reviews_by_product WHERE product_id in ({result_product_id}) GROUP BY product_id;"
        )
        return jsonify(res)

    def n_most_productive(self, date_from, date_to, n):
        date_list_formatted = ",".join(date_range_to_list(date_from, date_to))
        res = self.session.execute(
            f"SELECT customer_id FROM reviews_by_date_star WHERE review_date IN ({date_list_formatted}) AND verified_purchase=true;"
        )
        return [{"customer_id": i[0]} for i in get_n_most_productive(res, n)]

    def n_best(self, fraction, n):
        res = self.session.execute(
            f"SELECT * FROM reviews_by_fraction_of_five WHERE fake_partition IN (0, 1) AND fraction_of_five={fraction} LIMIT {n};"
        )
        return jsonify(res)

    def n_most_productive_haters(self, date_from, date_to, n):
        date_list_formatted = ",".join(date_range_to_list(date_from, date_to))
        res = self.session.execute(
            f"SELECT customer_id FROM reviews_by_date_star WHERE review_date IN ({date_list_formatted}) AND verified_purchase in (true, false) AND star_rating <=2;"
        )
        return [{"customer_id": i[0]} for i in get_n_most_productive(res, n)]

    def n_most_productive_backers(self, date_from, date_to, n):
        date_list_formatted = ",".join(date_range_to_list(date_from, date_to))
        res = self.session.execute(
            f"SELECT customer_id FROM reviews_by_date_star WHERE review_date IN ({date_list_formatted}) AND verified_purchase in (true, false) AND star_rating >= 4;"
        )
        return [{"customer_id": i[0]} for i in get_n_most_productive(res, n)]
