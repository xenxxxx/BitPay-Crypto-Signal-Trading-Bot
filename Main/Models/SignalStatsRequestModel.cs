using CryptoSignalChecker.Enums;

namespace CryptoSignalChecker.Models
{
    public class SignalStatsRequestModel
    {
        public string TokenPair { get; set; }
        public FuturesType FuturesType { get; set; }
        public int Leverage { get; set; }
        public double Entry { get; set; }
        public double StopLoss { get; set; }
        public List<TakeProfitStats> TakeProfits { get; set; }
        public DateTime SignalDateTime { get; set; }
        public DateTime SignalEndDateTime { get; set; }
    }
}
