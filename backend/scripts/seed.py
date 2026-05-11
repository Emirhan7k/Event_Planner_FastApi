from app.repositories.event_repo import event_repository


if __name__ == "__main__":
    print(f"Seed ready: {len(event_repository.list())} sample events")
