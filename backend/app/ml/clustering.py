def cluster_interests(interests: list[str]) -> dict[str, list[str]]:
    return {"primary": interests[:3], "secondary": interests[3:]}
