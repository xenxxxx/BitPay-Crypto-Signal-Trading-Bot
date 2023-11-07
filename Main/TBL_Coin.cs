using System.ComponentModel.DataAnnotations;

namespace RealTimeSQL.Models
{
    public class TBL_Coin
    {
        public string id { get; set; }
        public string slug { get; set; }
        public string symbol { get; set; }
        [Display(Name = "Price [USD]")]
        public decimal? price_usd { get; set; }
        public string timestamp { get; set; }
    }
}
