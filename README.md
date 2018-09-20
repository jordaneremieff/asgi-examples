# asgi-examples

This repository exists to provide proof-of-concept implementations of the ASGI specification in an attempt to help encourage its adoption by the maintainers and developers of existing projects. The example adapters are not intended to be robust, complete solutions for integrating ASGI into existing Python frameworks - they are simple demonstrations to help others learn more about ASGI.

Please open an issue or pull request if you would like to contribute to the examples. The issue tracker may also be used for any informal ASGI-related discussions or questions.

**Current examples include the following frameworks**: 

- [Channels](https://github.com/django/channels/)

- [Flask](https://github.com/pallets/flask/)

- [Aiohttp](https://github.com/aio-libs/aiohttp/)

- [Pyramid](https://github.com/Pylons/pyramid/)

- [Quart](https://gitlab.com/pgjones/quart/)

- [Asgish](https://github.com/almarklein/asgish/)

## Running

Running an ASGI application requires an ASGI server:

- [Uvicorn](https://github.com/encode/uvicorn/)
- [Hypercorn](https://gitlab.com/pgjones/hypercorn/)
- [Daphne](https://github.com/django/daphne/)


```shell
$ <server> apps._<framework>:app
```

## Reference

Below are links to various ASGI-related projects and information. 

### Specification

- [ASGI (Asynchronous Server Gateway Interface) docs](https://asgi.readthedocs.io/)
- [asgiref](https://github.com/django/asgiref/)

### Misc

- [Pyramid cookbook recipe](https://docs.pylonsproject.org/projects/pyramid-cookbook/en/latest/deployment/asgi.html)

### Blog posts

- [A Django Async Roadmap](https://www.aeracode.org/2018/06/04/django-async-roadmap/)
- [Writing an ASGI Web Framework](https://yoongkang.com/blog/writing-an-asgi-web-framework/)
- [Embracing ASGI with Quart; Introducing Hypercorn](https://medium.com/@pgjones/embracing-asgi-with-quart-introducing-hypercorn-652cb6b269f5)
- [Quart; an ASGI alternative to Flask](https://medium.com/@pgjones/quart-an-asgi-alternative-to-flask-53915868d220)
- [An Asyncio socket tutorial](https://medium.com/@pgjones/an-asyncio-socket-tutorial-5e6f3308b8b0)

### Discussions

- [Gunicorn issue](https://github.com/benoitc/gunicorn/issues/1380)
- [Aiohttp issue](https://github.com/aio-libs/aiohttp/issues/2902)
- [Werkzeug issue](https://github.com/pallets/werkzeug/issues/1322)
- [Pyramid issue](https://github.com/Pylons/pyramid/issues/2603)
- [Vibora issue](https://github.com/vibora-io/vibora/issues/14)
- [Sanic issue](https://github.com/huge-success/sanic/issues/761)
