
using RealTimeSQL.Models;
using System.Collections.Generic;

namespace RealTimeSQL.Repository
{
    public interface ISQLRepositiory
    {
        List<TBL_Coin> GetAllCoin();
    }
}
