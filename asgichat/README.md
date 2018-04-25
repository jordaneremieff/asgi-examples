# asgichat

An example of using Django [Channels] with custom protocol and routing components from [asgitools]. 


# Running

Run the server using uvicorn:

```shell
$ uvicorn asgichat.asgi:application
```

or daphne

```shell
$ daphne asgichat.asgi:application
```

or runserver (uses daphne)

```shell
$ ./manage.py runserver
```

[Channels]: https://github.com/django/channels/
[asgitools]: https://github.com/erm/asgitools
