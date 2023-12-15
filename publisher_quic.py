import asyncio
import aioquic
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio import QuicConnectionProtocol
from aioquic.asyncio import connect

async def publisher():
    async with connect("localhost", 4433, configuration=QuicConfiguration(is_client=True, verify_mode=0)) as quic:
        id=quic._quic.get_next_available_stream_id()
        #reader, writer = await quic.create_stream()
        # Subscribe to a topic

        # Publish a message
        message = "PUBLISH|topic/A:Hello, World!"
        print(f"Sending: {message}")
        quic._quic.send_datagram_frame(message.encode())
        #quic._quic.send_data(id,message.encode("utf-8"),False)

# Run the publisher
if __name__ == "__main__":
    asyncio.run(publisher())
