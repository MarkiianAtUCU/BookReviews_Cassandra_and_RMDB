import mysql.connector as sql


class MySQL:
    def __init__(self, user, password, ip):
        self.conn = sql.connect(host=ip, user=password, password=password, database='bookstore')
        self.cursor = self.conn.cursor()

    def reviews_by_product(self, product_id):
        self.cursor.execute(f"SELECT * FROM review WHERE product_id={product_id};")
        return [dict(zip(self.cursor.column_names, i)) for i in self.cursor.fetchall()]

    def reviews_by_product_rating(self, product_id, star_rating):
        self.cursor.execute(f"SELECT * FROM review WHERE product_id={product_id} AND star_rating={star_rating};")
        return [dict(zip(self.cursor.column_names, i)) for i in self.cursor.fetchall()]

    def reviews_by_customer(self, customer_id):
        self.cursor.execute(f"SELECT * FROM review WHERE customer_id={customer_id};")
        return [dict(zip(self.cursor.column_names, i)) for i in self.cursor.fetchall()]

    def n_most_reviewed(self, date_from, date_to, n):
        self.cursor.execute(
            f"SELECT product_id, category.name as product_category, product.title as product_title FROM review"
            f"LEFT JOIN product ON review.product_id=product.id"
            f"LEFT JOIN category ON product.category_id=category.id"
            f"WHERE date >= {date_from} AND date <= {date_to}"
            f"GROUP BY product_id ORDER BY count(*) DESC LIMIT {n};"
        )
        return [dict(zip(self.cursor.column_names, i)) for i in self.cursor.fetchall()]

    def n_most_productive(self, date_from, date_to, n):
        self.cursor.execute(
            f"SELECT customer_id FROM review"
            f"WHERE date >= {date_from} AND date <= {date_to}"
            f"GROUP BY customer_id ORDER BY count(*) DESC LIMIT {n};"
        )
        return [dict(zip(self.cursor.column_names, i)) for i in self.cursor.fetchall()]

    def n_best(self, fraction, n):
        self.cursor.execute(
            f"SELECT subq.product_id, subq.product_category, subq.product_title, subq.fraction_of_five FROM"
            f"(SELECT product_id, category.name as product_category, product.title as product_title,"
            f"ROUND(COUNT(case when star_rating=5 then product_id end) / COUNT(*),3) as fraction_of_five,"
            f"COUNT(*) as total_reviews"
            f"FROM review"
            f"LEFT JOIN product ON review.product_id=product.id"
            f"LEFT JOIN category ON product.category_id=category.id"
            f"WHERE verified_purchase=true"
            f"GROUP BY product_id) AS subq"
            f"WHERE subq.fraction_of_five = {fraction} AND subq.total_reviews >= 100"
            f"ORDER BY fraction_of_five DESC LIMIT {n};"

        )
        return [dict(zip(self.cursor.column_names, i)) for i in self.cursor.fetchall()]

    def n_most_productive_haters(self, date_from, date_to, n):
        self.cursor.execute(
            f"SELECT customer_id FROM review"
            f"WHERE date >= {date_from} AND date <= {date_to} AND star_rating<=2"
            f"GROUP BY customer_id ORDER BY count(*) DESC LIMIT {n};"
        )
        return [dict(zip(self.cursor.column_names, i)) for i in self.cursor.fetchall()]

    def n_most_productive_backers(self, date_from, date_to, n):
        self.cursor.execute(
            f"SELECT customer_id FROM review"
            f"WHERE date >= {date_from} AND date <= {date_to} AND star_rating>=4"
            f"GROUP BY customer_id ORDER BY count(*) DESC LIMIT {n};"
        )
        return [dict(zip(self.cursor.column_names, i)) for i in self.cursor.fetchall()]
