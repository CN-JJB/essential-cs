# Mini Cloud — the recurring Essential CS integration surface

The Mini Cloud is a deliberately boring multi-user note/bookmark service. It
exists so a learner can trace **one** request through representation, process
boundaries, durable state, concurrency, a real dependency, failure, recovery,
and instrumentation — over and over, as each mechanism is taught.

The domain never changes. Only the system constraints around it do.

---

## 0. Status and honest claims

**Implemented and runnable. Not `VERIFIED`. Not `RELEASED`. Not v1.0.**

This tree exists to close the gap the accepted audit
(`meta/audits/post-v09-v10-gap-stabilization-plan-v0.1.md`, Gate 2) recorded as
`UNSATISFIED — IMPLEMENTATION REQUIRED`: the repository had Mini Cloud *mapping*
but no deployable application. It now has an application. That is an
implementation milestone, not a curriculum verdict:

- no learner-validation evidence is claimed (Issue #34 remains a human gate);
- no `VERIFIED` / `RELEASED` / v1.0 claim follows from this document;
- `OQ-BP-006` is not closed or modified by this project: it is CLOSED as the
  technical environment-definition/realization question (#167), and `#158` must
  still independently re-check the canonical environment before v1.0.

## 0.1 Milestone numbering — read this first

The `P0`–`P9` milestones used here are **the repository's accepted ones**, from
`meta/blueprint/mini-cloud-app-evolution-v0.1.md` and
`meta/blueprint/mini-cloud-curriculum-alignment-v0.1.md`. They are the
authoritative contract; this project does not redefine them.

A common paraphrase maps `P` numbers to a generic "cloud app" progression
(local process → request → validation → persistence → concurrency → network →
reliability → security → observability → integration). **That ordering differs
from the accepted one.** Every capability in that list is implemented, but under
the accepted milestone that owns it — for example security/trust boundaries are
`P2` (not `P7`), the real network path is `P3`, and `P7` is the deployment /
reproducible-environment boundary.

If you are cross-referencing a capability list against this tree, use
[§3](#3-p0p9-implementation-map) below rather than assuming positional parity.

## 1. What this is not

- Not a web framework, frontend, SaaS product, or microservices exercise.
- Not a feature showcase; there is no search ranking, rich editor, upload,
  billing, social graph, or real-time collaboration.
- Not a replacement for mechanism-specific classic labs.
- Not evidence that adding "more infrastructure" is good. Rejection is an
  intended and tested outcome.

## 2. Canonical environment

Everything runs inside the pinned canonical environment — the immutable OCI
digest in `.devcontainer/canonical-image.env`:

```text
ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460
```

Observed floors inside that digest: Ubuntu 24.04 (Noble), `x86_64`,
CPython 3.12.3, SQLite 3.45.1, GCC 13.3.0, curl 8.5.0.

**This project does not modify the canonical pin.** If the Mini Cloud ever
cannot run legally inside it, that is a blocker to report, not a pin to edit.

### Quick start

```bash
bash project/scripts/preflight.sh          # fail-closed environment check
export PYTHONPATH=project                  # when invoking from repo root
python3 -m minicloud.cli init --fixture    # create/migrate DB + alice/bob
python3 -m minicloud.cli run-indexer --port-file project/var/indexer.port &
export MINICLOUD_INDEXER_URL="http://127.0.0.1:$(cat project/var/indexer.port)"
python3 -m minicloud.cli serve --port 8765
```

Then, in another shell:

```bash
curl -fsS http://127.0.0.1:8765/health
curl -fsS -X POST http://127.0.0.1:8765/v1/users \
  -H 'Content-Type: application/json' -d '{"username":"alice","password":"alice-password"}'
TOKEN=$(curl -fsS -X POST http://127.0.0.1:8765/v1/sessions \
  -H 'Content-Type: application/json' -d '{"username":"alice","password":"alice-password"}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["token"])')
curl -fsS -X POST http://127.0.0.1:8765/v1/items \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"kind":"note","title":"first","body":"hello"}'
```

Clean up with `bash project/scripts/reset.sh`.

## 3. P0–P9 implementation map

| Milestone | What exists | Invariant you can check |
|---|---|---|
| **P0** one process, one durable collection | `minicloud/store.py`, `minicloud/cli.py init` | one owner per item; stable ids; read-after-write returns the committed value |
| **P1** process boundary + narrow interface | `minicloud/httpd.py`, `minicloud/client.py`, `cli.py serve` | every request yields one specified response or a bounded error; malformed input never reaches SQL as code |
| **P2** multiple users + trust boundaries | `minicloud/auth.py`, `service.py` authz | a private read/write is authorized for the effective user; denial is indistinguishable from "missing" |
| **P3** real network path + bounded failure | `client.py`, `dependency.py`, `indexer.py` | a timeout is reported as **ambiguous**, never as "not committed"; retries are bounded and key-aware |
| **P4** query shape, index, measurement | `minicloud/bench.py`, `cli.py bench` | results are identical before/after indexing; the plan and the cost are both recorded |
| **P5** concurrency + transactional correctness | `minicloud/race.py`, `cli.py race`, versioned updates | no lost update; a stale writer gets a conflict; a failed transaction leaves no partial state |
| **P6** durable recovery | `store.py` migrations/backup/restore, `cli.py backup/restore` | a completed migration has a known version; restore produces a readable DB with declared loss bounds |
| **P7** deployment boundary + reproducibility | `config.py`, `scripts/preflight.sh`, this README | configuration is injected, state is separate, and the canonical run path is reproducible |
| **P8** instrumentation before scaling | `minicloud/observability.py` | telemetry never changes user-visible correctness; secrets are redacted; labels stay bounded |
| **P9** integrated system reasoning | `minicloud/walkthrough.py`, `cli.py walkthrough` | one run proves request → app → state → dependency → observability → failure → recovery |

### Capability cross-reference (for the alternate numbering)

| Generic capability | Where it actually lives here |
|---|---|
| local process, start command, health check | P0 + P7 (`cli.py serve`, `GET /health`) |
| HTTP request path, curl-verifiable | P1 (`httpd.py`) |
| malformed input, denied request, error semantics | P1 + P2 (`errors.py`, 400/401/404/409) |
| persistence, restart durability | P0 + P6 (`store.py`, `walkthrough` restart step) |
| state / concurrency / consistency | P5 (`race.py`, versioned updates) |
| network/service boundary, latency, timeout, retry | P3 (`client.py`, `dependency.py`) |
| reliability, failure and recovery | P6 + P9 (backup/restore, dependency faults) |
| security boundary, authn/authz, secret separation | P2 (`auth.py`, `config.py`) |
| observability, correlation, latency/error evidence | P8 (`observability.py`) |
| integrated system reasoning | P9 (`walkthrough.py`) |

## 4. Architecture

```text
project/
  minicloud/
    config.py         configuration + secret separation (P7)
    errors.py         typed boundary errors (P1/P2)
    observability.py  structured logs, metrics, redaction (P8)
    schema.py         versioned migrations (P6)
    store.py          SQLite: parameterized SQL, transactions, backup (P0/P5/P6)
    auth.py           PBKDF2 verifiers, opaque session tokens (P2)
    service.py        transport-independent core (P0–P9)
    httpd.py          minimal stdlib HTTP adapter, no framework (P1)
    client.py         timeouts, bounded retry, ambiguity (P3)
    dependency.py     caller side of the bounded dependency (P3/P9)
    indexer.py        the dependency itself, with fault injection (P3/P9)
    bench.py          P4 measurement
    race.py           P5 concurrency demonstrations
    walkthrough.py    P9 end-to-end evidence
    cli.py            operations + demonstrations
  scripts/
    _common.sh        path conversion helper
    preflight.sh      fail-closed environment gate (P7)
    smoke.sh          learner-owned end-to-end smoke
    smoke_driver.py   real HTTP assertions against a running service
    reset.sh          idempotent cleanup
  tests/              unittest suite, one file per milestone pair
```

**Standard library only.** No web framework, ORM, or external service. The
service core has no HTTP knowledge; the adapter translates.

### HTTP surface

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | liveness + schema version |
| GET | `/metrics` | JSON counters and latency summary (local only) |
| POST | `/v1/users` | create a user |
| POST | `/v1/sessions` | log in (returns a bearer token) |
| DELETE | `/v1/sessions` | log out / revoke |
| POST | `/v1/items` | create (accepts `Idempotency-Key`) |
| GET | `/v1/items` | list own items |
| GET/PATCH/DELETE | `/v1/items/{id}` | read / optimistic update / delete |
| POST/DELETE | `/v1/items/{id}/shares/{username}` | grant / revoke an explicit share |
| POST | `/v1/items/{id}/reindex` | re-run the dependency after a failure |

## 5. State inventory

| State | Where | Survives |
|---|---|---|
| transient request state | process memory | request |
| durable domain state | SQLite at `MINICLOUD_DB_PATH` | process restart, service restart |
| credential verifiers | `users` table (salted PBKDF2, never plaintext) | restarts |
| sessions | `sessions` table (only SHA-256 of the token) | restarts; revocable |
| idempotency records | `idempotency` table | restarts |
| telemetry | structured log at `MINICLOUD_LOG_PATH` | restarts; local only |
| backup | any path via `cli.py backup` | host loss of the live DB |

## 6. Security and privacy decisions

- Passwords are stored as PBKDF2-HMAC-SHA256 verifiers with per-user salts.
  Plaintext is never written anywhere.
- Session tokens are opaque and random; only their SHA-256 is persisted, so a
  database read yields no usable credential.
- **Denial does not leak existence.** Reading another user's private item
  returns the same 404 and the same message as reading an item that does not
  exist.
- Untrusted input is validated at the boundary and never concatenated into SQL.
- Logs redact secrets and never contain note bodies; the smoke asserts that the
  fixture password never reaches the log.
- **Telemetry never carries raw usernames.** `user.created` / `user.login_failed`
  log the stable pseudonymous `user_id` only; unknown-account login attempts log
  nothing (so log presence cannot enumerate accounts); share/revoke against a
  missing grantee fail with the generic `invalid grantee user` message. Account
  correlation for debugging uses `user_id`, never the username.
- Config comes from the environment; no secret is committed. The service binds
  `127.0.0.1` by default and must never be exposed publicly as-is.
- Transport is plain HTTP on loopback **by design** — this is a local teaching
  boundary. TLS and public trust are deliberately out of scope.

## 7. Observability

Structured JSON lines, one per event, at `MINICLOUD_LOG_PATH`:

```json
{"ts":"2026-09-11T23:00:00.000000Z","level":"info","event":"http.request",
 "request_id":"…","route":"POST /v1/items","method":"POST","status":201,
 "duration_ms":1.83}
```

- Every request carries a `request_id` (echoed from `X-Request-ID` when the
  caller supplies one), so a single request can be followed across HTTP →
  service → dependency.
- `GET /metrics` exposes counters plus per-route latency statistics.
- Labels are bounded to the route. `item_id` and `user_id` are **excluded**
  from metric labels to avoid unbounded cardinality; they appear in logs only.
- Telemetry failure never breaks a request: if the log sink is unusable the
  request still completes.
- A caller that disconnects mid-response is recorded as
  `http.client_disconnected` (status 499), not as a server 5xx.

## 8. Deliberately postponed

Cache. Queue. Replicas. PostgreSQL. Reverse proxy / TLS termination. Kubernetes
and service mesh. Container-first deployment. Browser UI. Full-text search.
Migrations-as-a-framework. Managed backups and compliance certification.

Each has a justification card in
[`meta/blueprint/mini-cloud-app-evolution-v0.1.md` §6](../meta/blueprint/mini-cloud-app-evolution-v0.1.md).
Adding any of them is a decision that must be defended against measured
evidence, not a default.

**Simpler alternatives kept available:** an in-memory dictionary (contrast for
P0), append-only text (representation contrast), a CLI with no HTTP (contrast
for P1), fixed user ids without authentication (contrast for P2), and "just
keep the scan" (contrast for P4).

## 9. Running the evidence

```bash
# environment gate
bash project/scripts/preflight.sh

# resolve minicloud package from repo root
export PYTHONPATH=project

# unit-level evidence (P0–P9)
python3 -m unittest discover -s project/tests -p "test_*.py"

# demonstrations
python3 -m minicloud.cli bench      # P4: plan, latency, size, write cost
python3 -m minicloud.cli race       # P5: lost update, protection, atomicity
python3 -m minicloud.cli walkthrough  # P9: the whole chain in one run

# end-to-end smoke over real processes and real HTTP
bash project/scripts/smoke.sh
```

`smoke.sh` is fail-closed: it starts the dependency and the service as separate
processes, waits for readiness, runs the assertions, **restarts the service to
prove durability**, re-checks every required `SMOKE_EVIDENCE` line (so a
skipped step cannot look green), asserts the log has correlation ids and no
password, and finally asserts both processes were reaped.

## 10. Inference limits

- Loopback only. Nothing here characterises internet latency, loss, or DNS.
- Single node, single SQLite file. No distributed or multi-region claim.
- The P3 timeout demonstration uses an **injected slow dependency**, not real
  packet loss.
- P4 numbers are host- and cache-dependent at this scale; the write-cost
  difference is noise-dominated. No universal performance threshold is asserted.
- P5 uses scripted interleavings and bounded thread counts. It is not a
  stress test and not a serializability proof across engines.
- The concurrency demonstrations deliberately show both the naive lost update
  and the protected path, because "it passed once" is not evidence.

## 11. Licensing

Original code: **Apache-2.0** (see `LICENSES/Apache-2.0.txt` and `README.md`).
Generated files under `project/var/` are scratch state and are gitignored.
