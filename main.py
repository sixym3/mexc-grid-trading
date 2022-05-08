from mexc_sdk import Spot
import config
import asyncio
import time

RATE_LIMIT = 3 # Wait at least 3 seconds before sending transaction

async def main():
    spot = Spot(api_key=config.MEXC['API_KEY'], api_secret=config.MEXC['API_KEY_SECRET'])
    test = Grid("MX_USDT", 11, 2, 10, spot)
    test.generate_order()
    await test.place_all_order()
    while True:
        test.update()

class Order():

    placed = False
    symbol = ""

    def __init__(self, price, quantity, symbol, spot):
        self.price = price
        self.quantity = quantity
        self.allocation = price * quantity
        self.symbol = symbol
        self.spot = spot

    def get_market_price(self):
        return 2

    async def place_order(self):
        await asyncio.sleep(3)
        if (self.price < self.get_market_price()):
            self.buy_order()
        else:
            self.sell_order()

    def buy_order(self):
        print("buy order at " + str(self.symbol) + ": " + str(self.quantity) + " @ " + str(self.price) + " $")
        placed = True

    def sell_order(self):
        print("sell order at " + str(self.symbol) + ": " + str(self.quantity) + " @ " + str(self.price) + " $")
        placed = True

    def is_filled(self):
        print("checked if filled")
        if self.placed:
             self.place_order(self)
             self.placed = False


class Grid():

    def __init__(self, symbol, grid_count, percentage, quantity, spot):
        self.symbol = symbol
        self.open_orders = []
        self.grid_count = grid_count
        self.difference = self.get_market_price() * percentage / 100
        self.quantity = quantity
        self.spot = spot

    def generate_order(self):
        buy_order = int(self.grid_count / 2)
        sell_order = int(self.grid_count / 2)
        if self.grid_count % 2 == 1:
            buy_order = buy_order + 1

        for i in range(buy_order):
            self.open_orders.append(Order(self.get_market_price()*(1+(i*self.difference)),
                                                                        self.quantity,
                                                                        self.symbol,
                                                                        self.spot))
        for i in range(1, sell_order + 1):
            self.open_orders.append(Order(self.get_market_price()*(1-(i*self.difference)),
                                                                        self.quantity,
                                                                        self.symbol,
                                                                        self.spot))

    async def place_all_order(self):
        for order in self.open_orders:
            await order.place_order()

    def get_market_price(self):
        return 2

asyncio.run(main())
