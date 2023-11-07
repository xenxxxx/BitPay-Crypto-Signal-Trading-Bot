"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.WS_SECURITY_KEY = exports.WS_PORT = exports.WEB_URL = exports.WEB_DEPLOY = exports.CRYPTO_PAIR = exports.TELEGRAM_OWNER_CHAT_ID = exports.TELEGRAM_BOT_TOKEN = exports.API_KEY = exports.TIME_FRAME_IN_MS = exports.TIME_FRAME = exports.CURRENCY_WEBSOCKET_URL = exports.CURRENCY_API_URL = void 0;
const dotenv_1 = __importDefault(require("dotenv"));
dotenv_1.default.config();
//Enviroments
exports.CURRENCY_API_URL = process.env.CURRENCY_API_URL;
exports.CURRENCY_WEBSOCKET_URL = process.env.CURRENCY_WEBSOCKET_URL;
exports.TIME_FRAME = process.env.TIME_FRAME;
exports.TIME_FRAME_IN_MS = Number(process.env.TIME_FRAME_IN_MS);
exports.API_KEY = process.env.API_KEY;
exports.TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
exports.TELEGRAM_OWNER_CHAT_ID = process.env.TELEGRAM_OWNER_CHAT_ID;
exports.CRYPTO_PAIR = process.env.CRYPTO_PAIR;
exports.WEB_DEPLOY = process.env.WEB_DEPLOY;
exports.WEB_URL = process.env.WEB_URL;
exports.WS_PORT = Number(process.env.WS_PORT);
exports.WS_SECURITY_KEY = process.env.WS_SECURITY_KEY;
