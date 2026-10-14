import json,hashlib
from pathlib import Path
R=Path(__file__).absolute().parent; O=R.parent/'candidate-native-cf1-read-20261014'; F=R.parent/'candidate-native-fault-oracles-20261014'
s=(O/'native_cf1.c').read_text()
preamble='''
/* Diagnostic accounting of this helper's owned references only; no allocator hooks.
 * GIL-held, sequential research calls. live counts persist across calls. */
#ifndef CF1_DIAGNOSTIC
#error Resource accounting requires diagnostic build
#endif
static long acq[10], rel[10], transfer[10], live[10], peak[10];
static size_t scratch_live=0, scratch_peak=0;
static void balance_begin(void) {
    for(int i=0;i<10;i++){acq[i]=rel[i]=transfer[i]=0;peak[i]=live[i];}
    scratch_peak=scratch_live;
}
static void *balance_get(void *p,int i) {
    if(p){acq[i]++;live[i]++;if(live[i]>peak[i])peak[i]=live[i];}return p;
}
static void balance_put(void *p,int i) {
    if(p){rel[i]++;live[i]--;}
}
static void balance_transfer(void *p,int i) {
    if(p){transfer[i]++;live[i]--;}
}
static void *balance_malloc(size_t n) {
    void *p=OPENSSL_malloc(n);balance_get(p,8);
    if(p){scratch_live+=n;if(scratch_live>scratch_peak)scratch_peak=scratch_live;}return p;
}
static void balance_clear_free(void *p,size_t n) {
    if(p){balance_put(p,8);scratch_live-=n;}OPENSSL_clear_free(p,n);
}
static PyObject *balance_snapshot(PyObject *self,PyObject *args) {
    (void)self;(void)args;
    PyObject *rows=PyList_New(10);if(!rows)return NULL;
    for(int i=0;i<10;i++){
        PyObject *row=Py_BuildValue("(lllll)",acq[i],rel[i],transfer[i],live[i],peak[i]);
        if(!row){Py_DECREF(rows);return NULL;}PyList_SET_ITEM(rows,i,row);
    }
    return Py_BuildValue("(NKK)",rows,(unsigned long long)scratch_live,(unsigned long long)scratch_peak);
}
'''
names=['MD','MD_CTX','KDF','KDF_CTX','CIPHER','CIPHER_CTX','MAC','MAC_CTX']
for i,n in enumerate(names):
    fn='EVP_'+n; free=fn+'_free'
    preamble+=f'static void balance_{free}({fn} *p) {{ balance_put(p,{i}); {free}(p); }}\n'
    s=s.replace(f'{free}(',f'balance_{free}(')
# Wrap acquisitions directly without replacing library definitions.
for old,new in [
('md=EVP_MD_fetch(NULL,"SHA256","provider=default")','md=balance_get(EVP_MD_fetch(NULL,"SHA256","provider=default"),0)'),
('dc=EVP_MD_CTX_new()','dc=balance_get(EVP_MD_CTX_new(),1)'),
('kdf=EVP_KDF_fetch(NULL,"HKDF","provider=default")','kdf=balance_get(EVP_KDF_fetch(NULL,"HKDF","provider=default"),2)'),
('kc=EVP_KDF_CTX_new(kdf)','kc=balance_get(EVP_KDF_CTX_new(kdf),3)'),
('cipher=EVP_CIPHER_fetch(NULL,"AES-256-GCM-SIV","provider=default")','cipher=balance_get(EVP_CIPHER_fetch(NULL,"AES-256-GCM-SIV","provider=default"),4)'),
('cc=EVP_CIPHER_CTX_new()','cc=balance_get(EVP_CIPHER_CTX_new(),5)'),
('mac=EVP_MAC_fetch(NULL,"HMAC","provider=default")','mac=balance_get(EVP_MAC_fetch(NULL,"HMAC","provider=default"),6)'),
('mc=EVP_MAC_CTX_new(mac)','mc=balance_get(EVP_MAC_CTX_new(mac),7)'),
('out=OPENSSL_malloc(capacity)','out=balance_malloc(capacity)'),
('OPENSSL_clear_free(out,capacity)','balance_clear_free(out,capacity)'),
('result=PyBytes_FromStringAndSize(NULL,(Py_ssize_t)n)','result=balance_get(PyBytes_FromStringAndSize(NULL,(Py_ssize_t)n),9)'),
('Py_XDECREF(result);','balance_put(result,9); Py_XDECREF(result);'),
('    return result;','    balance_transfer(result,9); return result;'),
('static PyObject *open_impl(PyObject *args, int diagnostic) {','static PyObject *open_impl(PyObject *args, int diagnostic) {\n    balance_begin();')]:
    if s.count(old)!=1:raise RuntimeError(old)
    s=s.replace(old,new)
s=s.replace('/* PUBLIC-FIXTURE',preamble+'\n/* PUBLIC-FIXTURE',1)
s=s.replace('static PyMethodDef methods[]={','static PyMethodDef methods[]={\n    {"balance_snapshot",balance_snapshot,METH_NOARGS,"Owned-resource diagnostic counters."},')
(R/'native_cf1.c').write_text(s)
d=json.loads((F/'cases.json').read_text())
# Independent expected counts from predeclared ordered acquisition-site inventory.
stages=[(1,0),(2,1),(6,2),(7,3),(10,4),(11,5),(13,9),(14,8),(21,0),(22,1),(26,2),(27,3),(30,6),(31,7)]
for c in d['cases']:
    equality=bool(d['fixtures'][c['fixture']]['search_generation'])
    cutoff=c['selector'] or 99
    if c['bad_tag']:cutoff=min(cutoff,18)
    counts=[0]*10
    for site,i in stages:
        if site<cutoff and (equality or site<20):counts[i]+=1
    success='value' in c['expected']; rows=[]
    for i,n in enumerate(counts):
        transferred=int(i==9 and success)
        rows.append([n,n-transferred,transferred,0,int(n>0)])
    c['balance_expected']=[rows,0,39 if counts[8] else 0] # seven-byte plaintext + EVP_MAX_BLOCK_LENGTH (32)
old=json.loads((O/'cases.json').read_text())
term=next(c for c in old['cases'] if c['id']=='valid-aead-wrong-term')
d['fixtures'][term['fixture']]=old['fixtures'][term['fixture']]
reference=next(c for c in d['cases'] if c['fixture']=='grid-100-1' and c['selector']==0 and not c['bad_tag'])
import copy
for kind in ['before','term','recovery']:
    c=copy.deepcopy(reference);c['id']='term-'+kind;c['group']='term-sequence'
    if kind=='term':
        c['fixture']=term['fixture'];c['expected']=copy.deepcopy(term['expected']);c['expected'].update(cause_suppressed=True,native_calls=1)
        c['balance_expected'][0][9]=[1,1,0,0,1]
        c['balance_expected'][2]=len((O/old['fixtures'][term['fixture']]['frame_path']).read_bytes())-74+32
    d['cases'].append(c)
d['direct_cases']=[]
for rep in [0,1]:
    for mutation in ['arity','selector','frame']:
        for phase in ['before','refusal','recovery']:
            d['direct_cases'].append({'id':f'direct-{rep}-{mutation}-{phase}','rep':rep,'mutation':mutation,'phase':phase,'expected_exception':('TypeError' if mutation=='arity' else 'ValueError') if phase=='refusal' else None})
d['resource_names']=names+['scratch','result'];d['acquisition_stages']=stages
(R/'cases.json').write_text(json.dumps(d,indent=2)+'\n')
