"""server_example."""
import asyncio
import os.path
import threading

from socket_cyg.socket_server_asyncio import CygSocketServerAsyncio

def save(data):
    """保存文件的函数."""
    dir_path, datas = list(data.keys())[0], list(data.values())[0]
    dir_path = dir_path.decode("UTF-8")
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(f"{dir_path}/a.rar", "ab+") as f:
        f.write(datas)


if __name__ == '__main__':
    server = CygSocketServerAsyncio(end_identifier=b"@__@")

    def run_server():
        """启动server."""
        asyncio.run(server.run_socket_server())

    def run_consumer():
        """启动消费队列."""
        asyncio.run(server.consumer(save))

    threading.Thread(target=run_server).start()
    threading.Thread(target=run_consumer).start()
