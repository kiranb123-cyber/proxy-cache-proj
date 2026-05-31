# Caching Proxy Server

A CLI-based caching proxy server built with Python and Flask. It forwards HTTP requests to an origin server and caches the responses — meaning repeat requests are served from the cache instead of hitting the origin again.

## How It Works

When a request comes in, the proxy checks an in-memory cache first:

- **Cache MISS** — the request hasn't been seen before, so it's forwarded to the origin server. The response is stored in the cache and returned to the client with an `X-Cache: MISS` header.
- **Cache HIT** — the request has been seen before, so the cached response is returned immediately with an `X-Cache: HIT` header, without touching the origin server.

## Requirements

- Python 3.x
- Flask
- Requests

Install dependencies:

```bash
pip install flask requests
```

## Usage

### Start the proxy server

```bash
python main.py --port <number> --origin <url>
```

For example:

```bash
python main.py --port 3000 --origin http://dummyjson.com
```

This starts the proxy on port 3000. Any request to `http://localhost:3000/products` will be forwarded to `http://dummyjson.com/products`.

### Clear the cache

```bash
python main.py --clear-cache
```

### Testing

Make a request and inspect the `X-Cache` header:

```bash
curl -v http://localhost:3000/products
```

The first request will return `X-Cache: MISS`, and the second will return `X-Cache: HIT`.

## Limitations

The cache is in-memory, meaning it is cleared when the server restarts. A future improvement would be to swap the in-memory cache for Redis to enable persistent caching across restarts.

## What I Learned

- How HTTP proxy servers work under the hood
- CLI argument parsing with `argparse`


## Future Additions

- Add redis for caching
- adding tests to ensure functions work