import copy,ctypes,json,os,select,signal,time
from pathlib import Path
import native_cf1,native_read as nr,fixture_support as s,validate
from cryptalis.crypto import keys,cf1
R=Path(__file__).resolve().parent
manifest=json.loads((R/'cases.json').read_text()); observations=[]

def same(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b

def abi(c):
 selected=next(x for x in validate.manifest['cases'] if x['id']=='grid/grid-100-1')
 valid=validate.native_args(selected);a=list(valid);op=c['op'];p=c.get('pos');v=c.get('variant')
 def wrong(x):return (None,bytearray(x),s.BytesSubclass(x))[v]
 if op=='type':a[p]=wrong(a[p])
 elif op=='length':a[p]=bytes(len(a[p])+c['delta'])
 elif op.startswith('material-'):
  b=c['bundle'];bundle=list(a[b]);bundle[p]=wrong(bundle[p]) if op=='material-type' else bytes(len(bundle[p])+c['delta']);a[b]=tuple(bundle)
 elif op=='bundle':
  b=c['bundle'];a[b]={'missing':a[b][:-1],'extra':a[b]+(b'',),'none':None,'list':list(a[b])}[v]
 elif op=='arity':a=a[:-1] if v=='short' else a+[None]
 elif op=='record':a[6]=bytes(c['length'])
 elif op=='representation':a[1]=(None,True,-1,2,2**100)[v]
 elif op=='frame':a[0]=b'' if v=='empty' else bytes(cf1.MAX_TEXT_BYTES+75)
 elif op=='storage-extra-search':
  storage=next(x for x in validate.manifest['cases'] if x['id']=='grid/grid-000-1');a=list(validate.native_args(storage));a[-1]=valid[-1]
 else:raise RuntimeError('Unknown frozen operation')
 try:native_cf1.open_encoded(*a)
 except (ValueError,TypeError,OverflowError) as exc:
  return {'exception':type(exc).__name__,'args':list(exc.args),'cause_none':exc.__cause__ is None}
 raise RuntimeError('ABI unexpectedly returned')

def observe(args):
 calls=0;original=nr._native_encoded
 def counted(*a):
  nonlocal calls
  calls+=1;return original(*a)
 nr._native_encoded=counted;args[-1].trace.clear()
 try:
  try:value=nr.open_text_native(*args)
  except keys.CryptoFailure as exc:
   result={name:getattr(exc,name) for name in ('code','stage','retryable','effects','remedy')}
   result.update(exception=type(exc).__name__,operation_present=type(exc.operation_id) is str and bool(exc.operation_id),args_safe=exc.args==(f'{exc.code} during {exc.stage}. {exc.remedy} Operation {exc.operation_id}.',),cause_none=exc.__cause__ is None)
  else:result={'value':value,'value_type':type(value).__name__}
  result.update(trace=copy.deepcopy(args[-1].trace),native_calls=calls);return result
 finally:nr._native_encoded=original

def child_guard(parent):
 libc=ctypes.CDLL(None,use_errno=True)
 if libc.prctl(1,signal.SIGKILL,0,0,0)!=0:raise RuntimeError('Child death guard unavailable')
 if os.getppid()!=parent:os._exit(125)

# Deadline covers pipe reading AND process exit. A written result cannot evade it.
def supervised(c):
 inherited=s.invocation(c['fixture_case'],validate.fixtures) if c['kind']=='fork' else None
 r,w=os.pipe();parent=os.getpid();pid=None;reaped=False;buf=bytearray();category=None;status=None
 try:
  pid=os.fork()
  if pid==0:
   os.close(r)
   try:
    child_guard(parent)
    if c['kind']=='fork':
     out={'inherited':observe(inherited),'fresh':observe(s.invocation(c['fixture_case'],validate.fixtures)),'child_exit':0};data=json.dumps(out).encode()
    else:
     v=c['variant']
     if v=='silent':time.sleep(30)
     data=b'{}' if v=='write-hang' else b'x'*8193 if v=='oversize' else b'!'
    # Small bounded protocol; explicit complete-write loop.
    while data:
     n=os.write(w,data);data=data[n:]
    if c.get('variant')=='write-hang':time.sleep(30)
    os.close(w);os._exit(0)
   except BaseException:
    os._exit(126) # infrastructure failures cannot become accepted crypto refusals
  os.close(w);w=None;os.set_blocking(r,False)
  deadline=time.monotonic()+(1 if c['kind']=='containment' else 10);eof=False
  while True:
   if not reaped:
    got,st=os.waitpid(pid,os.WNOHANG)
    if got:reaped=True;status=st
   if reaped and eof:break
   remain=deadline-time.monotonic()
   if remain<=0:category='timeout';break
   ready,_,_=select.select([] if eof else [r],[],[],min(remain,0.05))
   if ready:
    chunk=os.read(r,8193)
    if not chunk:eof=True
    else:buf.extend(chunk)
    if len(buf)>8192:category='protocol';break
   if reaped and not eof:continue
  if category is None:
   if status!=0:raise RuntimeError('Fork child failed with wait status '+str(status))
   try:out=json.loads(buf)
   except (json.JSONDecodeError,UnicodeDecodeError):category='protocol'
   else:
    if c['kind']=='fork':return out
    raise RuntimeError('Containment control unexpectedly completed')
 finally:
  if pid and not reaped:
   try:os.kill(pid,signal.SIGKILL)
   except ProcessLookupError:pass
   os.waitpid(pid,0);reaped=True
  os.close(r)
  if w is not None:os.close(w)
 if c['kind']=='fork':raise RuntimeError('Fork supervision failure: '+str(category))
 return {'category':category,'reaped':reaped,'fds_closed':True}

def run(negative=None):
 for c in manifest['cases']:
  actual=abi(c) if c['kind']=='abi' else supervised(c)
  if not same(actual,c['expected']):
   observations.append({'id':c['id'],'unexpected':actual});raise RuntimeError('Frozen supplement mismatch')
  if negative and c['id']==('abi/type/0/0' if negative=='abi' else 'fork/000'):
   altered=copy.deepcopy(actual)
   if negative=='abi':altered['exception']='TypeError'
   else:altered['inherited']['trace']=[]
   observations.append({'id':c['id'],'verified_original':actual,'mutated':altered})
   if not same(altered,c['expected']):raise RuntimeError('Negative oracle mismatch')
   raise RuntimeError('Negative control escaped')
  observations.append({'id':c['id'],'actual':actual})
 if [o['id'] for o in observations]!=[c['id'] for c in manifest['cases']]:raise RuntimeError('ID inventory mismatch')
