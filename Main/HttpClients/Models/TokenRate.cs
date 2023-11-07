namespace CryptoSignalChecker.HttpClients.Models
{
    public class TokenRate
    {
        public long KlineOpenTime { get; set; }
        public double OpenPrice { get; set; }
        public double HighPrice { get; set; }
        public double LowPrice { get; set; }
        public double ClosePrice { get; set; }
        public long KlineCloseTime { get; set; }

        public TokenRate(
            long klineOpenTime,
            double openPrice,
            double highPrice,
            double lowPrice,
            double closePrice,
            long klineCloseTime)
        {
            KlineOpenTime = klineOpenTime;
            OpenPrice = openPrice;
            HighPrice = highPrice;
            LowPrice = lowPrice;
            ClosePrice = closePrice;
            KlineCloseTime = klineCloseTime;
        }
    }
}
