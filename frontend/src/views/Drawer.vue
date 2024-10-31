<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useUserStore } from "../stores/userStore";

// State management with the user store
const userStore = useUserStore();

// Reactive references for drawing state and WebSocket
const drawing = ref(false);
const context = ref(null);
const color = ref("black");
const size = ref(5);
const socket = ref(null);
const lastPoint = ref(null); // Keeps track of the last point to draw continuous paths
const connectedUsers = ref([]); // List of connected users

// Reference to the canvas element
const drawingCanvas = ref(null);

// Function to start drawing
const startDrawing = (event) => {
  drawing.value = true;
  context.value.beginPath();
  context.value.moveTo(event.offsetX, event.offsetY);
  lastPoint.value = { x: event.offsetX, y: event.offsetY };
};

// Function to stop drawing
const stopDrawing = () => {
  if (drawing.value && context.value) {
    context.value.closePath();
  }
  drawing.value = false;
  lastPoint.value = null;
};

// Function to draw on the canvas
const draw = (event) => {
  if (!drawing.value || !context.value) return;

  context.value.lineWidth = size.value;
  context.value.lineCap = "round";
  context.value.strokeStyle = color.value;

  context.value.lineTo(event.offsetX, event.offsetY);
  context.value.stroke();

  // Prevent path from connecting to future strokes
  context.value.beginPath();
  context.value.moveTo(event.offsetX, event.offsetY);

  lastPoint.value = { x: event.offsetX, y: event.offsetY };

  // Send drawing data to the server
  socket.value.send(
    JSON.stringify({
      type: "draw",
      data: {
        x: event.offsetX,
        y: event.offsetY,
        color: color.value,
        size: size.value,
        username: userStore.username,
      },
    })
  );
};

// Function to handle incoming WebSocket messages
const handleSocketMessage = (event) => {
  let data = JSON.parse(event.data);
  console.log("Received message:", data);

  if (data.type === "draw") {
    data = data.data; // Extract the data object

    if (context.value) {
      // Ensure data contains necessary properties
      if (
        data.x !== undefined &&
        data.y !== undefined &&
        data.color &&
        data.size &&
        data.username !== userStore.username
      ) {
        context.value.lineWidth = data.size;
        context.value.strokeStyle = data.color;
        context.value.lineCap = "round";

        // Draw from the last point to the current point
        if (lastPoint.value) {
          context.value.beginPath();
          context.value.moveTo(lastPoint.value.x, lastPoint.value.y);
        } else {
          context.value.beginPath();
          context.value.moveTo(data.x, data.y);
        }

        context.value.lineTo(data.x, data.y);
        context.value.stroke();

        // Update the last point
        lastPoint.value = { x: data.x, y: data.y };
      } else {
        console.error("Invalid drawing data received:", data);
      }
    }
  } else if (data.type === "user_list") {
    console.log("Connected users:", data.users);
    connectedUsers.value = data.users;
  } else {
    console.log("Unknown message type:", data.type);
  }
};

// onMounted lifecycle hook to set up the canvas and WebSocket
onMounted(() => {
  if (drawingCanvas.value) {
    context.value = drawingCanvas.value.getContext("2d");
  }

  // Initialize WebSocket connection
  socket.value = new WebSocket("ws://localhost:8000/ws/drawing/");

  socket.value.onopen = () => {
    socket.value.send(
      JSON.stringify({
        type: "register",
        data: { username: userStore.username },
      })
    );
  };

  socket.value.onmessage = handleSocketMessage;

  socket.value.onclose = () => {
    console.log("WebSocket connection closed");
  };

  socket.value.onerror = (error) => {
    console.error("WebSocket error:", error);
  };
});

// Clean up WebSocket on component unmount
onBeforeUnmount(() => {
  if (socket.value) {
    socket.value.close();
  }
});
</script>

<template>
  <canvas
    ref="drawingCanvas"
    @mousedown="startDrawing"
    @mousemove="draw"
    @mouseup="stopDrawing"
    @mouseleave="stopDrawing"
    width="800"
    height="600"></canvas>
  <div v-for="(user, index) in connectedUsers" :key="index" class="user-label">
    {{ user }}
  </div>
</template>

<style scoped>
canvas {
  border: 1px solid #000;
  cursor: crosshair;
}

.user-label {
  color: white;
}
</style>
