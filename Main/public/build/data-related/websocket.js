"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.wsSendMsg = void 0;
const ws_1 = __importDefault(require("ws"));
const env_1 = require("../env");
const PORT = env_1.WS_PORT || 8080;
const SECRET_KEY = env_1.WS_SECURITY_KEY;
const wss = new ws_1.default.Server({ port: PORT });
let ws;
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
function wsSendMsg(message) {
    if (ws) {
        ws.send(message);
    }
}
exports.wsSendMsg = wsSendMsg;
exports.default = wsSendMsg;
