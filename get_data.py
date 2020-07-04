import aiohttp
import asyncio
import math
from aiohttp import web
import json
import time

import redis




async def get_list_of_exchanges():
    async with aiohttp.ClientSession() as session:
            async with session.get('https://dev-api.shrimpy.io/v1/list_exchanges') as response:
                data = await response.json()
                exchange_list = []
                for di in data:
                    exchange_list.append(di['exchange'])

                return exchange_list

async def fetch(session, exchange,r):
    async with session.get('https://dev-api.shrimpy.io/v1/exchanges/' + exchange  + '/ticker') as response:
        if(response.status != 200): 
                    response_obj = {'rate': 'Invalid exchange'}
                    text = json.dumps(response_obj)
                    return response_obj

        data = await response.json()
        data_json = json.dumps(data)
        r.mset({exchange.lower() : data_json})
        r.expire(exchange, 60)
        return response




async def get_data():
    try:
        r = redis.Redis()

        if (r.exists('exchange_list') == 0):
            exchange_list_temp = await asyncio.wait_for(get_list_of_exchanges())
            exchange_list_json = json.dumps(exchange_list_temp)
            r.mset({'exchange_list' : exchange_list_json})
            r.expire('exchange_list', 24*60*60) #set expiry time to 1 day
    
        
        exchange_list = json.loads(r.get('exchange_list').decode('utf-8'))

        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout = timeout) as session:
            await asyncio.gather(*[asyncio.ensure_future(fetch(session, exchange,r)) for exchange in exchange_list])
            print("data loaded succesfully")
    except asyncio.exceptions.TimeoutError:
        response_obj = {'rate': 'TIME_OUT'}
        return response_obj


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_data())



