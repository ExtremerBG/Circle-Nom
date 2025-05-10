class FakePlayer:
    def __init__(self, size: int|float = 60, speed: int|float = 30):
        """Fake player used for testing purposes."""
        self.size = size
        self.speed = speed