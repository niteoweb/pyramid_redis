[![Build Status](https://travis-ci.org/dz0ny/pyramid_redis.svg?branch=master)](https://travis-ci.org/dz0ny/pyramid_redis)

[pyramid_redis][] is one specific way of integrating [redis-py][] with a
[Pyramid][] web application.

### Features

* provides a redis client at `request.redis`
* blocking connection pool
* fakeredis integration

NOTE: This package should not be used if you plan to use MULTI/EXEC or PUB/SUB commands. Since those are not thread-safe and will cause issues in multi threaded app. You are however free to use custom client for such case.
### Example

```python
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config

import os

@view_config(route_name='hello', renderer='string', request_method="GET")
def get_hello(request):
    return 'Hello {0}'.format(request.redis.get('name'))

@view_config(route_name='hello', renderer='string', request_method="POST")
def set_hello(request):
    name = request.POST.get(name)
    request.redis.set(name)
    return 'Hello set to {0}'.format(name)

if __name__ == '__main__':
    config = Configurator()
    config.add_settings({'redis.dsn': os.environ.get('REDIS_DSN')})
    config.add_route('hello', '/')
    config.include('pyramid_redis')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
```

### Usage

To use, `pip install pyramid_redis` / add `pyramid_redis` to your requirements.txt
and then [include][] the package:

    config.include('pyramid_redis')

### Configuration

Requires one of the the following [INI setting][]:

* Redis over TCP, using database 0:
```
redis.dsn=redis://[:password]@localhost:6379/0
redis.max_connections=4
```

* Redis over SSL wrapped TCP, using database 1:
`redis.dsn=rediss://[:password]@localhost:6379/1`

* Unix Domain Socket using database 0
`redis.dsn=unix://[:password]@/path/to/socket.sock?db=0`


#### Using BlockingPool

* Redis over TCP, using database 5 with BlockingPool:
```
redis.dsn=redis+blocking://[:password]@localhost:6379/5
redis.max_connections=100
```

* Unix Domain Socket using database 5 with BlockingPool:
`redis.dsn=unix+blocking://[:password]@/path/to/socket.sock?db=5`

* Unix Domain Socket using database 3 with BlockingPool:
`redis.dsn=rediss+blocking://[:password]@localhost:6379/3`


#### Using fakeredis for testing

* Fakeredis library, for easier testing
`redis.dsn=fakeredis://`


[pyramid_redis]: https://github.com/thruflo/pyramid_redis
[redis-py]: https://github.com/andymccurdy/redis-py
[Pyramid]: http://pypi.python.org/pypi/pyramid
