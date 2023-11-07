import WebSocket from 'ws';
import { WS_PORT , WS_SECURITY_KEY } from '../env';


const PORT = WS_PORT || 8080;
const SECRET_KEY = WS_SECURITY_KEY;
const wss: WebSocket.Server = new WebSocket.Server({ port: PORT });

let ws: WebSocket;

wss.on('connection', (socket, req) => {
  ws = socket;

  // Authentication step
  const authHeader = req.headers['authorization'];
  if (!authHeader || authHeader !== SECRET_KEY) {
    ws.send("Unauthorized");
    ws.terminate(); // Close the connection if no authorization header
    return;
  }

});

export function wsSendMsg(message: any) {
  if (ws) {
    ws.send(message);
  }
}

export default wsSendMsg;