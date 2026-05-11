from app.websocket.manager import manager


async def notify_recommendation(message: str) -> None:
    await manager.broadcast(message)
