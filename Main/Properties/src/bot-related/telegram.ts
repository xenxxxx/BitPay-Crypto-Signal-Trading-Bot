import TelegramBot from "node-telegram-bot-api";
import { TELEGRAM_BOT_TOKEN, TELEGRAM_OWNER_CHAT_ID } from "../env";

const botToken = TELEGRAM_BOT_TOKEN!;
const ownerChatId = TELEGRAM_OWNER_CHAT_ID!;
const TBot = new TelegramBot(botToken, { polling: true });

TBot.onText(/\/start/, (msg) => {
    // const chatId = msg.chat.id;
    const chatId = ownerChatId;
    // Check if the bot is already started
    if (!isBotStarted(chatId)) {
      // Perform start action
      startBot(chatId);
      TBot.sendMessage(chatId, 'Bot started!');
    } else {
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
    } else {
        TBot.sendMessage(chatId, 'Bot already stopped!');
    }
  });

  const botState : any = {};

  function startBot(chatId : any) {
    botState[chatId] = true;
  }
  
  function stopBot(chatId : any) {
    botState[chatId] = false;
  }
  
  function isBotStarted(chatId : any) {
    return botState[chatId] || false;
  }

function BotSendMsg(message: string) {
    if (isBotStarted(ownerChatId)) {
        TBot.sendMessage(ownerChatId, message);
    }
}

export default BotSendMsg;