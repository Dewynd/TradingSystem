class Grid:
    def __init__(self, strategy, trade, grid):
        self.grid_data = []
        self._strategy = strategy
        self._trade = trade
        self._grid = grid

    async def place(self):
        if self._trade.position_type == "long":
            for g in self._grid:
                print("l")
                size = self._trade.margin * g[1]*(1+g[0]/100) / 100
                print(f"S: {size} {g[1]}")
                await self._strategy.limit_order("sell", "long", size, self._strategy.price_with_percentage_delta(g[0]), trade=self._trade)
                self.grid_data.append([size, self._strategy.price_with_percentage_delta(g[0])])
        else:
            for g in self._grid:
                print("s")
                size = self._trade.margin * g[1] * (1+g[0]/100) / 100
                await self._strategy.limit_order("buy", "short", size, self._strategy.price_with_percentage_delta(-g[0]), trade=self._trade)
                self.grid_data.append([size, self._strategy.price_with_percentage_delta(-g[0])])
