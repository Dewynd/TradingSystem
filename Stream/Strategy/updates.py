class Update:
    def __init__(self, event, timestamp, data):
        self._event = event
        self._timestamp = timestamp
        self._data = data

    def is_update_worked(self, timestamp):
        if timestamp >= self._timestamp:
            return True
        else:
            return False

    async def update(self):
        await self._event(self._data)