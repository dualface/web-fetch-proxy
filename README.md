# Web Fetch Proxy

FlareSolverr Adapter Service - Forward GET requests to FlareSolverr running in a container.

## Quick Start

```bash
docker compose up -d
```

## Service Ports

| Service | Port |
|------|------|
| Web Fetch Proxy | 1803 |
| FlareSolverr | 1804 |

## API Usage

```bash
curl "http://127.0.0.1:1803/fetch?url=https://example.com"
```

## Stop Service

```bash
docker compose down
```

## Proxy Configuration

To use a proxy when requesting FlareSolverr, configure it in `docker-compose.yml`:

```yaml
environment:
  - PROXY_URL=http://127.0.0.1:8888
```

Or set it when running directly:

```bash
PROXY_URL=http://127.0.0.1:8888 python app.py
```
