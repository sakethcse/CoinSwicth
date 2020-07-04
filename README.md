# CoinSwicth
1. Required python modules-- aiohttp, redis
2.Installation instrcutions can be found here,
https://docs.aiohttp.org/en/stable/ and
https://pypi.org/project/redis/
3. open terminal and execute following in order, 
python3 get_data.py
python3 exchange_server_cache.py 
4. keep the terminal open for server to run and execute following link in any browser,
localhost:8080/exchange-rate?exchange=kucoin&fromCurrency=BTC&toCurrency=ETH
5. The time taken by API to return results is printed on console 

Desgin:
1) API retruns with TIME_OUT if it takes more than 100ms(now it takes approximately < 5ms)
2) API returns invalid exchange, invalid src currency or invalid destination currency error accordingly.
3) used redis cache to store key , value pairs where key is exchange name and value is list of its exchange rates
4) redis keys expire after 1 minute and need to be refilled by a cronjob which loads data every minute in redis cache
