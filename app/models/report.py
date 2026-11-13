from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base
from app.models.enums import ReportCategory, ReportPriority, ReportStatus


class Report(Base):
    __tablename__ = "reports"

    report_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    category: Mapped[ReportCategory] = mapped_column(
        SQLEnum(ReportCategory, name="report_category", native_enum=False),
        nullable=False,
    )

    location: Mapped[str] = mapped_column(String(255), nullable=False)

    image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    reporter_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False
    )

    assigned_to: Mapped[int | None] = mapped_column(
        ForeignKey("users.user_id"), nullable=True
    )

    status: Mapped[ReportStatus] = mapped_column(
        SQLEnum(ReportStatus, name="report_status", native_enum=False),
        default=ReportStatus.SUBMITTED,
        nullable=False,
    )

    priority: Mapped[ReportPriority] = mapped_column(
        SQLEnum(ReportPriority, name="report_priority", native_enum=False),
        default=ReportPriority.MEDIUM,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # User who submitted the report
    reporter = relationship(
        "User", back_populates="submitted_reports", foreign_keys=[reporter_id]
    )

    # Technician currently responsible
    assignee = relationship(
        "User", back_populates="assigned_reports", foreign_keys=[assigned_to]
    )

    assignments = relationship(
        "Assignment", back_populates="report", order_by="Assignment.assigned_at"
    )

    comments = relationship(
        "Comment", back_populates="report", order_by="Comment.created_at"
    )

    notifications = relationship("Notification", back_populates="report")
