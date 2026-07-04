from abc import ABC, abstractmethod


class SpeechProvider(ABC):
    @abstractmethod
    def transcribe(self, audio_bytes: bytes) -> str:
        """Convert speech audio into text."""

    @abstractmethod
    def synthesize(self, text: str, voice: str | None = None) -> bytes:
        """Convert text into speech audio."""


class StubSpeechProvider(SpeechProvider):
    def transcribe(self, audio_bytes: bytes) -> str:
        return ""

    def synthesize(self, text: str, voice: str | None = None) -> bytes:
        return b""
