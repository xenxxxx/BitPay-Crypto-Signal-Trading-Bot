import { TIME_FRAME_IN_MS, WEB_DEPLOY, WEB_URL } from "./env";
import { getData, getMsgWs, startWs } from "./data-related/api";
import crossEMA from "./data-related/calculate";
import BotSendMsg from "./bot-related/telegram";
import express, { Request, Response } from 'express';
import axios from "axios";

import wsFn from "./data-related/websocket";

//Function To Send Msg (Limit Messages Bot Can Send 1 In 5 Mins)
let lastMessageTime = 0;
function botFn(message: string) {
  const currentTime = Date.now();
  const interrupt = 300000; // 5 minutes in milliseconds

  if (currentTime - lastMessageTime >= interrupt) {
    lastMessageTime = currentTime;
    BotSendMsg(message);
  }
}

//Calculate Function
function calculateFn(prices: string[]) {
  return crossEMA(prices, botFn, wsFn);
}

//Function To Keep Alive The App In Free Backend Services
function keepAlive(appUrl: string) {
  axios.get(appUrl).then(res => console.log(`Keep Alive Function Successfuly Executed. Status Code :${res.status}, Status Text : ${res.statusText}.`)).catch((err: any) => console.log(err))
}

//Function Of Start Application
async function ApplicationStart() {
  try {
    const updateMinutes = Number(TIME_FRAME_IN_MS);
    let data = await getData();
    let closePricesArrFromAPI = data.getClosePricesArr();
    const ws = startWs()
    getMsgWs(ws, closePricesArrFromAPI, calculateFn);
    console.log("Bot Running Successfuly.");

    setInterval(async () => {
      data = await getData();
      closePricesArrFromAPI = data.getClosePricesArr();
      getMsgWs(ws, closePricesArrFromAPI, calculateFn);
    }, updateMinutes!);


  } catch (error) {
    console.error("An error occurred:", error);
  }
}

// This Is For Free Hostings Deploy Set "WEB_DEPLOY" Enviuroment False
if (WEB_DEPLOY === "true") {
  const PORT = <string>process.env.PORT || "5000";
  const app = express()
  app.get("/", function (req: Request, res: Response) {
    res.status(200).send("Bot Is Working.")
  });
  app.listen(PORT, function () {
    ApplicationStart();
    console.log(`🚀 WebServer Running On Port :${PORT}`);
  });
  setInterval(() => {
    keepAlive(WEB_URL)
  }, 30 * 1000)
} else {
  ApplicationStart();
}