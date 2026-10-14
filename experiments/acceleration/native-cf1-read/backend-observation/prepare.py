from pathlib import Path
import json,hashlib
R=Path(__file__).parent; O=R.parent/'candidate-native-cf1-read-20261014'
s=(O/'native_cf1.c').read_text()
assert hashlib.sha256(s.encode()).hexdigest()=='2926d61e43b3dc53a5fff56ab5367982c89b92b146ef9cbc47fbd2b71e5a9469'
header='''
/* Observation-only fixed buffers; no global observation state. */
typedef struct { char provider[6][64]; char name[6][64]; int seen[6];
 int key_length, iv_length, block_size, mode; unsigned long flags; } Observation;
static void record_method(Observation *o,int slot,const OSSL_PROVIDER *p,const char *name) {
 if(!o) return;
 const char *provider=p?OSSL_PROVIDER_get0_name(p):NULL;
 snprintf(o->provider[slot],64,"%s",provider?provider:"<null>");
 snprintf(o->name[slot],64,"%s",name?name:"<null>"); o->seen[slot]=1;
}
'''
s=s.replace('static int derive(',header+'static int derive(')
s=s.replace('int fault, int base) {','int fault, int base, Observation *observation) {')
s=s.replace('if(fault==base+2', 'record_method(observation,base==0?0:3,EVP_MD_get0_provider(md),EVP_MD_get0_name(md));\n    if(fault==base+2')
s=s.replace('if(fault==base+7', 'record_method(observation,base==0?1:4,EVP_KDF_get0_provider(kdf),EVP_KDF_get0_name(kdf));\n    if(fault==base+7')
s=s.replace('open_impl(PyObject *args, int diagnostic)', 'open_impl(PyObject *args, int diagnostic, Observation *observation)')
s=s.replace('key,fault,0)', 'key,fault,0,observation)').replace('skey,fault,20)', 'skey,fault,20,observation)')
s=s.replace('if(EVP_CIPHER_get_key_length(cipher)', '''record_method(observation,2,EVP_CIPHER_get0_provider(cipher),EVP_CIPHER_get0_name(cipher));
    if(observation) { observation->key_length=EVP_CIPHER_get_key_length(cipher);
      observation->iv_length=EVP_CIPHER_get_iv_length(cipher); observation->block_size=EVP_CIPHER_get_block_size(cipher);
      observation->mode=EVP_CIPHER_get_mode(cipher); observation->flags=EVP_CIPHER_get_flags(cipher); }
    if(EVP_CIPHER_get_key_length(cipher)''')
