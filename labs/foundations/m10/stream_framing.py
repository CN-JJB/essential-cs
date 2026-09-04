#!/usr/bin/env python3
"""
M10 Lesson 2 Activity: TCP Byte-Stream Framing & UDP Datagram Boundaries.

Demonstrates:
1. TCP ordered reliable byte-stream abstraction (RFC 9293).
2. Why TCP does NOT preserve application send() boundaries (stream coalescing/partitioning).
3. Robust receiver loop reconstructing framed messages across arbitrary recv() partitions.
4. Host empirical recording of actual recv() chunk partitions (no hardcoded partition assertions).
5. Contrast with UDP (RFC 768 / RFC 8200) datagram boundary preservation and checksum rules.
"""

import argparse
import json
import socket
import struct
import sys
import threading
import time


def run_tcp_stream_reconstruction(messages=None, buffer_size=16):
    """
    Demonstrates that TCP transmits a continuous byte stream without message boundaries.
    Uses length-prefixed application framing (!H = 2-byte unsigned short length)
    and loops recv() until complete application messages are reconstructed.
    """
    if messages is None:
        messages = [
            b"PACKET_HEADER_DATA",
            b"METRIC_SAMPLE_12345",
            b"SHORT",
            b"A_SOMEWHAT_LONGER_APPLICATION_PAYLOAD_BLOCK_FOR_TESTING",
            b"FINAL_RECORD_END",
        ]

    # Server setup on loopback port 0
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.settimeout(3.0)
    server_sock.bind(("127.0.0.1", 0))
    server_sock.listen(1)
    bound_host, bound_port = server_sock.getsockname()

    record = {
        "messages_sent_count": len(messages),
        "total_logical_bytes_sent": sum(len(m) for m in messages),
        "actual_recv_partitions": [],
        "reconstructed_messages": [],
        "reconstruction_matches": False,
        "error": None,
    }

    server_error = []

    def server_reader():
        conn = None
        try:
            conn, _ = server_sock.accept()
            conn.settimeout(3.0)
            stream_accumulator = bytearray()
            received_messages = []

            # Framing loop: accumulate stream bytes until complete messages are parsed
            while len(received_messages) < len(messages):
                chunk = conn.recv(buffer_size)
                if not chunk:
                    break
                record["actual_recv_partitions"].append(len(chunk))
                stream_accumulator.extend(chunk)

                # Parse length-prefixed frames: [2 bytes length][payload]
                while len(stream_accumulator) >= 2:
                    (frame_len,) = struct.unpack("!H", stream_accumulator[:2])
                    total_frame_size = 2 + frame_len
                    if len(stream_accumulator) >= total_frame_size:
                        msg_payload = bytes(stream_accumulator[2:total_frame_size])
                        received_messages.append(msg_payload)
                        # Drain parsed frame from stream
                        del stream_accumulator[:total_frame_size]
                    else:
                        # Incomplete frame; need more bytes from stream
                        break

            record["reconstructed_messages"] = [
                m.decode("ascii", errors="replace") for m in received_messages
            ]
            if received_messages == messages:
                record["reconstruction_matches"] = True
            else:
                record["error"] = "Reconstructed messages do not match original sequence."
        except Exception as exc:
            server_error.append(exc)
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass

    srv_thread = threading.Thread(target=server_reader, daemon=True)
    srv_thread.start()

    # Client connects and sends length-prefixed frames
    client_sock = None
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.settimeout(3.0)
        client_sock.connect(("127.0.0.1", bound_port))

        for msg in messages:
            framed_bytes = struct.pack("!H", len(msg)) + msg
            client_sock.sendall(framed_bytes)
            # Brief pause to induce varying segment arrival
            time.sleep(0.005)

        srv_thread.join(timeout=3.0)
    except Exception as exc:
        record["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        if client_sock:
            try:
                client_sock.close()
            except Exception:
                pass
        try:
            server_sock.close()
        except Exception:
            pass

    if server_error and not record["error"]:
        record["error"] = f"Server error: {server_error[0]}"

    return record


def run_udp_datagram_contrast(datagrams=None):
    """
    Demonstrates UDP datagram boundary preservation.
    Each sendto() produces exactly one datagram read by recvfrom().
    """
    if datagrams is None:
        datagrams = [
            b"UDP_RECORD_ALPHA",
            b"UDP_RECORD_BRAVO",
            b"UDP_RECORD_CHARLIE",
        ]

    # Receiver binds to port 0
    rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rx_sock.settimeout(3.0)
    rx_sock.bind(("127.0.0.1", 0))
    rx_host, rx_port = rx_sock.getsockname()

    record = {
        "datagrams_sent_count": len(datagrams),
        "datagrams_received_count": 0,
        "datagrams_received": [],
        "boundaries_preserved": False,
        "error": None,
    }

    rx_error = []

    def rx_worker():
        try:
            received = []
            for _ in range(len(datagrams)):
                data, _ = rx_sock.recvfrom(2048)
                received.append(data)
            record["datagrams_received_count"] = len(received)
            record["datagrams_received"] = [d.decode("ascii", errors="replace") for d in received]
            if received == datagrams:
                record["boundaries_preserved"] = True
            else:
                record["error"] = "Received datagram contents do not match sent datagrams."
        except Exception as exc:
            rx_error.append(exc)

    rx_thread = threading.Thread(target=rx_worker, daemon=True)
    rx_thread.start()

    # Sender transmits datagrams
    tx_sock = None
    try:
        tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tx_sock.settimeout(3.0)

        for d in datagrams:
            tx_sock.sendto(d, (rx_host, rx_port))
            time.sleep(0.005)

        rx_thread.join(timeout=3.0)
    except Exception as exc:
        record["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        if tx_sock:
            try:
                tx_sock.close()
            except Exception:
                pass
        try:
            rx_sock.close()
        except Exception:
            pass

    if rx_error and not record["error"]:
        record["error"] = f"Receiver error: {rx_error[0]}"

    return record


def main():
    parser = argparse.ArgumentParser(description="M10 Stream Framing & UDP Contrast")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    tcp_res = run_tcp_stream_reconstruction()
    udp_res = run_udp_datagram_contrast()

    combined = {
        "tcp_stream_reconstruction": tcp_res,
        "udp_datagram_contrast": udp_res,
        "checksum_and_ack_rules": {
            "tcp_ack_boundary": "A TCP ACK confirms sequence-space delivery to the kernel receive buffer only; it does NOT prove application processing or durability.",
            "ipv4_udp_checksum": "Optional (RFC 768 / RFC 791). A checksum field of 0 indicates no checksum was computed.",
            "ipv6_udp_checksum": "Mandatory (RFC 8200). A checksum of zero is disallowed for standard traffic; must be validated.",
        },
    }

    if args.json:
        print(json.dumps(combined, indent=2))
        return 0 if (tcp_res["reconstruction_matches"] and udp_res["boundaries_preserved"]) else 1

    print("=" * 60)
    print(" M10-02 TCP Byte Stream vs UDP Datagram Boundaries")
    print("=" * 60)
    print(" [TCP Stream Reconstruction]")
    print(f"   Messages Sent:            {tcp_res['messages_sent_count']}")
    print(f"   Total Bytes:              {tcp_res['total_logical_bytes_sent']}")
    print(f"   Actual recv() Partitions: {tcp_res['actual_recv_partitions']}")
    print(f"   Reconstructed Messages:   {tcp_res['reconstructed_messages']}")
    print(f"   Exact Match Verified:     {'YES' if tcp_res['reconstruction_matches'] else 'NO'}")
    if tcp_res["error"]:
        print(f"   Error:                    {tcp_res['error']}")
    print("-" * 60)
    print(" [UDP Datagram Boundary Preservation]")
    print(f"   Datagrams Sent:           {udp_res['datagrams_sent_count']}")
    print(f"   Datagrams Received:       {udp_res['datagrams_received_count']}")
    print(f"   Datagrams Preserved:      {'YES' if udp_res['boundaries_preserved'] else 'NO'}")
    if udp_res["error"]:
        print(f"   Error:                    {udp_res['error']}")
    print("-" * 60)
    print(" [Normative Boundaries]")
    print("   TCP ACK Invariant:       Delivery to OS buffer != application commit")
    print("   IPv4 UDP Checksum:       Optional (RFC 768)")
    print("   IPv6 UDP Checksum:       Mandatory (RFC 8200)")
    print("=" * 60)

    return 0 if (tcp_res["reconstruction_matches"] and udp_res["boundaries_preserved"]) else 1


if __name__ == "__main__":
    sys.exit(main())
