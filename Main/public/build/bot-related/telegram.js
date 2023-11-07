"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const node_telegram_bot_api_1 = __importDefault(require("node-telegram-bot-api"));
const env_1 = require("../env");
const botToken = env_1.TELEGRAM_BOT_TOKEN;
const ownerChatId = env_1.TELEGRAM_OWNER_CHAT_ID;
const TBot = new node_telegram_bot_api_1.default(botToken, { polling: true });
TBot.onText(/\/start/, (msg) => {
    // const chatId = msg.chat.id;
    const chatId = ownerChatId;
    // Check if the bot is already started
    if (!isBotStarted(chatId)) {
        // Perform start action
        startBot(chatId);
        TBot.sendMessage(chatId, 'Bot started!');
    }
    else {
        TBot.sendMessage(chatId, 'Bot already started!');
    }
});
TBot.onText(/\/stop/, (msg) => {
    // const chatId = msg.chat.id;
    const chatId = ownerChatId;
    // Check if the bot is already stopped
    if (isBotStarted(chatId)) {
        // Perform stop action
        stopBot(chatId);
        TBot.sendMessage(chatId, 'Bot stopped!');
    }
    else {
        TBot.sendMessage(chatId, 'Bot already stopped!');
    }
});
const botState = {};
function startBot(chatId) {
    botState[chatId] = true;
}
function stopBot(chatId) {
    botState[chatId] = false;
}
function isBotStarted(chatId) {
    return botState[chatId] || false;
}
function BotSendMsg(message) {
    if (isBotStarted(ownerChatId)) {
        TBot.sendMessage(ownerChatId, message);
    }
}
exports.default = BotSendMsg;
