## Environment

- Gentoo Linux (any modern GNU/Linux will do)
- Docker 20.10.9
- docker-compose v1.29.2

## Basic Info

`/welcome` API will return with a response header `X-CACHE` indicating whether the data is from cache.

## File Content

```
├── python      # python implementation
└── openapi.yml # OpenAPI definition for API service
```

Fill the content of `openapi.yml` into https://editor.swagger.io/ to read API doc.

`cd` into implemented folder and follow the coresponding `README`.
