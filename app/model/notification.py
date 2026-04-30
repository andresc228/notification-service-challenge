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

class ConsoleChannel(NotificationChannel):

    def send(self, message: str) -> None:
        try:
            print(message)
        except Exception:
            raise DeliveryError("Error al imprimir en consola")

    def get_channel_name(self) -> str:
        return "console"

    def is_available(self) -> bool:
        return True

class FileChannel(NotificationChannel):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def is_available(self) -> bool:
        directorio = os.path.dirname(self.file_path) or '.'
        return os.access(directorio, os.W_OK)

    def get_channel_name(self) -> str:
        return f"file: {self.file_path}"

    def send(self, message: str) -> None:
        if not self.is_available():
            raise ChannelUnavailableError("Archivo no disponible")

        try:
            with open(self.file_path, "a") as f:
                f.write(message + "\n")
        except Exception:
            raise DeliveryError("Error al escribir en archivo")

class MockChannel(NotificationChannel):

    def send(self, message: str) -> None:
        raise ChannelUnavailableError("Canal mock no disponible")

    def get_channel_name(self) -> str:
        return "mock"

    def is_available(self) -> bool:
        return False