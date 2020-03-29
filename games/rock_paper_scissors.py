class RockPaperScissors:

    def __init__(self, connections):
        self.connections = connections

    def __str__(self):
        return f"Session with {[str(c) for c in self.connections]}"

    async def play(self):
        async for conn in self.connections_gen:
            await conn.send("game", "ready")
            await conn.close()
