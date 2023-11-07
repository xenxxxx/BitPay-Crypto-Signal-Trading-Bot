using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using RealTimeSQL.Models;
using RealTimeSQL.Repository;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;

namespace RealTimeSQL.Controllers
{
    public class HomeController : Controller
    {

        private readonly ISQLRepositiory _SQLRepositiory;
        public HomeController(ISQLRepositiory SQLRepositiory)
        {
            _SQLRepositiory = SQLRepositiory;
        }

        public IActionResult Index()
        {
            return View();
        }

        [HttpGet]
        public IActionResult GetCoins()
        {
            List<TBL_Coin> coin = new List<TBL_Coin>();
            coin = _SQLRepositiory.GetAllCoin();
            DateTime LstUpdate = Convert.ToDateTime(coin.FirstOrDefault().timestamp.ToString());
            ViewBag.Time = LstUpdate.ToString("dd-MM-yyyy HH:mm:ss");
            return PartialView(coin);
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
