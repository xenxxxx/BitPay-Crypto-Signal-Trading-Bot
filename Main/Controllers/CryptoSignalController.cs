using CryptoSignalChecker.Interfaces;
using CryptoSignalChecker.Models;
using Microsoft.AspNetCore.Mvc;

namespace CryptoSignalChecker.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CryptoSignalController : ControllerBase
    {
        private readonly ICryptoSignalService _cryptoSignalService;

        public CryptoSignalController(ICryptoSignalService cryptoSignalService)
        {
            _cryptoSignalService = cryptoSignalService;
        }

        [HttpPost]
        public async Task<IActionResult> GetTokenRate(SignalStatsRequestModel request)
        {
            var result = await _cryptoSignalService.GetRate(request);
            return Ok(result);
        }
    }
}
