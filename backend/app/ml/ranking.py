def rank(scores: dict[int, float]) -> list[int]:
    return [event_id for event_id, _ in sorted(scores.items(), key=lambda item: item[1], reverse=True)]
