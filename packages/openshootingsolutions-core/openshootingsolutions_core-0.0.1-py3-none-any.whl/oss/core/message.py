from __future__ import annotations

import json
from enum import Enum
from uuid import uuid4

import pika
from pika.exchange_type import ExchangeType
from pydantic import UUID4, BaseModel, Field


class BrokerExchangeType(Enum):
    FANOUT: ExchangeType = ExchangeType.fanout
    TOPIC: ExchangeType = ExchangeType.topic


class BrokerConnection:
    _connection: pika.BlockingConnection
    channel: pika.adapters.blocking_connection.BlockingChannel

    def __init__(self, host: str, port: int):
        connection_parameters = pika.ConnectionParameters(
            host=host,
            port=port,
        )
        self._connection = pika.BlockingConnection(parameters=connection_parameters)
        self.channel = self._connection.channel()

    def setup_channel(self, name: str, exchange_type: BrokerExchangeType):
        self.channel.exchange_declare(exchange=name, exchange_type=exchange_type.value)


class BrokerMessage(BaseModel):
    model_config = {
        "extra": "ignore",  # Prevent unwanted extra fields from being added to this class
    }
    producer: UUID4 = Field(
        examples=["00000000-0000-0000-0000-000000000000"],
        description="The unique identifier of the producer of this broker message.",
    )
    identifier: UUID4 = Field(
        examples=["00000000-0000-0000-0000-000000000000"],
        description="The unique identifier of this broker message.",
        default=uuid4(),
    )
    body: dict

    def send(
        self,
        broker_connection: BrokerConnection,
        exchange: str,
        routing_key: str,
    ) -> None:
        """
        Sends the message to the topic on the message broker.
        Args:

        Returns:
            None
        """

        # Needs to be serialized to a json string
        serialized_message = self.to_json()

        # The serialized message needs to be encoded to bytes
        encoded_message = serialized_message.encode()
        broker_connection.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=encoded_message)

    def send_rpc(self, callback_function) -> BrokerMessage:
        """
        Sends a rpc request to on the message broker

        The result will be passed to the passed callback function.
        The result will be a class derived of BaseBrokerReply.
        Args:

        Returns:
            None
        """
        raise NotImplementedError

    def to_json(self) -> str:
        serialized_message: str = self.model_dump_json()

        return serialized_message

    @staticmethod
    def from_json(serialized_message: str) -> BrokerMessage:
        broker_message: dict = json.loads(serialized_message)

        deserialized_message: BrokerMessage = BrokerMessage(**broker_message)

        return deserialized_message
