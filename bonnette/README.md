# Bonnette

ASGI adapter for Azure Functions.

**Requirements**: Python 3.6

## Installation

```shell
$ pip3 install bonnette
```

## Example

Bonnette consists of a single adapter class for using ASGI applications on Azure Functions, example usage:

```python
from bonnette import Bonnette


class App:
    def __init__(self, scope):
        self.scope = scope

    async def __call__(self, receive, send):
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [[b"content-type", b"text/plain"]],
            }
        )
        await send({"type": "http.response.body", "body": b"Hello, world!"})


handler = Bonnette(App)
```

## Dependencies

`azure-functions` - *required* for Azure Function support.

## Frameworks

Any ASGI framework should work with Bonnette, however there are cases where certain non-ASGI behaviour of an application will causes issues when deploying to a serverless platform.

## Support

This adapter was originally part of [Mangum](https://github.com/erm/mangum), a project for ASGI support on AWS Lambda & API Gateway. It was forked because I'd rather focus on supporting a single platform well, Bonnette will likely not get as much attention unless there becomes a strong interest by others in using it.