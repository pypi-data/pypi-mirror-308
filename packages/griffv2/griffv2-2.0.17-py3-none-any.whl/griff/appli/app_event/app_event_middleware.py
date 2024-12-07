from abc import ABC, abstractmethod

from griff.appli.app_event.app_event import AppEvent
from griff.appli.message.message_middleware import MessageMiddleware, MessageContext


class AppEventMiddleware(MessageMiddleware[AppEvent, None], ABC):
    @abstractmethod
    async def dispatch(
        self, message: AppEvent, context: MessageContext | None = None
    ) -> None:
        pass
