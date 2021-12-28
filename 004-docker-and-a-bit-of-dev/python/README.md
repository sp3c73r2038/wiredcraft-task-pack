## Environment

- Python 3.9 (only required for development)
- Docker 20.10.9
- docker-compose 1.29.2

## Quick Start

```bash
$ docker build -t wiredcraft-004-api .
$ docker-compose up
```

```
$ curl -v http://localhost:3000/welcome

$ curl -v -X PUT -H 'Content-Type: application/json' -d '{"name": "your name"}'  http://localhost:3000/welcome
```

and check `X-CACHE` header in response. default cache ttl is 5 seconds.

## Trouble shoot

if pypi mirror is not reachable, replace `https://mirrors.163.com/pypi/simple` to any mirror fit.
