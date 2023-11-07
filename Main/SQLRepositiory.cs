using Microsoft.AspNetCore.SignalR;

using Microsoft.Extensions.Configuration;
using RealTimeSQL.Hubs;
using RealTimeSQL.Models;
using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Threading.Tasks;

namespace RealTimeSQL.Repository
{
    public class SQLRepositiory : ISQLRepositiory
    {
        private readonly IHubContext<SQLHub> _context;
        public SQLRepositiory(IHubContext<SQLHub> context)
        {
            _context = context;
        }
        public List<TBL_Coin> GetAllCoin()
        {
            List<TBL_Coin> LstCoin = new List<TBL_Coin>();
            string SQLCon = "Data Source=Localhost;Initial Catalog=DevDB;User Id=sa;Password=Abc@12345;Connection Lifetime=30;Pooling=True;Min Pool Size=5;Max Pool Size=100;Connection TimeOut=60;";
            using (SqlConnection conn = new SqlConnection(SQLCon))
            {
                if (conn.State != System.Data.ConnectionState.Open)
                {
                    conn.Open();
                }
                SqlDependency.Start(SQLCon);
                string query = "SELECT id, slug, symbol, price_usd, [timestamp] FROM dbo.TBL_Coin";
                SqlCommand cmd = new SqlCommand(query, conn);
                cmd.Notification = null;
                SqlDependency dep = new SqlDependency(cmd);
                dep.OnChange += new OnChangeEventHandler(dbChangeNotification);
                var reader = cmd.ExecuteReader();
                while (reader.Read())
                {
                    TBL_Coin newItem = new TBL_Coin();

                    newItem.id = reader["id"].ToString();
                    newItem.slug = reader["slug"].ToString();
                    newItem.symbol = reader["symbol"].ToString();
                    newItem.timestamp = reader["timestamp"].ToString();
                    newItem.price_usd = Convert.ToDecimal(reader["price_usd"]);
                    LstCoin.Add(newItem);
                }
            }
            return LstCoin;
        }
        private void dbChangeNotification(object sender, SqlNotificationEventArgs e)
        {
            string info = e.Info.ToString();
            //if(info == "Update")
            //{
                _context.Clients.All.SendAsync("RefreshData");
            //}
        }
    }
}
