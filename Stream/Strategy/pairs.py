class Pair:
    def __init__(self, symbol1, symbol2):
        self._symbol1 = symbol1
        self._symbol2 = symbol2

    @property
    def symbol(self):
        return self._symbol1

    @property
    def symbol2(self):
        return self._symbol2
            