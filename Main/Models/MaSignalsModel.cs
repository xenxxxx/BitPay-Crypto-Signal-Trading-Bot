using System;
using System.Collections.Generic;
using System.Text;

namespace CryptoSignalsMailing.Models
{
    public class MaSignalsModel
    {
        public string Name { get; set; }

        public double MovingAverage { get; set; }

        public int ChartInHours { get; set; }

        public double PriceCurrent { get; set; }

        public double PriceYesterday { get; set; }

        public double PercentageCurrentPriceToMa { get; set; }

        public bool IsShortable { get; set; }
    }
}
