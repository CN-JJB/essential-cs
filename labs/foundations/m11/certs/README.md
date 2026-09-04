# M11 Course Test PKI

These keys and certificates are intentionally committed **public test fixtures** for the localhost-only M11 TLS activity.

- They are **not secrets**.
- They must **never** be reused for a real service, production environment, private network, or credential-bearing system.
- Learner Core execution uses the committed files with Python's standard-library `ssl`; it does not require the external `openssl` CLI or the `cryptography` package.
- `generate_certs.py` is a **maintenance/regeneration utility**. It requires the optional `cryptography` package and regenerates a new local-only CA/leaf fixture.
- The leaf SAN covers the course reference identities `DNS:localhost` and `IP:127.0.0.1`.
- Certificate validity is a fixture-maintenance concern. If the committed fixture expires or is regenerated, record the new validity window in release/verification evidence instead of treating expiry as learner failure.
- The 10-year local fixture lifetime is **not** a Web PKI or production certificate-lifetime recommendation.

Do not import the course CA into a system-wide trust store. The activity uses a dedicated trust context only.
