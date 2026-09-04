#!/usr/bin/env python3
"""
Certificate generation utility for M11 TLS local fixture.

Generates:
1. Course Test Root CA (ca.pem, ca.key)
2. Course Server Leaf Certificate (server.pem, server.key) with SAN (localhost, 127.0.0.1)
3. Separate Untrusted Root CA (untrusted_ca.pem) for deterministic path-rejection tests.

Adheres strictly to RFC 5280, RFC 9846, and RFC 9525.
Validity: 10 years (3650 days) from 2026-09-04 to avoid unexpected test failure due to expiry.
"""

import datetime
import ipaddress
import os
import sys

try:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID
except ImportError:
    print("Error: cryptography library is required to generate new certificates.")
    sys.exit(1)


def generate_all_certs(output_dir=None):
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    os.makedirs(output_dir, exist_ok=True)

    now = datetime.datetime.now(datetime.timezone.utc)
    start_time = now - datetime.timedelta(days=1)
    end_time = now + datetime.timedelta(days=3650)  # 10 years

    # 1. Generate Course Test Root CA
    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    ca_name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "Essential CS Test Root CA"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Essential CS Project"),
    ])
    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(ca_name)
        .issuer_name(ca_name)
        .public_key(ca_key.public_key())
        .serial_number(1)
        .not_valid_before(start_time)
        .not_valid_after(end_time)
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=True,
                crl_sign=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key()), critical=False)
        .sign(ca_key, hashes.SHA256())
    )

    ca_key_path = os.path.join(output_dir, "ca.key")
    ca_pem_path = os.path.join(output_dir, "ca.pem")
    with open(ca_key_path, "wb") as f:
        f.write(ca_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption()))
    with open(ca_pem_path, "wb") as f:
        f.write(ca_cert.public_bytes(serialization.Encoding.PEM))

    # 2. Generate Server Leaf Certificate (SAN: localhost, 127.0.0.1)
    leaf_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    leaf_name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Essential CS Local Server"),
    ])
    leaf_cert = (
        x509.CertificateBuilder()
        .subject_name(leaf_name)
        .issuer_name(ca_name)
        .public_key(leaf_key.public_key())
        .serial_number(2)
        .not_valid_before(start_time)
        .not_valid_after(end_time)
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        )
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_encipherment=True,
                key_cert_sign=False,
                crl_sign=False,
                content_commitment=False,
                data_encipherment=False,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False)
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(leaf_key.public_key()), critical=False)
        .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()), critical=False)
        .sign(ca_key, hashes.SHA256())
    )

    server_key_path = os.path.join(output_dir, "server.key")
    server_pem_path = os.path.join(output_dir, "server.pem")
    with open(server_key_path, "wb") as f:
        f.write(leaf_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption()))
    with open(server_pem_path, "wb") as f:
        f.write(leaf_cert.public_bytes(serialization.Encoding.PEM))

    # 3. Generate Independent Untrusted CA (for Case 3 deterministic rejection)
    untrusted_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    untrusted_name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "Foreign Untrusted Authority"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Untrusted Corp"),
    ])
    untrusted_cert = (
        x509.CertificateBuilder()
        .subject_name(untrusted_name)
        .issuer_name(untrusted_name)
        .public_key(untrusted_key.public_key())
        .serial_number(999)
        .not_valid_before(start_time)
        .not_valid_after(end_time)
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=True,
                crl_sign=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(untrusted_key.public_key()), critical=False)
        .sign(untrusted_key, hashes.SHA256())
    )

    untrusted_ca_path = os.path.join(output_dir, "untrusted_ca.pem")
    with open(untrusted_ca_path, "wb") as f:
        f.write(untrusted_cert.public_bytes(serialization.Encoding.PEM))

    print(f"Generated certificates in: {output_dir}")
    print(f"  CA Certificate:       {ca_pem_path}")
    print(f"  Server Certificate:   {server_pem_path}")
    print(f"  Untrusted CA Cert:    {untrusted_ca_path}")
    print(f"  Validity Window:      {start_time.isoformat()} to {end_time.isoformat()}")


if __name__ == "__main__":
    generate_all_certs()
