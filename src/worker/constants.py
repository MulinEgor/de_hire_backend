"""Модуль для констант для пакета worker"""

from src.core.jobs.models import JobStatus
from src.core.settings import settings

EVENT_TO_STATUS = {
    "JobAssignedEvent": JobStatus.IN_PROGRESS,
    "JobWaitingReviewEvent": JobStatus.WAITING_REVIEW,
    "JobCompletedEvent": JobStatus.COMPLETED,
    "JobCancelledEvent": JobStatus.CANCELLED,
    "JobReopenedEvent": JobStatus.OPEN,
}
WEBSOCKET_URL: str = f"wss://sepolia.infura.io/ws/v3/{settings.INFURA_PROJECT_ID}"
ABI_URL: str = f"https://api-sepolia.etherscan.io/api?module=contract&action=getabi&address={settings.CONTRACT_ADDRESS}&apikey={settings.ETHERSCAN_API_KEY}"
