const express = require("express");
const app = express();
const http = require("http");
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

app.use(express.static("public"));

const lats = [];
app.get("/users", (req, res) => {
  console.log(lats);
  res.send(lats);
});

io.on("connection", (socket) => {
  socket.on("gps", (lat) => {
    lats.push(lat);
  });
});

server.listen(3000, "0.0.0.0", () => {
  console.log("listening on *:3000");
});
