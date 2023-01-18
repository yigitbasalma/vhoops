#!/usr/bin/python
# -*- coding: utf-8 -*-

from couchbase.cluster import Cluster
from couchbase.auth import PasswordAuthenticator
from couchbase.options import ClusterOptions
from couchbase.exceptions import DocumentNotFoundException, DocumentExistsException
from json import dumps, loads

from vhoops.external.x_tools import calculate_hash


class NoSQL(object):
    def __init__(self, app):
        cluster = Cluster(
            app.config["CACHE_CONN_STRING"],
            ClusterOptions(
                authenticator=PasswordAuthenticator(
                    username=app.config["CACHE_USERNAME"],
                    password=app.config["CACHE_PASSWORD"]
                )
            )
        )

        self.buckets = dict()
        for bucket in app.config["CACHE_BUCKETS"]:
            self.buckets[bucket] = cluster.bucket(bucket)

    def write_key(self, bucket, cache_key, cache_value, prefix, ttl):
        try:
            self.buckets[bucket].insert(
                prefix + "-" + calculate_hash(cache_key),
                dumps(cache_value),
                ttl=ttl
            )
        except DocumentExistsException:
            self.buckets[bucket].replace(
                prefix + "-" + calculate_hash(cache_key),
                dumps(cache_value),
                ttl=ttl
            )

    def read_key(self, bucket, cache_key, prefix):
        try:
            return loads(
                self.buckets[bucket].get(
                    prefix + "-" + calculate_hash(cache_key)
                ).value
            )
        except DocumentNotFoundException:
            pass

    def delete_key(self, bucket, cache_key, prefix):
        try:
            self.buckets[bucket].remove(
                prefix + "-" + calculate_hash(cache_key)
            )
        except DocumentNotFoundException:
            pass
