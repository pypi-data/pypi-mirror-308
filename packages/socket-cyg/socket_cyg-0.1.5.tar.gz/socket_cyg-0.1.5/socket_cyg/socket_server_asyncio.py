"""异步socket."""
import asyncio
import datetime
import logging
import os
import socket
import sys
from asyncio import AbstractEventLoop
from logging.handlers import TimedRotatingFileHandler
from typing import Union


# pylint: disable=R0801, disable=R0902
class CygSocketServerAsyncio:
    """异步socket class."""
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s"

    clients = {}  # 保存已连接的client
    tasks = {}
    loop: AbstractEventLoop = None

    def __init__(self, address="127.0.0.1", port=8000, key_value_split=b"-_-", end_identifier=b"@_@"):
        self._address = address
        self._port = port
        self._key_value_split = key_value_split
        self._end_identifier = end_identifier
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")
        self._file_handler = None
        self.set_log()
        self.queue = asyncio.Queue()

    def set_log(self):
        """设置日志."""
        self.file_handler.setFormatter(logging.Formatter(self.LOG_FORMAT))
        self.file_handler.setLevel(logging.INFO)
        self.logger.addHandler(self.file_handler)
        if sys.version_info.minor == 11:
            logging.basicConfig(level=logging.INFO, encoding="UTF-8", format=self.LOG_FORMAT)
        else:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(self.LOG_FORMAT))
            console_handler.setLevel(logging.INFO)
            self.logger.addHandler(console_handler)
            self.logger.setLevel(logging.INFO)

    @property
    def file_handler(self):
        """保存日志的日志器."""
        if self._file_handler is None:
            log_dir = f"{os.getcwd()}/log"
            os.makedirs(log_dir, exist_ok=True)
            file_name = f"{log_dir}/{datetime.datetime.now().strftime('%Y-%m-%d')}_{os.path.basename(os.getcwd())}.log"
            self._file_handler = TimedRotatingFileHandler(
                file_name, when="D", interval=1, backupCount=10, encoding="UTF-8"
            )
        return self._file_handler

    @property
    def logger(self):
        """日志实例."""
        return self._logger

    async def consumer(self, operation_func: callable):
        """获取队列里客户端发来的数据进行处理.

        Args:
            operation_func: 处理函数.
        """
        while True:
            while self.queue.qsize() != 0:
                data = await self.queue.get()
                operation_func(data)
                self.queue.task_done()

    async def socket_send(self, client_connection, data: Union[bytes, str]):
        """发送数据给客户端."""
        if isinstance(data, str):
            data = data.encode("UTF-8")
        if client_connection:
            client_ip = client_connection.getpeername()
            await self.loop.sock_sendall(client_connection, data)
            self._logger.info("*** 发送 *** --> %s 发送成功, %s", client_ip, data)
        else:
            self._logger.info("*** 发送 *** --> 发送失败, %s, 未连接", data)

    async def receive_send(self, client_connection: socket.socket):
        """接收发送数据."""
        client_ip = client_connection.getpeername()[0]  # 获取连接客户端的ip
        self._logger.info("%s 处理 %s 客户端的任务开始 %s", "-" * 30, client_ip, "-" * 30)
        buffer_byte = b""
        try:
            while data_byte := await self.loop.sock_recv(client_connection, 1024 * 1024):
                buffer_byte += data_byte
                if self._end_identifier in buffer_byte:
                    one_message_byte, remaining = buffer_byte.split(self._end_identifier, 1)
                    buffer_byte = remaining
                    keys, datas = one_message_byte.split(self._key_value_split, 1)
                    await self.queue.put({keys: datas})
                    await self.socket_send(client_connection, b"^_^")
                    self._logger.info("*** 收到一条完整消息 ***")
                    self._logger.info("keys: %s", keys)
                    self._logger.info("*** 正在根据消息执行操作 ***")
                    self._logger.debug("datas: %s", datas)

        except Exception as e:  # pylint: disable=W0718
            self._logger.warning("*** 通讯出现异常 *** --> 异常信息是: %s", e)
        finally:
            self.clients.pop(client_ip)
            self.tasks.get(client_ip).cancel()
            self._logger.warning("*** 下位机断开 *** --> %s, 断开了", client_ip)
            self._logger.info("%s 处理 %s 客户端的任务结束 %s", "-" * 30, client_ip, "-" * 30)
            client_connection.close()

    async def listen_for_connection(self, socket_server: socket):
        """异步监听连接."""
        self._logger.info("*** 服务端已启动 *** --> %s 等待客户端连接", socket_server.getsockname())

        while True:
            self.loop = asyncio.get_running_loop()
            client_connection, address = await self.loop.sock_accept(socket_server)
            self._logger.warning("*** 下位机连接 *** --> %s, 连接了", address)
            client_connection.setblocking(False)
            await self.socket_send(client_connection, "^_^")
            self.clients.update({address[0]: client_connection})
            self.tasks.update({address[0]: self.loop.create_task(self.receive_send(client_connection))})
            self._logger.warning("*** 创建了处理 %s 客户端的任务 ***", address)

    async def run_socket_server(self):
        """运行socket服务, 并监听客户端连接."""
        socket_server = socket.socket()
        socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_server.setblocking(False)
        socket_server.bind((self._address, self._port))
        socket_server.listen()
        await self.listen_for_connection(socket_server)
