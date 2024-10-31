# myapp/routing.py

from django.urls import re_path
from .consumers import DrawingConsumer  # Replace with your actual consumer

websocket_urlpatterns = [
    re_path(r'ws/drawing/$', DrawingConsumer.as_asgi()),  # Adjust the URL pattern as needed
]
