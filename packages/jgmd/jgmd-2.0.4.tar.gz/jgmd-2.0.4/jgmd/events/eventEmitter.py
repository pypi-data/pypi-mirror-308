from __future__ import annotations
from typing import Callable, Dict, List
import asyncio
from dataclasses import dataclass
from .eventTypes import EventTypes
from ..util import exceptionToStr


_emitter: EventEmitter = None


def getEmitter() -> EventEmitter:
    global _emitter
    if _emitter is None:
        _emitter = EventEmitter()
    return _emitter


@dataclass
class EmissionMetrics:
    numEmissions: int = 0
    numSuccessfulEmissions: int = 0


class EventEmitter:
    _events: Dict[str, List[Callable]]  # instance variable

    def __init__(self):
        if _emitter is not None:
            raise Exception(
                "EventEmitter must be a singleton! Use getEmitter() to create/get the instance."
            )
        self.init()

    def init(self):
        self._events = {}

    def on(self, event: str, listener: Callable):
        if event not in self._events:
            self._events[event] = []
        self._events[event].append(listener)

    def off(self, event: str, listener: Callable):
        if event in self._events:
            self._events[event].remove(listener)
            if not self._events[event]:  # If the list is empty, remove the event entry
                del self._events[event]

    def _getAwaitableListeners(self, event: str, *args, **kwargs):
        if event in self._events:
            awaitables = []
            errorStrs = []
            for listener in self._events[event]:
                if asyncio.iscoroutinefunction(listener):
                    # collect async awaitables to invoke later
                    awaitables.append(
                        self._async_listener_wrapper(listener, event, *args, **kwargs)
                    )
                else:
                    # immediately invoke non-async functions
                    try:
                        listener(event, *args, **kwargs)
                    except Exception as e:
                        errorStrs.append(exceptionToStr(e))
            if errorStrs:
                self.emit(
                    EventTypes.App.ERROR,
                    f"Error during '{event}' event emission!\n"
                    + "\n\n".join(errorStrs),
                )
            return awaitables

    async def emitAsync(self, event: str, *args, **kwargs):
        awaitables = self._getAwaitableListeners(event, *args, **kwargs)
        if awaitables:
            await asyncio.gather(*awaitables)

    def emit(self, event: str, *args, **kwargs):
        awaitables = self._getAwaitableListeners(event, *args, **kwargs)
        if awaitables:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.ensure_future(asyncio.gather(*awaitables))
            else:
                loop.run_until_complete(asyncio.gather(*awaitables))

    async def _async_listener_wrapper(self, listener, event, *args, **kwargs):
        try:
            await listener(event, *args, **kwargs)
        except Exception as e:
            error_message = exceptionToStr(e)
            self.emit(EventTypes.App.ERROR, error_message)
