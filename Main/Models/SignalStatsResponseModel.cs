using CryptoSignalChecker.Enums;

namespace CryptoSignalChecker.Models
{
    public class SignalStatsResponseModel
    {
        public DateTime StopLoss { get; set; }
        public DateTime AprxmtLiquidation { get; set; }
        public List<TakeProfitStats> TakeProfitStats { get; set; } = new List<TakeProfitStats>();
    }
}
