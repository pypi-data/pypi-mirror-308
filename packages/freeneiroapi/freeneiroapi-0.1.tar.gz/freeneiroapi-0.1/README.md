from http.client import responses

# FreeNeiroAPI

FreeNeiroAPI is a library for interacting with the DuckGPT API.

## Installation:

```bash
pip install freeneiroapi
```

## Dependencies:

```
requests
```

## Using:

```python
import freeneiroapi
api = freeneiroapi()
response = api.get_response("Hello!")
print(response)
```
