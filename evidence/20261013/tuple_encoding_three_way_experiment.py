"""Pure synthetic allocation experiment; no secret material or new primitive."""
import io,json,random,statistics,struct,time,tracemalloc
from pathlib import Path

def original(*parts):
    if len(parts)>0xFFFFFFFF or any(type(p) is not bytes or len(p)>0xFFFFFFFF for p in parts):raise ValueError
    return len(parts).to_bytes(4,'big')+b''.join(len(p).to_bytes(4,'big')+p for p in parts)

def one_pass(*parts):
    if len(parts)>0xFFFFFFFF:raise ValueError
    encoded=[len(parts).to_bytes(4,'big')]
    for part in parts:
        if type(part) is not bytes:raise ValueError
        size=len(part)
        if size>0xFFFFFFFF:raise ValueError
        encoded.append(size.to_bytes(4,'big'));encoded.append(part)
    return b''.join(encoded)

def bytearray_variant(*parts):
    if len(parts)>0xFFFFFFFF:raise ValueError
    encoded=bytearray(len(parts).to_bytes(4,'big'))
    for part in parts:
        if type(part) is not bytes:raise ValueError
        size=len(part)
        if size>0xFFFFFFFF:raise ValueError
        encoded.extend(size.to_bytes(4,'big'));encoded.extend(part)
    return bytes(encoded)

def oracle(parts):
    output=io.BytesIO();output.write(struct.pack('!I',len(parts)))
    for part in parts:output.write(struct.pack('!I',len(part)));output.write(part)
    return output.getvalue()

r=random.Random(601013)
cases=[(),(b'',),(b'a',b'',b'bc')]+[tuple(r.randbytes(r.randrange(0,512)) for _ in range(r.randrange(0,12))) for _ in range(128)]
for case in cases:assert original(*case)==one_pass(*case)==bytearray_variant(*case)==oracle(case)
class BytesSubclass(bytes):pass
for value in [None,1,True,'x',bytearray(b'x'),memoryview(b'x'),BytesSubclass(b'x')]:
 for fn in [original,one_pass,bytearray_variant]:
  try:fn(value)
  except ValueError:pass
  else:raise AssertionError('Invalid input accepted')
small=(b'CF1/payload',b'a'*16,b'b'*16,b'c'*16,b'd'*16,b'e'*32,b'f'*46)
records=[]
for block in range(7):
 for name,fn in ([('original',original),('one_pass',one_pass),('bytearray',bytearray_variant)] if block%2==0 else [('bytearray',bytearray_variant),('one_pass',one_pass),('original',original)]):
  start=time.perf_counter_ns()
  for _ in range(50000):fn(*small)
  records.append(dict(block=block,variant=name,ns_per_call=(time.perf_counter_ns()-start)/50000))
large=(b'equality',b'x'*(8*1024*1024));peaks={}
for name,fn in [('original',original),('one_pass',one_pass),('bytearray',bytearray_variant)]:
 tracemalloc.start();value=fn(*large);_,peak=tracemalloc.get_traced_memory();tracemalloc.stop();assert value==oracle(large);peaks[name]=peak
report=dict(scope='Pure synthetic function experiment, not product benchmark; same encoding and checks; no caches or retained keys',oracle_cases=len(cases),invalid_type_cases=7,records=records,median_ns={name:statistics.median(x['ns_per_call'] for x in records if x['variant']==name) for name in ['original','one_pass','bytearray']},large_value_bytes=8*1024*1024,tracemalloc_peak_bytes=peaks)
Path('persistence-recovery-20261013/s10-tuple-three-way-experiment.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='records'}))
