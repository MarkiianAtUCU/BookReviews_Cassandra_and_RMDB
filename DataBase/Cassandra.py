from dse.cluster import Cluster
from dse.auth import PlainTextAuthProvider


class Cassandra:
    def __init__(self, user, password, ips):
        auth_provider = PlainTextAuthProvider(user, password)
        cluster = Cluster(ips, auth_provider=auth_provider)
        self.session = cluster.connect(keyspace="bookstore")
