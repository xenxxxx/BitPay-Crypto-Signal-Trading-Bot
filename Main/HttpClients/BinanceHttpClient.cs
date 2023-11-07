using CryptoSignalChecker.HttpClients.Models;
using Microsoft.AspNetCore.WebUtilities;

namespace CryptoSignalChecker.HttpClients
{
    public class BinanceHttpClient
    {
        private readonly HttpClient _httpClient;
        private const string KlinesEndpoint = "klines";
        private const string ServerTimeEndpoint = "time";

        public BinanceHttpClient(HttpClient httpClient)
        {
            _httpClient = httpClient;
            _httpClient.BaseAddress = new Uri("https://api.binance.com/api/v3/");
        }

        public async Task<IEnumerable<TokenRate>> GetTokenRates(string symbol, string interval, long startTime, long endTime)
        {
            var query = new Dictionary<string, string>()
            {
                ["symbol"] = symbol,
                ["interval"] = interval,
                ["startTime"] = startTime.ToString(),
                ["endTime"] = endTime.ToString(),
                ["limit"] = "1000"
            };

            var uri = QueryHelpers.AddQueryString(KlinesEndpoint, query);
            var jsonResult = await _httpClient.GetFromJsonAsync<List<List<object>>>(uri);
            var tokenRates = new List<TokenRate>();
            foreach (var res in jsonResult)
            {
                var tokenRate = new TokenRate(
                    Convert.ToInt64(res[0].ToString()),
                    Convert.ToDouble(res[1].ToString()),
                    Convert.ToDouble(res[2].ToString()),
                    Convert.ToDouble(res[3].ToString()),
                    Convert.ToDouble(res[4].ToString()),
                    Convert.ToInt64(res[6].ToString()));
                tokenRates.Add(tokenRate);
            }
            return tokenRates;
        }

        public async Task<BinanceServerTime> GetBinanceServerTime()
        {
            return await _httpClient.GetFromJsonAsync<BinanceServerTime>(ServerTimeEndpoint);
        }
    }
}
