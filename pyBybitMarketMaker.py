from BybitWebsocket import BybitWebsocket
import time
import json
import bybit
import asyncio

# fill in your api keys
spread = 10
apikey = 'key'
apisecret = 'secret'

ws = BybitWebsocket(wsURL="wss://stream.bybit.com/realtime",
                         api_key=apikey, api_secret=apisecret)
client  = bybit.bybit(test=False, api_key=apikey, api_secret=apisecret)

async def connectapi():
    # subscribe to topics
    ws.subscribe_order()
    # ws.subscribe_execution()
    # ws.subscribe_position()

    # get responses forever
    while(1):
        # print(ws.get_data('order'))
        orderData = ws.get_data('order')
        lenData = len(orderData)
        for x in range (0,lenData):
            ele = orderData[x]
            print(ele)
            order_id = ele['order_id']
            symbol = ele['symbol'] 
            side = ele['side'] 
            order_type = ele['order_type'] 
            price = float(ele['price'])
            qty = ele['qty']
            time_in_force = ele['time_in_force']
            order_status = ele['order_status']
            if order_status == 'Filled':
                if side == 'Buy':
                    # set sell order
                    print("Buy filled. Setting sell")
                    print(client.Order.Order_newV2(side="Sell",symbol=symbol,order_type=order_type,qty=qty,price=price+spread,time_in_force="GoodTillCancel").result())
                else:
                    # set buy order
                    print("Sell filled. Setting buy")
                    print(client.Order.Order_newV2(side="Buy",symbol=symbol,order_type=order_type,qty=qty,price=price-spread,time_in_force="GoodTillCancel").result())

        # logger.info(ws.get_data("execution"))
        # logger.info(ws.get_data("position"))
        time.sleep(1)  # wait one second before checking for new responses

loop = asyncio.get_event_loop()
loop.run_until_complete(connectapi())
loop.run_forever()
