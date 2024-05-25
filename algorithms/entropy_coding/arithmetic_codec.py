class ArithmeticCodec:
    def __init__(self, num_symbols=256):
        self.num_symbols = num_symbols
        self.low = 0
        self.high = 0xFFFFFFFF
        self.scale = 0x10000

    def encode(self, data):
        stream = []
        for symbol in data:
            range = self.high - self.low + 1
            self.high = self.low + (range * self.cumulative_frequency[symbol + 1] // self.total_symbols) - 1
            self.low = self.low + (range * self.cumulative_frequency[symbol] // self.total_symbols)
            while True:
                if self.high < self.scale:
                    stream.append(0)
                    self.low *= 2
                    self.high = self.high * 2 + 1
                elif self.low >= self.scale:
                    stream.append(1)
                    self.low = (self.low - self.scale) * 2
                    self.high = (self.high - self.scale) * 2 + 1
                else:
                    break
        return bytes(stream)

    def decode(self, encoded_data, length):
        data = []
        value = 0
        for byte in encoded_data:
            value = (value * 2) + byte
        for _ in range(length):
            range = self.high - self.low + 1
            cum = ((value - self.low + 1) * self.total_symbols - 1) // range
            symbol = 0  # Find the symbol
            data.append(symbol)
            self.high = self.low + (range * self.cumulative_frequency[symbol + 1] // self.total_symbols) - 1
            self.low = self.low + (range * self.cumulative_frequency[symbol] // self.total_symbols)
        return data