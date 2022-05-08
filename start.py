from mexc_sdk import Spot
import config
import asyncio
import time
from queue import Queue

async def main():
    spot = queue_spot(api_key=config.MEXC['API_KEY'], api_secret=config.MEXC['API_KEY_SECRET'])
    spot.ticker_price("MXUSDT")
    spot.ticker_price("MXUSDT")
    spot.ticker_price("MXUSDT")
    print(await spot.dequeue())
    print(await spot.dequeue())
    print(await spot.dequeue())

    """
    mx = stock(spot, "MXUSDT")
    mx_grid = grid(mx, 10, 6, 2)
    print(mx_grid.delta)
    print(mx.price)
    print(mx_grid.get_order_detail())
    """

class async_function():
    def __init__(self, function, args = [], kwargs = {}):
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.last_message = float(time.time())

    async def execute(self):
        time_now = float(time.time())
        if time_now < self.last_message + 3:
            await asyncio.sleep(3)
        self.last_message = time_now
        return str(self.function(self.args)) + " " + str(time_now)

class queue_spot(Spot):
    def __init__(self, api_key, api_secret):
        super().__init__(api_key, api_secret)
        self.queue = Queue()

    async def dequeue(self):
        func = self.queue.get()
        return await func.execute()

    def ticker_price(self, ticker):
        self.queue.put(async_function(super().ticker_price, ticker))

class stock():
    def __init__(self, spot, ticker):
        self.spot = spot
        self.ticker = ticker
        self.price = self.update_price()

    def update_price(self):
        return float(self.spot.ticker_price(self.ticker)["price"])

class limit_order():
    def __init__(self, stock, order_price, quantity):
        self.stock = stock
        self.order_price = order_price
        self.quantity = quantity
        self.type = self.get_order_type()

    def place_order(self):
        # Update order
        response = self.stock.spot.new_order(self.ticker, self.type, "LIMIT", {"timeInForce": "GTC", "quantity": self.quantity, "price": self.order_price})
        return response
        # self.spot.new_order(self.ticker, "BUY", "MARKET", {"timeInForce": "GTC", "quantity": self.quantity, "quoteOrderQty": 6})

    def get_order_type(self):
        if self.order_price > self.stock.price:
            return "SELL"
        else:
            return "BUY"

    def get_order_detail(self):
        return self.type + " " + str(self.order_price) + "$ x " + str(self.quantity) + " units of " + str(self.stock.ticker)

class grid():
    def __init__(self, stock, amount, order_quantity, percentage, initial_price = None):
        self.amount = amount
        self.stock = stock
        self.delta = self.get_delta(percentage)
        self.order_quantity = order_quantity
        self.initial_price = initial_price if initial_price != None else self.stock.price
        self.orders = self.generate_order()

    def generate_order(self):
        orders = []
        upper = int(self.amount / 2) + (1 if self.amount % 2 == 1 else 0)
        lower = int(self.amount / 2)
        # self.stock.update_price()
        for i in range(upper):
            orders.append(limit_order(self.stock, self.initial_price + (self.delta * i), self.order_quantity))
        for i in range(1, lower + 1):
            orders.append(limit_order(self.stock, self.initial_price - (self.delta * i), self.order_quantity))
        return orders

    def get_order_detail(self):
        results = ""
        for order in self.orders:
            results += order.get_order_detail() + "\n"
        return results

    def get_delta(self, percentage):
        return self.stock.price * percentage / 100


asyncio.run(main())
