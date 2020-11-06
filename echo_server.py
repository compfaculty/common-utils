import nest_asyncio

nest_asyncio.apply()
import asyncio
import subprocess
import shlex
from loguru import logger


class EchoProtocol(asyncio.Protocol):

    def connection_made(self, transport):

        peername = transport.get_extra_info('peername')
        logger.info(f'Connection from {peername}')
        self.transport = transport

    def connection_lost(self, exc):
        logger.info(f"Connection lost {self.transport.get_extra_info('peername')}, {exc or ''}")

    def pause_writing(self):
        logger.info(f"Pause writing")

    def resume_writing(self):
        logger.info(f"Resume writing")

    def data_received(self, data):
        msg = data.decode()
        logger.info(msg)
        pid = subprocess.Popen(shlex.split(msg), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            data, errors = pid.communicate(timeout=600)
        except subprocess.TimeoutExpired:
            pid.kill()
            data, errors = pid.communicate()
        finally:
            self.transport.write(data)


loop = asyncio.get_event_loop()
coro = loop.create_server(EchoProtocol, 'localhost', 5573)
server = loop.run_until_complete(coro)
loop.run_forever()
# try:
#     loop.run_forever()
# except:
#     loop.run_until_complete(server.wait_closed())
# finally:
#     loop.close()
