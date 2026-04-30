import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable
from abc import ABC, abstractmethod

from app.services.util import generate_unique_id

class NotificationError(Exception):
    pass

class ChannelUnavailableError(NotificationError):
    pass

class DeliveryError(NotificationError):
    pass

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...

    @abstractmethod
    def get_channel_name(self) -> str: ...

    @abstractmethod
    def is_available(self) -> bool: ...