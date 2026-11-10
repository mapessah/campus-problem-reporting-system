from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.models.enums import UserRole


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    full_name: Mapped[str] = mapped_column(String(150), nullable=False)

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True)

    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role", native_enum=False),
        nullable=False,
        default=UserRole.REPORTER,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Reports submitted by this user
    submitted_reports = relationship(
        "Report", back_populates="reporter", foreign_keys="Report.reporter_id"
    )

    # Reports currently assigned to this user
    assigned_reports = relationship(
        "Report", back_populates="assignee", foreign_keys="Report.assigned_to"
    )

    # Assignments received
    assignments_received = relationship(
        "Assignment", back_populates="technician", foreign_keys="Assignment.assigned_to"
    )

    # Assignments created by this user
    assignments_created = relationship(
        "Assignment", back_populates="assigner", foreign_keys="Assignment.assigned_by"
    )

    comments = relationship("Comment", back_populates="user")

    notifications = relationship("Notification", back_populates="user")
