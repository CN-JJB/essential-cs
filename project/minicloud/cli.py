"""Command-line entry point (P0/P1/P6/P7).

Operational commands plus the bounded demonstrations. Every command prints
JSON so its output is directly usable as evidence.

Examples::

    python -m minicloud.cli preflight
    python -m minicloud.cli init --fixture
    python -m minicloud.cli serve --port 8765
    python -m minicloud.cli run-indexer --port-file project/var/indexer.port
    python -m minicloud.cli bench
    python -m minicloud.cli race
    python -m minicloud.cli walkthrough
    python -m minicloud.cli backup --out project/var/backup.db
    python -m minicloud.cli restore --in project/var/backup.db
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from . import __version__, httpd, indexer
from .config import Config
from .dependency import IndexerClient
from .observability import Observability
from .service import MiniCloudService
from .store import Store

FIXTURE_USERS = (("alice", "alice-password"), ("bob", "bob-password"))


def _print(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _service(config: Config, *, echo_logs: bool = False) -> MiniCloudService:
    obs = Observability(log_path=config.log_path, echo=echo_logs)
    store = Store(config.db_path)
    dependency = None
    if config.indexer_url:
        dependency = IndexerClient(
            config.indexer_url,
            timeout_ms=config.dep_timeout_ms,
            max_attempts=config.dep_max_attempts,
            observability=obs,
        )
    return MiniCloudService(store=store, config=config, observability=obs, dependency=dependency)


# ---------------------------------------------------------------- commands
def cmd_preflight(args, config: Config) -> int:
    from .config import environment_report

    checks = environment_report()
    checks["db_path"] = config.db_path
    ok = checks["python_ok"] and checks["sqlite_ok"]
    _print({"result": "PASS" if ok else "FAIL", **checks})
    return 0 if ok else 1


def cmd_init(args, config: Config) -> int:
    service = _service(config)
    applied = service.initialize()
    created = []
    if args.fixture:
        for username, password in FIXTURE_USERS:
            if service.store.get_user_by_username(username) is None:
                service.create_user(username, password)
                created.append(username)
    _print(
        {
            "result": "PASS",
            "db_path": config.db_path,
            "migrations_applied": applied,
            "schema_version": service.store.schema_version(),
            "fixture_users_created": created,
        }
    )
    return 0


def cmd_migrate(args, config: Config) -> int:
    store = Store(config.db_path)
    applied = store.migrate()
    _print({"result": "PASS", "migrations_applied": applied, "schema_version": store.schema_version()})
    return 0


def cmd_reset(args, config: Config) -> int:
    store = Store(config.db_path)
    removed = store.reset()
    _print({"result": "PASS", "removed": removed})
    return 0


def cmd_backup(args, config: Config) -> int:
    store = Store(config.db_path)
    target = store.backup_to(args.out)
    _print(
        {
            "result": "PASS",
            "backup_path": target,
            "schema_version": store.schema_version(),
            "source": config.db_path,
        }
    )
    return 0


def cmd_restore(args, config: Config) -> int:
    store = Store(config.db_path)
    store.restore_from(args.infile)
    _print(
        {
            "result": "PASS",
            "restored_from": args.infile,
            "target": config.db_path,
            "schema_version": store.schema_version(),
            "integrity_check": store.integrity_check(),
        }
    )
    return 0


def cmd_serve(args, config: Config) -> int:
    service = _service(config, echo_logs=args.echo_logs)
    service.initialize()
    server = httpd.create_server(service, host=args.host or config.host, port=args.port or config.port)
    host, port = server.server_address[0], server.server_address[1]
    if args.port_file:
        parent = os.path.dirname(os.path.abspath(args.port_file))
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(args.port_file, "w", encoding="utf-8") as handle:
            handle.write(str(port))
    _print(
        {
            "result": "PASS",
            "listening": f"http://{host}:{port}",
            "db_path": config.db_path,
            "indexer_url": config.indexer_url,
            "schema_version": service.store.schema_version(),
        }
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def cmd_run_indexer(args, config: Config) -> int:
    return indexer.main(
        ["--host", args.host, "--port", str(args.port), "--fault", args.fault]
        + (["--port-file", args.port_file] if args.port_file else [])
    )


def cmd_bench(args, config: Config) -> int:
    from .bench import run_benchmark

    result = run_benchmark(rows=args.rows, repetitions=args.repetitions)
    _print(result)
    return 0 if result["disposition"] == "PASS" else 1


def cmd_race(args, config: Config) -> int:
    from .race import run_concurrency_demo

    result = run_concurrency_demo()
    _print(result)
    return 0 if result["disposition"] == "PASS" else 1


def cmd_walkthrough(args, config: Config) -> int:
    from .walkthrough import run_walkthrough

    result = run_walkthrough(log_path=config.log_path)
    _print(result)
    return 0 if result["disposition"] == "PASS" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="minicloud", description="Essential CS Mini Cloud")
    parser.add_argument("--version", action="version", version=f"minicloud {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("preflight", help="check the canonical environment floors")
    p.set_defaults(func=cmd_preflight)

    p = sub.add_parser("init", help="create/migrate the database (idempotent)")
    p.add_argument("--fixture", action="store_true", help="also create the alice/bob fixture users")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("migrate", help="apply pending schema migrations")
    p.set_defaults(func=cmd_migrate)

    p = sub.add_parser("reset", help="remove the database and sidecar files")
    p.set_defaults(func=cmd_reset)

    p = sub.add_parser("backup", help="write a consistent backup copy")
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_backup)

    p = sub.add_parser("restore", help="restore from a backup copy")
    p.add_argument("--in", dest="infile", required=True)
    p.set_defaults(func=cmd_restore)

    p = sub.add_parser("serve", help="run the HTTP service")
    p.add_argument("--host", default=None)
    p.add_argument("--port", type=int, default=None)
    p.add_argument("--port-file", default=None, help="write the bound port here (for scripted startup)")
    p.add_argument("--echo-logs", action="store_true", help="also write structured logs to stdout")
    p.set_defaults(func=cmd_serve)

    p = sub.add_parser("run-indexer", help="run the loopback indexer dependency")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=0)
    p.add_argument("--port-file", default=None)
    p.add_argument("--fault", default="ok", choices=indexer.FAULT_MODES)
    p.set_defaults(func=cmd_run_indexer)

    p = sub.add_parser("bench", help="run the P4 index/measurement benchmark")
    p.add_argument("--rows", type=int, default=4000)
    p.add_argument("--repetitions", type=int, default=25)
    p.set_defaults(func=cmd_bench)

    p = sub.add_parser("race", help="run the P5 concurrency demonstration")
    p.set_defaults(func=cmd_race)

    p = sub.add_parser("walkthrough", help="run the P9 integrated walkthrough")
    p.set_defaults(func=cmd_walkthrough)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = Config.from_env()
    return args.func(args, config)


if __name__ == "__main__":
    sys.exit(main())
