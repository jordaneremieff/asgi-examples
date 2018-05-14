# asgi-examples

This repository exists to provide proof-of-concept implementations of the ASGI specification in an attempt to help encourage its adoption by the maintainers and developers of existing projects. The example adapters are not robust, complete solutions for integrating ASGI into existing Python frameworks - they are intended to be simple demonstrations based on my personal understanding of ASGI at this point.

Please open an issue if you would like to see a specific framework example.

## Running

You will need to use either [uvicorn] or [daphne] to run the ASGI server. 

```shell
$ uvicorn <file>:<appname>
```

```shell
$ daphne <file>:<appname>
```

## Examples

### Django

A simple Django [Channels] websocket app.

### Flask

A [Flask] app and ASGI adapter providing http & websocket consumer support.

### AioHttp

An [aiohttp] app and ASGI adapter providing http consumer support. (todo: websocket)

### Afiqah

An example of a pure ASGI app using the [Afiqah] microframework.


[Channels]: https://github.com/django/channels/
[Afiqah]: https://github.com/afiqah/afiqah/
[uvicorn]: https://github.com/encode/uvicorn/
[daphne]: https://github.com/django/daphne/
[Flask]: https://github.com/pallets/flask/
[aiohttp]: https://github.com/aio-libs/aiohttp/