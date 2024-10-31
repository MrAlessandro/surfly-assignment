# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import core.routing  # Replace with your app name and routing module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'surfly_assignment_backend.settings')  # Replace 'myproject' with your project name

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
            core.routing.websocket_urlpatterns  # Replace with the appropriate routing configuration
        ),
})
