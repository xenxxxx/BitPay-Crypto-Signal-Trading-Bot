
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using RealTimeSQL.Data;
using RealTimeSQL.Models;
using RealTimeSQL.ViewModels;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace RealTimeSQL.BackgroudServices
{
    public class CoinBackgroundService : BackgroundService
    {
        private readonly IServiceScopeFactory _scopeFactory;
        private Timer _timer;
        public CoinBackgroundService(IServiceScopeFactory scopeFactory)
        {
            _scopeFactory = scopeFactory;
        }
        protected override Task ExecuteAsync(CancellationToken stoppingToken)
        {
            _timer = new Timer(DoWork, null, TimeSpan.Zero, TimeSpan.FromSeconds(1));
            return Task.CompletedTask;

        }

        private void DoWork(object state)
        {
            CoinApiVM DataFromAPI = Service.CoinAPI.GetDataFromAPI();
            using (var scope = _scopeFactory.CreateScope())
            {
                var _context = scope.ServiceProvider.GetRequiredService<AppDBContext>();
                _context.TBL_Coin.RemoveRange(_context.TBL_Coin.ToList());
                if (DataFromAPI.data != null && DataFromAPI.data.Count > 0)
                {
                    foreach (var i in DataFromAPI.data)
                    {
                        _context.Add(new TBL_Coin
                        {
                            id = i.id,
                            slug = i.slug,
                            symbol = i.symbol,
                            price_usd = i.metrics.market_data.price_usd,
                            timestamp = DataFromAPI.status.timestamp
                        });
                        Console.WriteLine($"{i.symbol}: {i.metrics.market_data.price_usd}");
                    }
                    _context.SaveChanges();
                }
                else
                {
                    Console.WriteLine($"No data from api.");
                }
            }
        }

        public override void Dispose()
        {
            base.Dispose();
            _timer.Dispose();

        }
    }
}
