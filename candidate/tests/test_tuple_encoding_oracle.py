"""Independent wire-byte oracle; optimization never alters CF1 composition."""
import io
import random
import struct
import pytest
from cryptalis.crypto.keys import InvalidContext, tuple_bytes


def oracle(parts):
    output=io.BytesIO()
    output.write(struct.pack('!I',len(parts)))
    for part in parts:
        output.write(struct.pack('!I',len(part)))
        output.write(part)
    return output.getvalue()


def test_tuple_wire_bytes_match_independent_writer():
    rng=random.Random(601013)
    cases=[(),(b'',),(b'a',b'',b'bc')]
    cases += [tuple(rng.randbytes(rng.randrange(0,512)) for _ in range(rng.randrange(0,12))) for _ in range(128)]
    cases.append((b'equality',b'x'*(8*1024*1024)))
    for parts in cases: assert tuple_bytes(*parts)==oracle(parts)
    assert tuple_bytes(b'ab',b'c') != tuple_bytes(b'a',b'bc')
    assert tuple_bytes() != tuple_bytes(b'')


def test_tuple_never_implicitly_converts_parts():
    class BytesSubclass(bytes):pass
    for value in [None,1,True,'x',bytearray(b'x'),memoryview(b'x'),BytesSubclass(b'x')]:
        with pytest.raises(InvalidContext): tuple_bytes(b'valid-prefix',value)
