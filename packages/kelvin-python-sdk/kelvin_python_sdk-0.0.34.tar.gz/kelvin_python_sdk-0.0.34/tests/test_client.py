import asyncio
from asyncio import StreamReader, StreamWriter
from unittest.mock import Mock

import pytest
import pytest_asyncio

from kelvin.application.client import KelvinApp
from kelvin.application.stream import KelvinStream, KelvinStreamConfig
from kelvin.krn import KRN, KRNAssetDataStream
from kelvin.message import Number, StringParameter

pytest_plugins = ("pytest_asyncio",)


# Setup server
async def made_server(reader: StreamReader, writer: StreamWriter):
    print("Made server")
    while not writer.is_closing():
        data = await reader.readline()
        if data:
            writer.write(data)
            await writer.drain()
        await asyncio.sleep(0.05)


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module", autouse=True)
async def start_server(event_loop):
    print("Setting up server")
    server = await asyncio.start_server(made_server, "127.0.0.1", KelvinStreamConfig().port)
    asyncio.get_event_loop().create_task(server.serve_forever())
    yield server
    server.close()
    await server.wait_closed()


# Stream Tests
@pytest.mark.asyncio
async def test_connect():
    stream = KelvinStream()
    await stream.connect()
    await stream.disconnect()


@pytest.mark.asyncio
async def test_rw():
    stream = KelvinStream()
    await stream.connect()
    msg = Number(payload=1.0, resource=KRNAssetDataStream("foo", "bar"))
    await stream.write(msg)
    msg2 = await stream.read()
    await stream.disconnect()
    assert msg == msg2


# Client Tests
@pytest.mark.asyncio
async def test_client_connect():
    client = KelvinApp()

    event = asyncio.Event()
    event.set()
    mock_wait = Mock(side_effect=lambda: event.wait())

    client.config_received.wait = mock_wait

    await client.connect()
    await client.disconnect()


@pytest.mark.asyncio
async def test_client_ctx():
    event = asyncio.Event()
    event.set()
    mock_wait = Mock(side_effect=lambda: event.wait())

    client = KelvinApp()
    client.config_received.wait = mock_wait

    async with client as client:
        assert client
