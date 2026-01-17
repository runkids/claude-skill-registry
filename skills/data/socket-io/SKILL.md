---
name: socket-io
description: Real-time communication with Socket.IO including connection management, events, rooms, and error handling. Use when working on TitanMirror or any real-time applications.
---

# 🔌 Socket.IO Skill

## Server Setup (Node.js)

```javascript
const { Server } = require('socket.io');
const io = new Server(server, {
  cors: { origin: '*' },
  pingTimeout: 60000,
  pingInterval: 25000
});

io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);
  
  socket.on('disconnect', (reason) => {
    console.log('Disconnected:', reason);
  });
});
```

---

## Client Setup

### JavaScript
```javascript
const socket = io('http://localhost:3000');

socket.on('connect', () => {
  console.log('Connected!', socket.id);
});

socket.on('connect_error', (err) => {
  console.error('Connection error:', err.message);
});
```

### Android (Kotlin)
```kotlin
val options = IO.Options().apply {
    reconnection = true
    reconnectionAttempts = 5
    reconnectionDelay = 1000
}
val socket = IO.socket("http://192.168.1.x:3000", options)
socket.connect()
```

---

## Event Patterns

### Emit & Listen
```javascript
// Client → Server
socket.emit('frame', { data: base64Image });

// Server → Client
io.emit('command', { type: 'click', x: 100, y: 200 });

// Server → Specific client
io.to(socketId).emit('private', { message: 'hello' });
```

### Acknowledgement
```javascript
// Client
socket.emit('upload', file, (response) => {
  console.log('Server confirmed:', response);
});

// Server
socket.on('upload', (file, callback) => {
  saveFile(file);
  callback({ success: true });
});
```

---

## Rooms

```javascript
// Join room
socket.join('device-' + deviceId);

// Send to room
io.to('device-' + deviceId).emit('frame', frameData);

// Leave room
socket.leave('device-' + deviceId);
```

---

## Binary Data (TitanMirror)

```javascript
// Server receives frame
socket.on('frame', (data) => {
  // data is Buffer or ArrayBuffer
  const buffer = Buffer.from(data);
  broadcastFrame(buffer);
});

// Client sends frame (Android)
val bytes = compressToJPEG(bitmap)
socket.emit("frame", bytes)
```

---

## Error Handling

```javascript
socket.on('connect_error', (error) => {
  if (error.message === 'xhr poll error') {
    // Network issue - will auto-retry
  }
});

socket.on('disconnect', (reason) => {
  if (reason === 'io server disconnect') {
    socket.connect(); // Manual reconnect
  }
});
```

---

## Performance Tips

| Tip | Why |
|-----|-----|
| Use binary instead of base64 | 33% smaller |
| Compress images (JPEG 50%) | Reduce bandwidth |
| Debounce frequent events | Prevent flooding |
| Use rooms for targeting | Avoid broadcast all |
