def vectorize(text: str) -> list[float]:
    return [ord(char) / 255 for char in text[:32]]
