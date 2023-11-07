import axios from 'axios';
import { CURRENCY_API_URL, API_KEY , CURRENCY_WEBSOCKET_URL } from "../env";
import WebSocket from "ws";

//Get Crypto Data From The REST API
async function fetchAPI(API_URL: string) {
  try {
    const response = await axios.get(API_URL);
    return response.data;
  } catch (error: any) {
    throw new Error(error.message);
  }
}


//Sort Data From The REST API
function organizePriceData(data: any[]) {
    const timeOfPricesArr = data.map((obj) => obj?.time);
    const closePricesArr = data.map((obj) => obj?.close);
    const openPricesArr = data.map((obj) => obj?.open);
    const highPricesArr = data.map((obj) => obj?.high);
    const lowPricesArr = data.map((obj) => obj?.low);
    return { timeOfPricesArr, closePricesArr, openPricesArr, highPricesArr, lowPricesArr }
}

//Convert Time Zones From Unix To GMT (UTC / TEHRAN)
function convertToTimezones(unixTimestamp: string) {
    const ts = Number(unixTimestamp);
    const timestampGMT0000 = new Date(ts * 1000).toUTCString();
    const timestampGMT0330 = new Date(ts * 1000 + 19800000).toUTCString();

    return {
        UTC: timestampGMT0000,
        TEHRAN: timestampGMT0330,
    };
}

//Final Function To Return All Of Data We Need From REST API
async function getData(): Promise<GetDataReturn> {
    const API_URL = CURRENCY_API_URL!;
    let fetchDataFromAPI = await fetchAPI(API_URL);

    const priceDataFromApi = fetchDataFromAPI?.Data?.Data;
    const getOrganizedPriceData = organizePriceData(priceDataFromApi);

    const timeFromUnix = fetchDataFromAPI?.Data?.TimeFrom;
    const timeToUnix = fetchDataFromAPI?.Data?.TimeTo;
    const timeFromGMT = convertToTimezones(timeFromUnix);
    const timeToGMT = convertToTimezones(timeToUnix);

    return Object.freeze({
        getTimeFromUnix: () => timeFromUnix,
        getTimeToUnix: () => timeToUnix,
        getTimeFromGMT: () => timeFromGMT,
        getTimeToGMT: () => timeToGMT,
        getTimeOfPricesArr: () => getOrganizedPriceData?.timeOfPricesArr,
        getClosePricesArr: () => getOrganizedPriceData?.closePricesArr,
        getOpenPricesArr: () => getOrganizedPriceData?.openPricesArr,
        getHighPricesArr: () => getOrganizedPriceData?.highPricesArr,
        getLowPricesArr: () => getOrganizedPriceData?.lowPricesArr,
    })
}

function startWs() {
  let apiKey = API_KEY!;
  let wsURL = CURRENCY_WEBSOCKET_URL!;
  const ccStreamer = new WebSocket(wsURL + apiKey);
  const subRequest = {
    action: "SubAdd",
    subs: ["2~Binance~BTC~USDT"],
  };

  function subscribeToPrices() {
    ccStreamer.send(JSON.stringify(subRequest));
  }

  ccStreamer.onopen = function () {
    subscribeToPrices();
  };
  return ccStreamer
}

function getMsgWs(ws : any ,prices: string[], calculateFn: Function) {
  function handleWebSocketMessage(data: any) {
    const objectData = JSON.parse(data.toString("utf8"));
    if (objectData && objectData.PRICE !== undefined) {
      // Remove Last Price And Replace The Price With New Price We Get From Ws
      // Calculate Things U Want
      calculateFn([...prices.slice(0, -1),String(objectData.PRICE)]);
    }
  }

  ws.onmessage = function (event : any) {
    handleWebSocketMessage(event.data);
  };
}

export {getData , startWs ,getMsgWs};

//Interfaces

interface GetDataReturn {
  getTimeFromUnix: () => string
  getTimeToUnix: () => string
  getTimeFromGMT: () => { UTC: string, TEHRAN: string }
  getTimeToGMT: () => { UTC: string, TEHRAN: string }
  getTimeOfPricesArr: () => string[]
  getClosePricesArr: () => string[]
  getOpenPricesArr: () => string[]
  getHighPricesArr: () => string[]
  getLowPricesArr: () => string[]
}