class HttpResponse:

    __slots__ = ("scope", "body", "more_body", "status", "headers")

    def __init__(
        self, scope, body=b"", more_body=False, status=200, headers=[[b"content-type", b"text/plain"]]
    ):
        self.scope = scope
        if not isinstance(body, bytes):
            body = body.encode()
        self.body = body
        self.more_body = more_body
        self.status = status
        self.headers = headers

    async def __call__(self, receive, send):
        await send(
            {
                "type": "http.response.start",
                "status": self.status,
                "headers": self.headers,
            }
        )
        await send(
            {"type": "http.response.body", "body": self.body, "more_body": self.more_body}
        )
