"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getMsgWs = exports.startWs = exports.getData = void 0;
const axios_1 = __importDefault(require("axios"));
const env_1 = require("../env");
const ws_1 = __importDefault(require("ws"));
//Get Crypto Data From The REST API
function fetchAPI(API_URL) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const response = yield axios_1.default.get(API_URL);
            return response.data;
        }
        catch (error) {
            throw new Error(error.message);
        }
    });
}
//Sort Data From The REST API
function organizePriceData(data) {
    const timeOfPricesArr = data.map((obj) => obj === null || obj === void 0 ? void 0 : obj.time);
    const closePricesArr = data.map((obj) => obj === null || obj === void 0 ? void 0 : obj.close);
    const openPricesArr = data.map((obj) => obj === null || obj === void 0 ? void 0 : obj.open);
    const highPricesArr = data.map((obj) => obj === null || obj === void 0 ? void 0 : obj.high);
    const lowPricesArr = data.map((obj) => obj === null || obj === void 0 ? void 0 : obj.low);
    return { timeOfPricesArr, closePricesArr, openPricesArr, highPricesArr, lowPricesArr };
}
//Convert Time Zones From Unix To GMT (UTC / TEHRAN)
function convertToTimezones(unixTimestamp) {
    const ts = Number(unixTimestamp);
    const timestampGMT0000 = new Date(ts * 1000).toUTCString();
    const timestampGMT0330 = new Date(ts * 1000 + 19800000).toUTCString();
    return {
        UTC: timestampGMT0000,
        TEHRAN: timestampGMT0330,
    };
}
//Final Function To Return All Of Data We Need From REST API
function getData() {
    var _a, _b, _c;
    return __awaiter(this, void 0, void 0, function* () {
        const API_URL = env_1.CURRENCY_API_URL;
        let fetchDataFromAPI = yield fetchAPI(API_URL);
        const priceDataFromApi = (_a = fetchDataFromAPI === null || fetchDataFromAPI === void 0 ? void 0 : fetchDataFromAPI.Data) === null || _a === void 0 ? void 0 : _a.Data;
        const getOrganizedPriceData = organizePriceData(priceDataFromApi);
        const timeFromUnix = (_b = fetchDataFromAPI === null || fetchDataFromAPI === void 0 ? void 0 : fetchDataFromAPI.Data) === null || _b === void 0 ? void 0 : _b.TimeFrom;
        const timeToUnix = (_c = fetchDataFromAPI === null || fetchDataFromAPI === void 0 ? void 0 : fetchDataFromAPI.Data) === null || _c === void 0 ? void 0 : _c.TimeTo;
        const timeFromGMT = convertToTimezones(timeFromUnix);
        const timeToGMT = convertToTimezones(timeToUnix);
        return Object.freeze({
            getTimeFromUnix: () => timeFromUnix,
            getTimeToUnix: () => timeToUnix,
            getTimeFromGMT: () => timeFromGMT,
            getTimeToGMT: () => timeToGMT,
            getTimeOfPricesArr: () => getOrganizedPriceData === null || getOrganizedPriceData === void 0 ? void 0 : getOrganizedPriceData.timeOfPricesArr,
            getClosePricesArr: () => getOrganizedPriceData === null || getOrganizedPriceData === void 0 ? void 0 : getOrganizedPriceData.closePricesArr,
            getOpenPricesArr: () => getOrganizedPriceData === null || getOrganizedPriceData === void 0 ? void 0 : getOrganizedPriceData.openPricesArr,
            getHighPricesArr: () => getOrganizedPriceData === null || getOrganizedPriceData === void 0 ? void 0 : getOrganizedPriceData.highPricesArr,
            getLowPricesArr: () => getOrganizedPriceData === null || getOrganizedPriceData === void 0 ? void 0 : getOrganizedPriceData.lowPricesArr,
        });
    });
}
exports.getData = getData;
function startWs() {
    let apiKey = env_1.API_KEY;
    let wsURL = env_1.CURRENCY_WEBSOCKET_URL;
    const ccStreamer = new ws_1.default(wsURL + apiKey);
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
    return ccStreamer;
}
exports.startWs = startWs;
function getMsgWs(ws, prices, calculateFn) {
    function handleWebSocketMessage(data) {
        const objectData = JSON.parse(data.toString("utf8"));
        if (objectData && objectData.PRICE !== undefined) {
            // Remove Last Price And Replace The Price With New Price We Get From Ws
            // Calculate Things U Want
            calculateFn([...prices.slice(0, -1), String(objectData.PRICE)]);
        }
    }
    ws.onmessage = function (event) {
        handleWebSocketMessage(event.data);
    };
}
exports.getMsgWs = getMsgWs;
