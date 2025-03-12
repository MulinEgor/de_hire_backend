"""Модуль для констант для пакета worker"""

from src.jobs.models import JobStatus

EVENT_TO_STATUS = {
    "JobAssignedEvent": JobStatus.IN_PROGRESS,
    "JobWaitingReviewEvent": JobStatus.WAITING_REVIEW,
    "JobCompletedEvent": JobStatus.COMPLETED,
    "JobCancelledEvent": JobStatus.CANCELLED,
    "JobReopenedEvent": JobStatus.OPEN,
}