s=s.replace('if(fault==31', 'record_method(observation,5,EVP_MAC_get0_provider(mac),EVP_MAC_get0_name(mac));\n        if(fault==31')
s=s.replace('open_impl(args,0)', 'open_impl(args,0,NULL)').replace('open_impl(args,1)', 'open_impl(args,1,NULL)')
extra=r'''
/* Benign public sentinel fixture. No preexisting marks are installed. */
static PyObject *queue_seed(PyObject *self,PyObject *arg) {
 (void)self; long count=PyLong_AsLong(arg); if(PyErr_Occurred()) return NULL;
 if(count<0||count>2 || ERR_peek_error()!=0) {PyErr_SetString(PyExc_ValueError,"seed requires empty queue and count 0..2");return NULL;}
 for(int i=0;i<count;i++) {ERR_new();ERR_set_debug("public-sentinel.c",700+i,"public_sentinel");
   ERR_set_error(ERR_LIB_USER,100+i,"public-sentinel-%d",i);}
 Py_RETURN_NONE;
}
static PyObject *entry(unsigned long code,const char *file,int line,const char *func,const char *data,int flags) {
 return Py_BuildValue("(ksissi)",code,file?file:"",line,func?func:"",data?data:"",flags);
}
static PyObject *queue_peek(PyObject *self,PyObject *arg) {
 (void)self;long n=PyLong_AsLong(arg);if(PyErr_Occurred())return NULL;
 if(n<0||n>2){PyErr_SetString(PyExc_ValueError,"peek 0..2");return NULL;}
 PyObject *list=PyList_New(0); if(!list)return NULL;
 const char *file=NULL,*func=NULL,*data=NULL;int line=0,flags=0;
 unsigned long code=ERR_peek_error_all(&file,&line,&func,&data,&flags);
 if(code) {PyObject *x=entry(code,file,line,func,data,flags);if(!x||PyList_Append(list,x)<0){Py_XDECREF(x);Py_DECREF(list);return NULL;}Py_DECREF(x);}
 if(n==2) {code=ERR_peek_last_error_all(&file,&line,&func,&data,&flags);
  if(code){PyObject *x=entry(code,file,line,func,data,flags);if(!x||PyList_Append(list,x)<0){Py_XDECREF(x);Py_DECREF(list);return NULL;}Py_DECREF(x);}}
 return list;
}
static PyObject *queue_drain(PyObject *self,PyObject *args) {
 (void)self;(void)args;PyObject *list=PyList_New(0);if(!list)return NULL;
 const char *file=NULL,*func=NULL,*data=NULL;int line=0,flags=0;unsigned long code;
 while((code=ERR_get_error_all(&file,&line,&func,&data,&flags))!=0){
  PyObject *x=entry(code,file,line,func,data,flags);if(!x||PyList_Append(list,x)<0){Py_XDECREF(x);Py_DECREF(list);return NULL;}Py_DECREF(x);}
 return list;
}
static PyObject *observe(PyObject *self,PyObject *args) {
 (void)self;Observation o={0};PyObject *value=open_impl(args,1,&o),*failure=NULL;
 if(!value){failure=PyErr_GetRaisedException();if(!failure)return NULL;}
 PyObject *methods=PyList_New(0);if(!methods){Py_XDECREF(value);Py_XDECREF(failure);return NULL;}
 for(int i=0;i<6;i++)if(o.seen[i]){PyObject *x=Py_BuildValue("(iss)",i,o.name[i],o.provider[i]);
  if(!x||PyList_Append(methods,x)<0){Py_XDECREF(x);Py_DECREF(methods);Py_XDECREF(value);Py_XDECREF(failure);return NULL;}Py_DECREF(x);}
 PyObject *result=Py_BuildValue("(OOO(ii iik))",value?value:Py_None,failure?failure:Py_None,methods,o.key_length,o.iv_length,o.block_size,o.mode,o.flags);
 Py_XDECREF(value);Py_XDECREF(failure);Py_DECREF(methods);return result;
}
'''
s=s.replace('static PyMethodDef methods[]={',extra+'\nstatic PyMethodDef methods[]={\n {"observe",observe,METH_VARARGS,"Diagnostic own-call observation."},\n {"queue_seed",queue_seed,METH_O,"Install 0..2 public sentinels."},\n {"queue_peek",queue_peek,METH_O,"Inspect seeded entries without removal."},\n {"queue_drain",queue_drain,METH_NOARGS,"Read and remove entries."},')
(R/'native_cf1.c').write_text(s)
f=json.loads((O/'cases.json').read_text())['fixtures']; cases=[]
for rep in ['storage','equality']:
 spec=f['uuid-'+rep+'-unicode']; actions=['success','badtag','fault1','fault10','fault17']+(['wrongsearch','fault30'] if rep=='equality' else [])
 for action in actions:
  for count in range(3):
   cases.append(dict(id=f'{rep}-{action}-q{count}',rep=rep,action=action,sentinels=count,expected=spec['encoded_text'] if action=='success' else ('term' if action=='wrongsearch' else 'data-processing' if action in ('badtag','fault17') else 'backend')))
(R/'cases.json').write_text(json.dumps({'fixtures':{k:f[k] for k in ['uuid-storage-unicode','uuid-equality-unicode']},'cases':cases},indent=2)+'\n')
