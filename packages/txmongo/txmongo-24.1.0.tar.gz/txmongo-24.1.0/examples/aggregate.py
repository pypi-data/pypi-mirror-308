#!/usr/bin/env python
# coding: utf-8
# Copyright 2009-2014 The txmongo authors.  All rights reserved.
# Use of this source code is governed by the Apache License that can be
# found in the LICENSE file.

import _local_path
from twisted.internet import defer, reactor

import txmongo


@defer.inlineCallbacks
def example():
    mongo = yield txmongo.MongoConnection()

    foo = mongo.foo  # `foo` database
    test = foo.test  # `test` collection

    yield test.insert_many(
        [
            {"src": "Twitter", "content": "bla bla"},
            {"src": "Twitter", "content": "more data"},
            {"src": "Wordpress", "content": "blog article 1"},
            {"src": "Wordpress", "content": "blog article 2"},
            {"src": "Wordpress", "content": "some comments"},
        ]
    )

    # Read more about the aggregation pipeline in MongoDB's docs
    pipeline = [{"$group": {"_id": "$src", "content_list": {"$push": "$content"}}}]
    result = yield test.aggregate(pipeline)

    print(("result:", result))


if __name__ == "__main__":
    example().addCallback(lambda ign: reactor.stop())
    reactor.run()
