from channels.consumer import SyncConsumer


class TestConsumer(SyncConsumer):

    def websocket_connect(self, message):
        self.send({
            "type": "websocket.accept",
        })
        self.send({
            "type": "websocket.close", 
            "code": 1000
        })

    def websocket_disconnect(self, message):
        self.send({
            "type": "websocket.close", 
            "code": 1000
        })

    def websocket_receive(self, message):
        self.send({"type": "websocket.receive", "text": "test"})
