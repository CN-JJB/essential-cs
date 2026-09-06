#!/usr/bin/env python3
"""
Alias / facade module for s6_m18_outbox_fixture.py.
Preserves the naming specified in Section 19 of the Design Dossier.
"""

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
