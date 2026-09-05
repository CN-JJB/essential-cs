#!/usr/bin/env python3
"""
Alias entry point for M16 RPC fixture per S6 Design Dossier naming.
Re-exports all symbols from rpc_fixture.
"""

from .rpc_fixture import (
    FaultAction,
    FaultShim,
    IdempotencyStore,
    RetryPolicy,
    RPCClient,
    RPCServer,
    recv_exact,
    recv_msg,
    send_msg,
)

__all__ = [
    "FaultAction",
    "FaultShim",
    "IdempotencyStore",
    "RetryPolicy",
    "RPCClient",
    "RPCServer",
    "recv_exact",
    "recv_msg",
    "send_msg",
]
