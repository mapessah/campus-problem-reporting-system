from enum import Enum


class UserRole(str, Enum):
    REPORTER = "REPORTER"
    TECHNICIAN = "TECHNICIAN"
    ADMIN = "ADMIN"


class ReportCategory(str, Enum):
    ELECTRICAL = "ELECTRICAL"
    PLUMBING = "PLUMBING"
    FURNITURE = "FURNITURE"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    CLEANING = "CLEANING"
    ICT = "ICT"
    SECURITY = "SECURITY"
    OTHER = "OTHER"


class ReportStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    ESCALATED = "ESCALATED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class ReportPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
