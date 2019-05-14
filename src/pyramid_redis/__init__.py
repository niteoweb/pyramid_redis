# -*- coding: utf-8 -*-
"""Provide a Pyramid request factory for redis."""

from __future__ import unicode_literals

import logging


logger = logging.getLogger(__name__)


def includeme(config):
    """Factory for Redis pyramid client."""

    dsn = config.registry.settings.get('redis.dsn')
    max_connections = config.registry.settings.get('redis.max_connections', 4)
    redis_client = None

    is_type = lambda name: dsn.startswith(name+'://')
    if any(is_type(t) for t in ['redis', 'rediss', 'unix']):
        from redis import StrictRedis

        redis_client = StrictRedis.from_url(dsn)
    elif any(is_type(t + '+blocking') for t in ['redis', 'rediss', 'unix']):
        from redis import BlockingConnectionPool
        from redis import StrictRedis

        # Strip the +blocking from dns, underlaying client
        # does not support this scheme.
        dsn = dsn.replace('+blocking:', ':')
        pool = BlockingConnectionPool.from_url(
            dsn, max_connections=max_connections)
        redis_client = StrictRedis(connection_pool=pool)
    elif is_type('fakeredis'):
        import fakeredis

        server = fakeredis.FakeServer()
        redis_client = fakeredis.FakeStrictRedis(server=server)

        config.registry.settings["fakeredis_server"] = server
    else:
        logger.error(
            'Redis could not be initialized, DSN %s is not supported!', dsn)


    # Create a request method that'll get the Redis client in each request.
    config.add_request_method(
        lambda request: redis_client,
        name='redis',
        reify=True,
    )
