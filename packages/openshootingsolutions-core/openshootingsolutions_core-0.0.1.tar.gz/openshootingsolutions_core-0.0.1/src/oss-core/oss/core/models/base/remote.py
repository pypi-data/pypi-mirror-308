from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Optional
from uuid import UUID, uuid4

from oss.core.message import BrokerConnection, BrokerExchangeType, BrokerMessage
from oss.core.models.base.timer import TimerControl


class BaseHook(ABC):
    name: str
    action: TimerControl

    def __init__(self, name: str, action: TimerControl, callback: Callable[[TimerControl], None]) -> None:
        self.name = name
        self.action = action
        self.callback = callback
        self.register()

    def __del__(self):
        self.remove()

    @abstractmethod
    def register(self):
        raise NotImplementedError

    @abstractmethod
    def remove(self):
        raise NotImplementedError


class BaseRemote(ABC):
    # Each remote needs an uuid so we can keep track of which remote triggered an action.
    # This is mostly for debugging.
    _identifier: UUID = uuid4()

    # References to the configured hooks
    _configured_hooks: list[BaseHook] = []

    # Each remote needs a connection to the message broker to send commands
    _broker_connection: BrokerConnection

    # Each type of remote needs a different hook type
    _hook_type: type[BaseHook]
    _action_schema: type[Enum]

    def __init__(self) -> None:
        self._broker_connection = BrokerConnection(host="localhost", port=5672)
        self._broker_connection.setup_channel(name="remote", exchange_type=BrokerExchangeType.TOPIC)
        self._register_hooks()

    def __del__(self):
        self._remove_hooks()

    def _handle_hook_event(self, action: TimerControl) -> None:
        broker_message: BrokerMessage = BrokerMessage(
            producer=self._identifier,
            body={"action": action.value},
        )
        broker_message.send(
            broker_connection=self._broker_connection,
            exchange="remote",
            routing_key="remote.keypad.action",
        )

    def _register_hooks(self) -> None:
        # If there are already hooks configured, remove them
        if len(self._configured_hooks) >= 1:
            self._remove_hooks()

        for action in self._action_schema:
            hook_type = self._hook_type  # Retrieve the type of the hook for this remote
            hook: BaseHook = hook_type(name=action.name, action=action.value, callback=self._handle_hook_event)
            self._configured_hooks.append(hook)

    def _remove_hooks(self, hooks: Optional[list[BaseHook]] = None) -> None:
        # If the hooks are specified remove those specific hooks.
        if hooks:
            for hook in hooks:
                hook.remove()
        else:  # Else remove all hooks
            for hook in self._configured_hooks:
                hook.remove()
