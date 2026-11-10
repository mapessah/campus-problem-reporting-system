from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Assignment(Base):
    __tablename__ = "assignments"

    assignment_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.report_id"), nullable=False
    )

    assigned_to: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False
    )

    assigned_by: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False
    )

    remarks: Mapped[str | None] = mapped_column(String(500), nullable=True)

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    unassigned_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    report = relationship("Report", back_populates="assignments")

    technician = relationship(
        "User", back_populates="assignments_received", foreign_keys=[assigned_to]
    )

    assigner = relationship(
        "User", back_populates="assignments_created", foreign_keys=[assigned_by]
    )
