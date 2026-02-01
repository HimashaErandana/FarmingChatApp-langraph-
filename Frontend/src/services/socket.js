import { io } from "socket.io-client";

const socket = io("http://127.0.0.1:8000", { autoConnect: false });

// Connect manually
socket.connect();

socket.on("connect", () => {
  console.log("Connected", socket.id);
});

export default socket;