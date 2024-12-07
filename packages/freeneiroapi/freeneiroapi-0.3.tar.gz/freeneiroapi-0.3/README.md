from build.lib.freeneiroapi import FreeNeiroAPIfrom http.client import responses

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
from freeneiroapi import FreeNeiroAPI
api = FreeNeiroAPI()
response = api.get_response("Hello!")
print(response)
```
