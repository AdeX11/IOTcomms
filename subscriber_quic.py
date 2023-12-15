import asyncio
import aioquic
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio import QuicConnectionProtocol
from aioquic.asyncio import connect

async def main():
    async with connect("localhost", 4433, configuration=QuicConfiguration(is_client=True, verify_mode=0)) as quic:
       
        reader, writer = await quic.create_stream()
        quic._stream_handler(reader,writer)
        # Subscribe to a topic
        message = "SUBSCRIBE|topic/A"
        print(f"Sending: {message}")
        quic._quic.send_stream_data(id,message.encode("utf-8"),False)
        writer.write(message.encode("utf-8"))
        
        # Ensure the message is sent
        await writer.drain()
        await asyncio.Future()

# Run the subscriber
if __name__ == "__main__":
    asyncio.run(main())
