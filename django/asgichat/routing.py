from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter

from chat.consumers import TestConsumer


application = ProtocolTypeRouter({
    "websocket":
    URLRouter(
        [
            # URLRouter just takes standard Django path() or url() entries.
            url(r"chat/stream/", TestConsumer)
        ]
    )

})
