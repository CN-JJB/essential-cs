"""Shared test helpers.

``unittest discover -s project/tests`` puts this directory on ``sys.path``;
the bootstrap below then puts the ``project`` directory on ``sys.path`` so
``import minicloud`` resolves without requiring an install step.
"""

from __future__ import annotations

import os
import socket
import sys
import tempfile
import threading
import time

_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_DIR not in sys.path:
    sys.path.insert(0, _PROJECT_DIR)

from minicloud import httpd, indexer  # noqa: E402
from minicloud.client import MiniCloudClient  # noqa: E402
from minicloud.config import Config  # noqa: E402
from minicloud.dependency import IndexerClient  # noqa: E402
from minicloud.observability import Observability  # noqa: E402
from minicloud.service import MiniCloudService  # noqa: E402
from minicloud.store import Store  # noqa: E402

TEST_PBKDF2_ITERATIONS = "10000"
PASSWORD = "test-password"


def make_service(tmpdir: str, **env_overrides) -> tuple[MiniCloudService, Config, Observability]:
    env = {
        "MINICLOUD_DB_PATH": os.path.join(tmpdir, "minicloud.db"),
        "MINICLOUD_PBKDF2_ITERATIONS": TEST_PBKDF2_ITERATIONS,
    }
    env.update(env_overrides)
    config = Config.from_env(env)
    observability = Observability(log_path=config.log_path)
    store = Store(config.db_path)
    dependency = None
    if config.indexer_url:
        dependency = IndexerClient(
            config.indexer_url,
            timeout_ms=config.dep_timeout_ms,
            max_attempts=config.dep_max_attempts,
            observability=observability,
        )
    service = MiniCloudService(
        store=store, config=config, observability=observability, dependency=dependency
    )
    service.initialize()
    return service, config, observability


class BlackHoleServer:
    """Accepts TCP connections and never answers — a deterministic timeout source.

    Used to prove the *client* deadline behaviour without depending on a slow
    dependency sleeping for a fixed wall-clock duration.
    """

    def __init__(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(("127.0.0.1", 0))
        self._sock.listen(8)
        self.host, self.port = self._sock.getsockname()
        self._stop = threading.Event()
        self._held: list[socket.socket] = []
        self._thread = threading.Thread(target=self._run, name="blackhole", daemon=True)
        self._thread.start()

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                conn, _ = self._sock.accept()
            except OSError:
                return
            self._held.append(conn)  # keep it open, send nothing

    def close(self) -> None:
        self._stop.set()
        for conn in self._held:
            try:
                conn.close()
            except OSError:
                pass
        try:
            self._sock.close()
        except OSError:
            pass


class RunningStack:
    """Context manager: indexer dependency + HTTP service + client, on loopback."""

    def __init__(self, tmpdir: str, *, indexer_fault: str = "ok", client_timeout_ms: int = 3000, **env_overrides):
        self.tmpdir = tmpdir
        self.indexer_fault = indexer_fault
        self.client_timeout_ms = client_timeout_ms
        self.env_overrides = env_overrides
        self._indexer_server = None
        self._http_server = None

    def __enter__(self) -> "RunningStack":
        self._indexer_server, _t, indexer_url = indexer.serve_in_thread(fault_mode=self.indexer_fault)
        env = {"MINICLOUD_INDEXER_URL": indexer_url, "MINICLOUD_DEP_TIMEOUT_MS": "1500"}
        env.update(self.env_overrides)
        self.service, self.config, self.observability = make_service(self.tmpdir, **env)
        self._http_server, _t2, self.base_url = httpd.serve_in_thread(self.service)
        self.client = MiniCloudClient(self.base_url, timeout_ms=self.client_timeout_ms)
        self.indexer_url = indexer_url
        return self

    def set_fault(self, mode: str) -> None:
        import json
        import urllib.request

        request = urllib.request.Request(
            f"{self.indexer_url}/control/fault",
            data=json.dumps({"mode": mode}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=5):
            pass

    def new_client(self, timeout_ms: int) -> MiniCloudClient:
        return MiniCloudClient(self.base_url, timeout_ms=timeout_ms)

    def register_and_login(self, username: str) -> str:
        assert self.client.create_user(username, PASSWORD).status == 201
        return self.client.login(username, PASSWORD).body["token"]

    def __exit__(self, *exc) -> None:
        for server in (self._http_server, self._indexer_server):
            if server is not None:
                try:
                    server.shutdown()
                    server.server_close()
                except Exception:  # noqa: BLE001
                    pass
        # Give the loopback sockets a moment to be released before tmp cleanup.
        time.sleep(0.05)
        return None


def temp_dir() -> str:
    return tempfile.mkdtemp(prefix="minicloud-test-")
