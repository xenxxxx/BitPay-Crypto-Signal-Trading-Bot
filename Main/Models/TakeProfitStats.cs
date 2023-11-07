namespace CryptoSignalChecker.Models
{
    public class TakeProfitStats
    {
        public double Value { get; set; }
        public DateTime DateTime { get; set; }
        public TakeProfitStats(double value)
        {
            Value = value;
        }
    }
}
