from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        nullable=True
    )

    completed: Mapped[bool] = mapped_column(
        nullable=False,
        default=False
    )

    priority: Mapped[int] = mapped_column(
        nullable=False,
        default=1
    )