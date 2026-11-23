#!/usr/bin/env python3
"""news-image-20261123 — graded entrypoint.

Checks the bundled front-page image (entry.png, 1024x1024, Monday
23 November 2026) and copies it byte-identical to the output directory.

Standard library only. No network, no Pillow, no third-party code.
Any failed check exits non-zero and writes nothing.
"""
import binascii
import hashlib
import os
import struct
import sys

MAX_BYTES = 1 << 20          # 1 MiB
MAX_SIDE = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def read_chunks(data):
    """Yield (type, payload, crc_ok) for every chunk after the signature."""
    offset = len(PNG_SIGNATURE)
    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError("truncated chunk header")
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        ctype = data[offset + 4:offset + 8]
        start = offset + 8
        end = start + length
        if end + 4 > len(data):
            raise ValueError("truncated chunk " + ctype.decode("latin-1"))
        payload = data[start:end]
        stored_crc = struct.unpack(">I", data[end:end + 4])[0]
        actual_crc = binascii.crc32(ctype + payload) & 0xFFFFFFFF
        yield ctype, payload, stored_crc == actual_crc
        offset = end + 4


def verify(data):
    """Return (width, height) or raise ValueError with the reason."""
    if len(data) > MAX_BYTES:
        raise ValueError("image is %d bytes, over the 1 MiB limit" % len(data))
    if len(data) < len(PNG_SIGNATURE) + 25:
        raise ValueError("file too short to be a PNG")
    if data[:8] != PNG_SIGNATURE:
        raise ValueError("missing PNG signature")
    chunks = list(read_chunks(data))
    if not chunks:
        raise ValueError("no chunks found")
    first_type, first_payload, first_ok = chunks[0]
    if first_type != b"IHDR":
        raise ValueError("first chunk is %s, expected IHDR" % first_type)
    if not first_ok:
        raise ValueError("IHDR chunk CRC mismatch")
    if len(first_payload) != 13:
        raise ValueError("IHDR payload is %d bytes, expected 13"
                         % len(first_payload))
    width, height = struct.unpack(">II", first_payload[:8])
    if width == 0 or height == 0:
        raise ValueError("zero image dimension")
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError("dimensions %dx%d exceed %dx%d"
                         % (width, height, MAX_SIDE, MAX_SIDE))
    bit_depth, colour_type, compression, filter_method, interlace = \
        first_payload[8:13]
    if bit_depth not in (1, 2, 4, 8, 16):
        raise ValueError("IHDR bit depth %d is not a PNG value" % bit_depth)
    if colour_type not in (0, 2, 3, 4, 6):
        raise ValueError("IHDR colour type %d is not a PNG value"
                         % colour_type)
    if compression != 0 or filter_method != 0:
        raise ValueError("IHDR compression/filter must both be 0")
    if interlace not in (0, 1):
        raise ValueError("IHDR interlace %d is not a PNG value" % interlace)
    if not any(c[0] == b"IDAT" for c in chunks):
        raise ValueError("no IDAT chunk found")
    if any(not c[2] for c in chunks):
        bad = [c[0].decode("latin-1") for c in chunks if not c[2]]
        raise ValueError("chunk CRC mismatch: " + ", ".join(bad))
    if chunks[-1][0] != b"IEND":
        raise ValueError("last chunk is %s, expected IEND"
                         % chunks[-1][0].decode("latin-1"))
    if len(chunks[-1][1]) != 0:
        raise ValueError("IEND chunk must be empty")
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, "entry.png")

    try:
        with open(source, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        return fail("cannot read bundled entry.png: %s" % exc)

    try:
        width, height = verify(data)
    except ValueError as exc:
        return fail("entry.png failed verification: %s" % exc)

    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        return fail("cannot create output directory: %s" % exc)

    tmp = target + ".tmp"
    try:
        with open(tmp, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, target)
    except OSError as exc:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        return fail("cannot write output: %s" % exc)

    try:
        with open(target, "rb") as handle:
            written = handle.read()
    except OSError as exc:
        return fail("cannot read back output: %s" % exc)
    if written != data:
        return fail("read-back differs from bundled entry.png")

    digest = hashlib.sha256(data).hexdigest()
    print("entry.png verified: %dx%d, %d bytes, sha256 %s"
          % (width, height, len(data), digest))
    print("wrote " + target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
