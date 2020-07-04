import aiohttp
import asyncio
import math
from aiohttp import web
import json
import time

import redis

async def main(request):
    start = time.time()
    try:
        response_obj =  await asyncio.wait_for(exchange_rate(request), timeout=0.1)
        print('Time taken for DATA is ', time.time() - start)
        return web.Response(text = json.dumps(response_obj), status = 200)
    except asyncio.TimeoutError:
        response_obj = {'rate': 'TIME_OUT'}
        text = json.dumps(response_obj)
        print('Time taken for TIME_OUT is ', time.time() - start)
        return web.Response(text = text, status = 408)

async def exchange_rate(request):

    r= redis.Redis()
    
    exchange = request.rel_url.query['exchange']
    srcCurrency = request.rel_url.query['fromCurrency']
    destCurrency = request.rel_url.query['toCurrency']

    if (r.exists(exchange.lower()) == 0):
        response_obj = {'rate': 'Invalid exchange'}
        text = json.dumps(response_obj)
        return response_obj

    data = json.loads(r.get(exchange.lower()).decode('utf-8'))

    
    srcBtc = 0
    destBtc = 0

    for di in data:        
        if (di['symbol'].lower() == srcCurrency.lower()):
            srcBtc = di['priceBtc']

        if (di['symbol'].lower() == destCurrency.lower()):
            destBtc = di['priceBtc']
        
    if (srcBtc == 0 or destBtc == 0):
        message = ''
        if(srcBtc == 0 and destBtc == 0):
             message = 'Both Source and Destination Currency Not Available'
        elif(srcBtc == 0):
            message = 'Source Currency Not Available'
        elif(destBtc == 0):
            message = 'Destination Currency Not Available'

        response_obj = {'rate': message}
        return response_obj
     

    rate = math.floor(float(srcBtc)/float(destBtc))
    response_obj = {'rate': rate}
    return response_obj



    
app = web.Application()
routes = [web.get('/exchange-rate',main)]
app.add_routes(routes)
web.run_app(app)


