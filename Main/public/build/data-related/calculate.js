"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.crossEMA = exports.calculateMACD = exports.calculateEMA = void 0;
const env_1 = require("../env");
function calculateEMA(prices, period, smoothing) {
    //*Good Smoothing For MACD : 2
    //*Good Smoothing For EMA 200 : 1.5
    //*Good Smoothing For EMA 25 : 1.2
    //*Good Smoothing For EMA 12 : 1.275
    //Typescript - make string array number array for ts warnings
    const numberPrices = prices.map(item => Number(item));
    //Add smoothing factor
    const multiplier = (smoothing || 2) / (period + 1);
    const ema = [];
    let emaPrev = numberPrices[0];
    ema.push(emaPrev);
    for (let i = 1; i < numberPrices.length; i++) {
        const emaValue = (numberPrices[i] - emaPrev) * multiplier + emaPrev;
        ema.push(emaValue);
        emaPrev = emaValue;
    }
    //round ema to two decimal places
    const roundedEma = ema.map(item => Number(item.toFixed(2)));
    return roundedEma;
}
exports.calculateEMA = calculateEMA;
function calculateMACD(prices, longEMA, shortEMA, signalEMA) {
    //Good Combo : longEMA : 100 , shortEMA : 26 , signalEMA : 9
    // Calculate Short EMA
    const ema12 = calculateEMA(prices, shortEMA || 26);
    // Calculate Long EMA
    const ema26 = calculateEMA(prices, longEMA || 100);
    // Calculate the MACD line
    const macdLine = ema12.map((ema12Value, index) => ema12Value - ema26[index]);
    // Calculate the Signal EMA Of MACD Line
    const signalLine = calculateEMA(macdLine, signalEMA || 9);
    // Calculate the MACD histogram
    const histogram = macdLine.map((macdValue, index) => macdValue - signalLine[index]);
    //round histogram to two decimal places
    const roundedHistogram = histogram.map(item => Number(item.toFixed(2)));
    return roundedHistogram;
}
exports.calculateMACD = calculateMACD;
function crossEMA(prices, botFn, wsFn, longEMA, shortEMA) {
    //Declare Signals And Get Last Price
    const signals = ["Buy", "Sell", "Nothing"];
    const priceLastOne = Number(prices[prices.length - 1]);
    //Calculate EMAs
    const slowEMA = calculateEMA(prices, longEMA || 25, 2);
    const fastEMA = calculateEMA(prices, shortEMA || 12, 2);
    //Get Previous Ones And Last EMAs
    const slowEMALastMinus = slowEMA[slowEMA.length - 5];
    const fastEMALastMinus = fastEMA[fastEMA.length - 5];
    const slowEMALastOne = slowEMA[slowEMA.length - 1];
    const fastEMALastOne = fastEMA[fastEMA.length - 1];
    //Check EMA 200 + MACD HISTOGRAM
    const ema200 = calculateEMA(prices, 200, 2);
    const ema200LastOne = ema200[ema200.length - 1];
    const macdHistogram = calculateMACD(prices);
    const macdLastOne = macdHistogram[macdHistogram.length - 1];
    //Give Signal
    if (fastEMALastOne > slowEMALastOne && fastEMALastMinus < slowEMALastMinus && ema200LastOne < priceLastOne && macdLastOne > 0) {
        //Buy Signal
        const wsData = {
            signal: signals[0],
            priceLastOne,
            fastEMALastOne,
            slowEMALastOne,
            fastEMALastMinus,
            slowEMALastMinus,
            ema200LastOne,
            macdLastOne
        };
        const returnData = `🚀 ${signals[0]} Signal At ${priceLastOne} In ${env_1.CRYPTO_PAIR} Pair. ⚙️ More Details : Time Frame : ${env_1.TIME_FRAME} , Last Fast Ema : ${fastEMALastOne} , Last Slow Ema : ${slowEMALastOne}, Last 200 EMA : ${ema200LastOne}, Last MACD Histogram : ${macdLastOne}`;
        botFn(returnData);
        wsFn(JSON.stringify(wsData));
    }
    else if (fastEMALastOne < slowEMALastOne && fastEMALastMinus > slowEMALastMinus && ema200LastOne > priceLastOne && macdLastOne < 0) {
        //Sell Signal
        const wsData = {
            signal: signals[1],
            priceLastOne,
            fastEMALastOne,
            slowEMALastOne,
            fastEMALastMinus,
            slowEMALastMinus,
            ema200LastOne,
            macdLastOne
        };
        const returnData = `🚀 ${signals[1]} Signal At ${priceLastOne} In ${env_1.CRYPTO_PAIR} Pair. ⚙️ More Details : Time Frame : ${env_1.TIME_FRAME} , Last Fast Ema : ${fastEMALastOne} , Last Slow Ema : ${slowEMALastOne}, Last 200 EMA : ${ema200LastOne}, Last MACD Histogram : ${macdLastOne}`;
        botFn(returnData);
        wsFn(JSON.stringify(wsData));
    }
    else {
        //Nothing Signal
        // return null;
        const wsData = {
            signal: signals[2],
            priceLastOne,
            fastEMALastOne,
            slowEMALastOne,
            fastEMALastMinus,
            slowEMALastMinus,
            ema200LastOne,
            macdLastOne
        };
        wsFn(JSON.stringify(wsData));
    }
}
exports.crossEMA = crossEMA;
exports.default = crossEMA;
