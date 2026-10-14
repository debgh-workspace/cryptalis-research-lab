"""Additive sanitizer-only freeze/cache/import guard. No historical guard edits."""
import hashlib,importlib.machinery,json,sys,sysconfig
from pathlib import Path
R=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(path,value):
    with Path(path).open('x') as f:
        count=0
        for chunk in json.JSONEncoder(indent=2,ensure_ascii=False).iterencode(value):
            count+=len(chunk.encode('utf8'))
            if count>134217728:raise RuntimeError('Receipt exceeds 128 MiB cap')
            f.write(chunk)
        f.write('\n')
def exact(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(exact(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b

def check(anchor=None):
    path=R/'EXECUTION_FREEZE_v3.json';raw=path.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    if anchor is not None and digest!=anchor:raise RuntimeError('Sanitizer freeze anchor changed')
    f=json.loads(raw)
    for p,h in f['pins'].items():
        if sha(p)!=h:raise RuntimeError('Sanitizer pin mismatch: '+p)
    for root,expected in f['cache_inventories'].items():
        actual=sorted(str(p) for p in Path(root).rglob('*.pyc'))
        if actual!=expected:raise RuntimeError('Shared cache inventory changed: '+root)
    for p,h in f['preserved_v2_artifacts'].items():
        if sha(p)!=h:raise RuntimeError('Preserved v2 artifact changed: '+p)
    f['_anchor']=digest;return f

def cache(expected):
    root=Path(expected)
    if root.parent!=R or root.is_symlink() or not root.is_dir() or not root.name.startswith('v3-cache-'):raise RuntimeError('Private cache path invalid')
    if sys.pycache_prefix!=str(root) or not sys.flags.dont_write_bytecode or not sys.flags.no_site or not sys.flags.ignore_environment:raise RuntimeError('Required startup cache flags missing')
    if list(root.iterdir()):raise RuntimeError('Private cache not empty')
    return []

class SourceFinder:
    @classmethod
    def find_spec(cls,fullname,path=None,target=None):
        spec=importlib.machinery.PathFinder.find_spec(fullname,path,target)
        if spec is not None and (isinstance(spec.loader,importlib.machinery.SourcelessFileLoader) or str(spec.origin).endswith('.pyc')):raise ImportError('Sourceless imports prohibited')
        return spec

def install():
    if importlib.machinery.PathFinder not in sys.meta_path:raise RuntimeError('PathFinder missing')
    sys.meta_path[sys.meta_path.index(importlib.machinery.PathFinder)]=SourceFinder

def interpreter(f,opt=None):
    if sys.executable!=f['python'] or list(sys.version_info[:3])!=[3,12,14] or sysconfig.get_config_var('SOABI')!='cpython-312-x86_64-linux-gnu' or sys.flags.optimize not in ([opt] if opt is not None else [0,1]):raise RuntimeError('Sanitizer interpreter mismatch')

def loaded_origins(f,binary=None):
    allowed=set(f['pins']);allowed.add(str(Path(binary))) if binary else None
    seen={}
    for name,module in list(sys.modules.items()):
        p=getattr(module,'__file__',None)
        if p is None:continue
        path=str(Path(p).absolute())
        if path.endswith('.pyc') or path not in allowed:raise RuntimeError('Unpinned loaded module: '+name+' '+path)
        seen[name]=path
    return seen

def mapped(f,binary=None,require_sanitizers=False):
    result={}
    for line in Path('/proc/self/maps').read_text().splitlines():
        cols=line.split()
        if len(cols)<6 or not cols[-1].startswith('/'):continue
        p=str(Path(cols[-1]).resolve())
        if binary is not None and p==str(Path(binary).resolve()):continue
        if '.so' not in p and 'ld-linux' not in p:continue
        if p not in f['resolved_pins'] or sha(p)!=f['resolved_pins'][p]:raise RuntimeError('Unpinned mapped library: '+p)
        result[p]=f['resolved_pins'][p]
    if require_sanitizers:
        for name in ('libasan.so','libubsan.so'):
            if not any(name in p for p in result):raise RuntimeError('Sanitizer runtime not mapped: '+name)
    return result
