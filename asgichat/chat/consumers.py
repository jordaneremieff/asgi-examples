from asgitools.middlewares.broadcast import BroadcastMiddleware


class WebSocketConsumer:

    middlewares = [BroadcastMiddleware]

    def __init__(self, scope):
        self.scope = scope
        self.groups = None
        self.user = scope['user']

    async def __call__(self, receive, send):
        self.send = send
        while True:
            message = await receive()

            if message['type'] == 'websocket.connect':
                await send({'type': 'websocket.accept'})
                await self.groups.send({
                    'group': 'chat',
                    'add': self.id
                })

            elif message['type'] == 'websocket.receive':
                text = '<%s> %s' % (self.user, message['text'])
                await self.groups.send({
                    'group': 'chat',
                    'send': {'type': 'websocket.send', 'text': text}
                })

            elif message['type'] == 'websocket.disconnect':
                await self.groups.send({
                    'group': 'chat',
                    'discard': self.id
                })
