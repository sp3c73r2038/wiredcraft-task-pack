# -*- coding: utf-8 -*-
import os
import pprint
import time

import pytest

import server


def setup():
    server.setupLogging(True)

@pytest.fixture
def client():
    app = server.server

    # config for testing
    app.config['UNIT_TEST'] = True
    app.config['CACHE_TTL'] = 1
    app.testing = True

    with app.test_client() as client:
        with app.app_context():
            server.init()
        yield client

def test_initial(client):
    """initial value"""

    rv = client.get('/welcome')
    assert b'Hello, John Doe' in rv.data

def test_put_missing_header(client):
    # missing/wrong header
    rv = client.put('/welcome')
    assert rv.status_code == 400
    assert b'application/json' in rv.data

def test_put_missing_body(client):
    rv = client.put('/welcome', headers={
        'Content-Type': 'application/json',
    })
    assert rv.status_code == 400
    assert b'invalid JSON' in rv.data

def test_put_invalid_json(client):
    # invalid json
    rv = client.put('/welcome', headers={
        'Content-Type': 'application/json',
    }, data='hello')
    assert rv.status_code == 400
    assert b'invalid JSON' in rv.data

def test_put_ok(client):
    # invalid json
    rv = client.put('/welcome', headers={
        'Content-Type': 'application/json',
    }, data='{"name": "hello"}')
    assert rv.status_code == 200
    assert b'update ok' in rv.data

    rv = client.get('/welcome')
    assert b'Hello, hello' in rv.data

def test_get_cache_hit(client):
    """
    test get cache
    """

    # first time, miss
    rv = client.get('/welcome')
    assert rv.headers['X-CACHE'] == 'Miss'

    # second time, hit
    rv = client.get('/welcome')
    assert rv.headers['X-CACHE'] == 'Hit'

    # cache expired
    time.sleep(1)
    rv = client.get('/welcome')
    assert rv.headers['X-CACHE'] == 'Miss'
