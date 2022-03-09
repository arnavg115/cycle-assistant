const express = require("express");
const app = express();
const http = require("http");
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

app.get("/", (req, res) => {
  res
    .send(
      `<script src="/socket.io/socket.io.js"></script>
  <script>
    var socket = io();
  </script>`
    )
    .type("html");
});

io.on("connection", (socket) => {
  console.log("a user connected");
  setTimeout(() => socket.emit("my_message", { gello: "sello" }), 5000);
  socket.on("my response", (daa) => {
    console.log(daa);
  });
  socket.on("button_pressed", (data) => {
    console.log(data);
  });
});

server.listen(3000, "0.0.0.0", () => {
  console.log("listening on *:3000");
});
