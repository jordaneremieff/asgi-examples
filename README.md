# asgi-examples

[ASGI (Asynchronous Server Gateway Interface)](https://asgi.readthedocs.io/) examples and information.

## ASGI application example

Here are two examples of writing an ASGI application in its simplest form.

```python

def app(scope):
    async def asgi(receive, send):
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [[b"content-type", b"text/plain"]],
            }
        )
        await send({"type": "http.response.body", "body": b"Hello, world!"})

    return asgi
```

```python
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
```


## Frameworks / Adapters / Middlewares

Below are various frameworks, adapters, and middlewares that use ASGI.

- [Channels](https://github.com/django/channels/)
- [Starlette](https://github.com/encode/starlette/)
- [Quart](https://gitlab.com/pgjones/quart/)
- [Quart Trio](https://gitlab.com/pgjones/quart-trio/)
- [Asgish](https://github.com/almarklein/asgish/)
- [FastAPI](https://github.com/tiangolo/fastapi/)
- [Responder](https://github.com/kennethreitz/responder/)
- [Lemon](https://github.com/joway/lemon/)
- [Nardis](https://github.com/yoongkang/nardis)
- [Bocadillo](https://github.com/bocadilloproject/bocadillo)
- [Sentry ASGI](https://github.com/encode/sentry-asgi)
- [Mangum](https://github.com/erm/mangum)
- [Bonnette](https://github.com/erm/bonnette)

## Servers

- [Uvicorn](https://github.com/encode/uvicorn/)
- [Hypercorn](https://gitlab.com/pgjones/hypercorn/)
- [Daphne](https://github.com/django/daphne/)

## Tools

- [uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)
- [uvicorn-gunicorn-starlette-docker](https://github.com/tiangolo/uvicorn-gunicorn-starlette-docker)
- [uvicorn-gunicorn-docker](https://github.com/tiangolo/uvicorn-gunicorn-docker)
- [asgi-scope](https://github.com/simonw/asgi-scope)

### Running the applications

An ASGI server is required to run the examples. For example, to run an application using `uvicorn`, use the following command:

```shell
$ uvicorn app:app
```

### Reference

Below are links to various ASGI-related projects and information. 

#### Specification

- [ASGI (Asynchronous Server Gateway Interface) docs](https://asgi.readthedocs.io/)
- [asgiref](https://github.com/django/asgiref/)

#### Misc

- [A Django Async Roadmap](https://www.aeracode.org/2018/06/04/django-async-roadmap/)
- [Writing an ASGI Web Framework](https://yoongkang.com/blog/writing-an-asgi-web-framework/)
- [Embracing ASGI with Quart; Introducing Hypercorn](https://medium.com/@pgjones/embracing-asgi-with-quart-introducing-hypercorn-652cb6b269f5)
- [Quart; an ASGI alternative to Flask](https://medium.com/@pgjones/quart-an-asgi-alternative-to-flask-53915868d220)
- [An Asyncio socket tutorial](https://medium.com/@pgjones/an-asyncio-socket-tutorial-5e6f3308b8b0)
- [Pyramid cookbook recipe](https://docs.pylonsproject.org/projects/pyramid-cookbook/en/latest/deployment/asgi.html)
- [Quart-Trio - A Trio based HTTP Framework](https://medium.com/@pgjones/quart-trio-9415d7c1928a)
- [Hello, ASGI - Introduction to the emerging ASGI standard](https://www.encode.io/articles/hello-asgi/)
- [Working with ASGI and HTTP](https://www.encode.io/articles/asgi-http/)
- [Working with HTTP requests in ASGI](https://www.encode.io/articles/working-with-http-requests-in-asgi/)

#### Discussions

- [Gunicorn issue](https://github.com/benoitc/gunicorn/issues/1380)
- [Werkzeug issue](https://github.com/pallets/werkzeug/issues/1322)
- [Pyramid issue](https://github.com/Pylons/pyramid/issues/2603)
- [Vibora issue](https://github.com/vibora-io/vibora/issues/14)
- [Sanic issue](https://github.com/huge-success/sanic/pull/1265)

## Contributing

Please open an issue or pull request if you would like to contribute to the examples or README. The issue tracker may also be used for any informal ASGI-related discussions or questions.