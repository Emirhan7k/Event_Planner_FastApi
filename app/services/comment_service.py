from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment
from app.models.user import User
from app.repositories.base import BaseRepository

class CommentRepository(BaseRepository[Comment]):
    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)

class CommentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = CommentRepository(session)

    async def add_comment(self, user: User, event_id: int, content: str, rating: int) -> Comment:
        comment = Comment(
            user_id=user.id,
            event_id=event_id,
            content=content,
            rating=rating
        )
        return await self.repo.create(comment)

    async def get_event_comments(self, event_id: int) -> list[Comment]:
        result = await self.session.execute(
            select(Comment)
            .where(Comment.event_id == event_id)
            .options(selectinload(Comment.user))
            .order_by(Comment.created_at.desc())
        )
        return list(result.scalars().all())

    async def delete_comment(self, comment_id: int, user_id: int) -> bool:
        comment = await self.repo.get(comment_id)
        if comment and (comment.user_id == user_id):
            await self.repo.delete(comment_id)
            return True
        return False
