class MockSession:
    ready_timeout = 1
    pick_timeout = 1
    round_timeout = 1

    def __init__(self):
        self.removed = []

    async def disconnect(self, player):
        self.removed.append(player)
