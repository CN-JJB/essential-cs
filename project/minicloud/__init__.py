"""Mini Cloud — the recurring Essential CS integration surface.

This package implements the accepted Mini Cloud P0–P9 evolution
(`meta/blueprint/mini-cloud-app-evolution-v0.1.md`, aligned by
`meta/blueprint/mini-cloud-curriculum-alignment-v0.1.md`) as a small,
readable, standard-library-only, local-first multi-user note/bookmark
service.

Deliberate boundaries (see ``project/README.md``):

* Standard library only — no web framework, no ORM, no external service.
* One primary process plus one bounded loopback dependency process.
* SQLite is the durable store.
* HTTP is an *adapter*; the service core is transport-independent.
* The domain (personal notes/bookmarks with owners and explicit sharing)
  never changes; only the system constraints around it do.

Nothing here is a claim of ``VERIFIED``, ``RELEASED``, or v1.0 readiness.
"""

from __future__ import annotations

__all__ = ["__version__"]

__version__ = "0.1.0"
