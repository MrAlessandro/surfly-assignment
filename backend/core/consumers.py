# myapp/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

# A dictionary to track connected users with user-friendly identifiers
connected_users = {}

class DrawingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the connection
        await self.accept()

        # Add the user to the drawing group
        await self.channel_layer.group_add("drawing_group", self.channel_name)

        # Initialize username with None; this will be set upon user registration
        self.username = None

    async def receive(self, text_data):
        # Parse the incoming message and handle different message types
        message = json.loads(text_data)
        message_type = message['type']
        data = message['data']

        if message_type == 'draw':
            # Broadcast drawing data to all users in the group
            await self.channel_layer.group_send(
                "drawing_group",
                {
                    'type': 'send_drawing',
                    'message': data
                }
            )
        
        elif message_type == 'register':
            # Handle user registration
            self.username = data['username']
            connected_users[self.channel_name] = self.username

            # Notify all users of the updated list of connected users
            await self.channel_layer.group_send(
                "drawing_group",
                {
                    'type': 'send_user_list',
                    'users': list(connected_users.values())
                }
            )

    async def disconnect(self, close_code):
        # Remove the user from the connected users list if they disconnect
        if self.channel_name in connected_users:
            del connected_users[self.channel_name]

        # Remove the user from the drawing group
        await self.channel_layer.group_discard("drawing_group", self.channel_name)

        # Notify all users of the updated list of connected users
        await self.channel_layer.group_send(
            "drawing_group",
            {
                'type': 'send_user_list',
                'users': list(connected_users.values())
            }
        )

    async def send_drawing(self, event):
        # Send drawing data to the client
        await self.send(text_data=json.dumps({'type': 'draw', 'data': event['message']}))

    async def send_user_list(self, event):
        # Send the user list to all connected clients
        await self.send(text_data=json.dumps({'type': 'user_list', 'users': event['users']}))
