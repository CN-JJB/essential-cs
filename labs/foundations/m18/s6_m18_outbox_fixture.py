#!/usr/bin/env python3
"""
Facade for the M18 transactional-outbox fixture name retained by the Design Dossier.

Supports both:
- direct sibling/script loading from labs/foundations/m18; and
- package-style imports when the repository is imported as a namespace package.
"""

if __package__:
    from .outbox_fixture import (
        DeliveryBuffer,
        DualWriteCrashError,
        OutboxRelay,
        RelayCrashBeforeMarkError,
        Worker,
        init_database,
        produce_broken_dual_write,
        produce_transactional_outbox,
    )
else:
    from outbox_fixture import (
        DeliveryBuffer,
        DualWriteCrashError,
        OutboxRelay,
        RelayCrashBeforeMarkError,
        Worker,
        init_database,
        produce_broken_dual_write,
        produce_transactional_outbox,
    )


__all__ = [
    "DeliveryBuffer",
    "DualWriteCrashError",
    "OutboxRelay",
    "RelayCrashBeforeMarkError",
    "Worker",
    "init_database",
    "produce_broken_dual_write",
    "produce_transactional_outbox",
]
