# asgi-examples

This repository exists to provide proof-of-concept implementations of the ASGI specification in an attempt to help encourage its adoption by the maintainers and developers of existing projects. The example adapters are not intended to be robust, complete solutions for integrating ASGI into existing Python frameworks - they are simple demonstrations to help others learn more about ASGI.


**Current examples include the following frameworks**: 

- Django [Channels]

- [Flask]

- [aiohttp]

- [afiqah]

- [Pyramid]

- [Quart]



Please open an issue if you would like to see a specific framework example.


## Running

You will need to use either [uvicorn] or [daphne] to run the ASGI server. 

```shell
$ uvicorn apps._<framework>:app
```

```shell
$ daphne apps._<framework>:app
```


## todo

- More examples
- Tests
- Simplify running examples


[Channels]: https://github.com/django/channels/
[Afiqah]: https://github.com/afiqah/afiqah/
[uvicorn]: https://github.com/encode/uvicorn/
[daphne]: https://github.com/django/daphne/
[Flask]: https://github.com/pallets/flask/
[aiohttp]: https://github.com/aio-libs/aiohttp/
[Pyramid]: https://github.com/Pylons/pyramid/
[Quart]: https://gitlab.com/pgjones/quart/