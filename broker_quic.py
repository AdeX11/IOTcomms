import asyncio
import os
import aioquic
from aioquic.asyncio import serve, QuicConnectionProtocol
from aioquic.tls import SessionTicket
from aioquic.quic.configuration import QuicConfiguration
from typing import Callable, Deque, Dict, List, Optional, Union, cast
from aioquic.quic.events import DatagramFrameReceived, ProtocolNegotiated, QuicEvent

class SessionTicketStore:
    """
    Simple in-memory store for session tickets.
    """

    def __init__(self) -> None:
        self.tickets: Dict[bytes, SessionTicket] = {}

    def add(self, ticket: SessionTicket) -> None:
        self.tickets[ticket.ticket] = ticket

    def pop(self, label: bytes) -> Optional[SessionTicket]:
        return self.tickets.pop(label, None)


class QuicMqttBrokerProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscriptions = {}  # Dictionary to store subscriptions

    def quic_event_received(self, event: QuicEvent) -> None:
        if isinstance(event, aioquic.quic.events.StreamDataReceived):
            print("received")
            data = event.data.decode("utf-8")

            # MQTT handling logic
            parts = data.split('|')
            if len(parts) == 2 and parts[0] == "SUBSCRIBE":
                topic = parts[1]
                if topic not in self.subscriptions:
                    self.subscriptions[topic] = set()
                self.subscriptions[topic].add(event.stream_id)
                print(f"New subscription to topic: {topic}")
            elif len(parts) == 2 and parts[0] == "PUBLISH":
                topic, message = parts[1].split(':')
                if topic in self.subscriptions:
                    print(f"Received message: {message} on topic: {topic}")
                    for stream_id in self.subscriptions[topic]:
                        self._send_message(stream_id, f"Received: {message}")

    def _send_message(self, stream_id, message):
        stream = self._quic._get_or_create_stream(stream_id)
        stream.send_data(message.encode("utf-8"))

async def main():
    # Load TLS certificate and key
    certfile = "cert.pem"
    keyfile = "cert.key"
    if not (os.path.exists(certfile) and os.path.exists(keyfile)):
        print(f"Please provide valid TLS certificate ({certfile}) and key ({keyfile}) paths.")
        return

    # Create TLS configuration
    configuration = QuicConfiguration(is_client=False, verify_mode=0)
    configuration.load_cert_chain(certfile, keyfile)
    session_ticket_store = SessionTicketStore()
    # Start QUIC server with TLS
    server = await serve("localhost", 4433, create_protocol=QuicMqttBrokerProtocol, configuration=configuration,session_ticket_fetcher=session_ticket_store.pop,
        session_ticket_handler=session_ticket_store.add,retry=True)
    await asyncio.Future()
# Run the broker server
if __name__ == "__main__":
    asyncio.run(main())
