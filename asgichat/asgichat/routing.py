from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack

from asgitools.routing import (
    AsgiProtocolRouter,
    AsgiProtocol,
    AsgiUrlRouter,
    AsgiUrlRoute,
)

from chat.consumers import WebSocketConsumer


application = AsgiProtocolRouter([
    AsgiProtocol(
        'http',
        AsgiHandler
    ),
    AsgiProtocol(
        'websocket',
        AuthMiddlewareStack(AsgiUrlRouter([
            AsgiUrlRoute(
                '/chat/stream/', WebSocketConsumer
            ),
        ])),
    ),
])
