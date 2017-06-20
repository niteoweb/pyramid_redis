# -*- coding: utf-8 -*-
"""Tests for Redis Pyramid factory."""

from __future__ import unicode_literals
from pyramid import testing
from pyramid.interfaces import IRequestExtensions

import fakeredis
import pytest


@pytest.fixture()
def pyramid_config():
    config = testing.setUp(settings={
        'redis.dsn': 'fakeredis://localhost:6379',
    })
    config.include('pyramid_redis')
    yield config
    testing.tearDown()
    fakeredis.FakeStrictRedis().flushall()


def test_redis_present(pyramid_config):
    exts = pyramid_config.registry.getUtility(IRequestExtensions)
    assert 'redis' in exts.descriptors


def test_redis_native():
    config = testing.setUp(settings={
        'redis.dsn': 'redis://localhost:6379',
    })
    config.include('pyramid_redis')
    exts = config.registry.getUtility(IRequestExtensions)
    assert 'redis' in exts.descriptors
    testing.tearDown()


def test_redis_native_blocking():
    config = testing.setUp(settings={
        'redis.dsn': 'redis+blocking://localhost:6379',
    })
    config.include('pyramid_redis')
    exts = config.registry.getUtility(IRequestExtensions)
    assert 'redis' in exts.descriptors
    testing.tearDown()


def test_redis_fail(caplog):
    config = testing.setUp(settings={
        'redis.dsn': 'fail://localhost:6379',
    })
    config.include('pyramid_redis')
    exts = config.registry.getUtility(IRequestExtensions)
    assert 'redis' in exts.descriptors
    assert 'Redis could not be initialized, DSN fail' in caplog.text
    testing.tearDown()
