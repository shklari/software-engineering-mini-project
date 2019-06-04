from channels.routing import ProtocolTypeRouter , URLRouter
from django.urls import path

from MarketingSystem.consumers import ChatConsumer


application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/", ChatConsumer),
    ])
})