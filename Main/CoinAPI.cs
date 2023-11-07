using RealTimeSQL.ViewModels;
using RestSharp;

namespace RealTimeSQL.Service
{
    public class CoinAPI
    {
        public static CoinApiVM GetDataFromAPI()
        {
            CoinApiVM CoinData = new CoinApiVM();
            var client = new RestClient("https://data.messari.io/api/v1/assets?fields=id,slug,symbol,metrics/market_data/price_usd");
            client.Timeout = -1;
            var request = new RestRequest(Method.GET);
            IRestResponse response = client.Execute(request);
            if (response.StatusCode == System.Net.HttpStatusCode.OK)
            {
                CoinData = Newtonsoft.Json.JsonConvert.DeserializeObject<CoinApiVM>(response.Content);
            }
            return CoinData;
        }
    }
}
