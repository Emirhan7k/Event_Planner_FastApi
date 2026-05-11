def cosine_like_score(user_vector: list[float], event_vector: list[float]) -> float:
    pairs = zip(user_vector, event_vector, strict=False)
    return sum(a * b for a, b in pairs)
