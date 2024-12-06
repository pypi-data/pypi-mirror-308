import socket
import ssl
import threading
from pathlib import Path
from typing import List

import pytest
from testcontainers.core.network import Network
from testcontainers.core.waiting_utils import wait_container_is_ready
from testcontainers.generic import ServerContainer
from testcontainers.postgres import PostgresContainer

from pyrelukko import RelukkoClient

SCRIPT_DIR = Path(__file__).parent.absolute()
INITDB_DIR = SCRIPT_DIR / "initdb.d"


class RelukkoContainer(ServerContainer):
    def __init__(self, net: Network,
                 image="registry.gitlab.com/relukko/relukko:0.9.0", db_url=None):
        self.db_url = db_url
        self.net = net
        super(RelukkoContainer, self).__init__(image=image, port=3000)

    def _configure(self):
        self.with_env("DATABASE_URL", self.db_url)
        self.with_env("RELUKKO_API_KEY", "somekey")
        self.with_env("RELUKKO_USER", "relukko")
        self.with_env("RELUKKO_PASSWORD", "relukko")
        self.with_env("RELUKKO_BIND_ADDR", "0.0.0.0")
        self.with_network(self.net)

    def get_api_url(self) -> str:
        return f"http://localhost:{self.get_exposed_port(3000)}"

    def _create_connection_url(self) -> str:
        return f"{self.get_api_url()}/healthchecker"


class RelukkoDbContainer(PostgresContainer):
    def __init__(self, net: Network, image: str = "postgres:latest", port: int = 5432, username: str | None = None, password: str | None = None, dbname: str | None = None, driver: str | None = "psycopg2", **kwargs) -> None:
        self.net = net
        super().__init__(image, port, username, password, dbname, driver, **kwargs)

    def _configure(self) -> None:
        self.with_volume_mapping(INITDB_DIR, "/docker-entrypoint-initdb.d", "Z")
        self.with_env("POSTGRES_USER", "relukko")
        self.with_env("POSTGRES_PASSWORD", "relukko")
        self.with_env("POSTGRES_DB", "relukko")
        self.with_network(self.net)

    @wait_container_is_ready()
    def _connect(self) -> None:
        packet = bytes([
            0x00, 0x00, 0x00, 0x52, 0x00, 0x03, 0x00, 0x00, 
            0x75, 0x73, 0x65, 0x72, 0x00, 0x72, 0x65, 0x6c, 
            0x75, 0x6b, 0x6b, 0x6f, 0x00, 0x64, 0x61, 0x74, 
            0x61, 0x62, 0x61, 0x73, 0x65, 0x00, 0x72, 0x65, 
            0x6c, 0x75, 0x6b, 0x6b, 0x6f, 0x00, 0x61, 0x70, 
            0x70, 0x6c, 0x69, 0x63, 0x61, 0x74, 0x69, 0x6f, 
            0x6e, 0x5f, 0x6e, 0x61, 0x6d, 0x65, 0x00, 0x70, 
            0x73, 0x71, 0x6c, 0x00, 0x63, 0x6c, 0x69, 0x65, 
            0x6e, 0x74, 0x5f, 0x65, 0x6e, 0x63, 0x6f, 0x64, 
            0x69, 0x6e, 0x67, 0x00, 0x55, 0x54, 0x46, 0x38, 
            0x00, 0x00
        ])
        port = self.get_exposed_port(self.port)
        with socket.create_connection(("localhost", port)) as sock:
            sock.send(packet)
            buf = sock.recv(40)
            if len(buf) == 0 and "SCRAM-SHA" not in buf:
                raise ConnectionError


@pytest.fixture(scope="session")
def relukko_backend():
    with Network() as rl_net:
        with RelukkoDbContainer(net=rl_net,
            image="postgres:16", hostname="relukkodb") as _db:
            db_url = "postgresql://relukko:relukko@relukkodb/relukko"
            with RelukkoContainer(rl_net, db_url=db_url) as backend:
                relukko = RelukkoClient(
                    base_url=backend.get_api_url(), api_key="somekey")
                yield relukko, backend

@pytest.fixture(scope="function")
def tls_listener():

    certfile = SCRIPT_DIR / "cert" / "relukko.crt"
    keyfile = SCRIPT_DIR / "cert" / "relukko.key"

    def run_server(port_info: List, keep_running: threading.Event):
        # Create a TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind(("127.0.0.1", 0))
            sock.listen(5)  # Listen for incoming connections

            _, assigned_port = sock.getsockname()
            port_info.append(assigned_port)

            # Wrap the socket with TLS
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile=certfile, keyfile=keyfile)
            with context.wrap_socket(sock, server_side=True) as ssock:

                ssock.settimeout(1)

                while keep_running.is_set():
                    try:
                        client_socket, _ = ssock.accept()
                        client_socket.sendall(b"Hello, TLS Client!")
                        client_socket.close()
                    except Exception as _:
                        continue

    port_info = []
    keep_running = threading.Event()
    keep_running.set()
    thread = threading.Thread(target=run_server, args=(port_info, keep_running))
    thread.start()

    while not port_info:
        pass

    yield thread, port_info[0]

    keep_running.clear()
    thread.join()
