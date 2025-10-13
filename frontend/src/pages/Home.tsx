import type { ReactElement } from 'react';

const Home=():ReactElement=>{
  const socket = new WebSocket("ws://localhost:3000/ws/echo/");

  socket.onopen = () => {
    console.log("WebSocket is open now.");
    socket.send("Hello Server!");
  };

  socket.onmessage = (event) => {
    console.log("Message from server ", event.data);
  }

  return (
    <div>Vite + React</div>
  )
}

export default Home;