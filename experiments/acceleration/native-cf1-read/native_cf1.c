#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <openssl/evp.h>
#include <openssl/kdf.h>
#include <openssl/core_names.h>
#include <openssl/params.h>
#include <openssl/crypto.h>
#include <openssl/err.h>
#include <openssl/provider.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>

/* PUBLIC-FIXTURE RESEARCH ONLY. GIL held; all keyed state is call-local.
 * RuntimeError categories are private stage labels, never cause diagnoses.
 * Diagnostic selector exists only in separately compiled CF1_DIAGNOSTIC builds.
 */
#define MAX_TEXT ((size_t)16 * 1024 * 1024)
#define B(o) ((const unsigned char *)PyBytes_AS_STRING(o))
typedef struct { const unsigned char *p; size_t n; } Part;
typedef struct { PyObject *root, *domain, *tenant, *id, *generation; } Material;
static void be32(unsigned char *p, uint32_t n) {
    p[0]=(unsigned char)(n>>24); p[1]=(unsigned char)(n>>16);
    p[2]=(unsigned char)(n>>8); p[3]=(unsigned char)n;
}
static int tuple(unsigned char *out, size_t cap, const Part *parts, size_t count, size_t *used) {
    size_t n=4;
    if (count>UINT32_MAX || cap<4) return 0;
    be32(out,(uint32_t)count);
    for(size_t i=0;i<count;i++) {
        if(parts[i].n>UINT32_MAX || n>cap || cap-n<4 || parts[i].n>cap-n-4) return 0;
        be32(out+n,(uint32_t)parts[i].n); n+=4;
        memcpy(out+n,parts[i].p,parts[i].n); n+=parts[i].n;
    }
    *used=n; return 1;
}
static Part objpart(PyObject *o) { Part p={B(o),(size_t)PyBytes_GET_SIZE(o)}; return p; }
#define LIT(s) {(const unsigned char *)(s),sizeof(s)-1}
static int bytes_len(PyObject *o, Py_ssize_t n) {
    return PyBytes_CheckExact(o) && PyBytes_GET_SIZE(o)==n;
}
static int material(PyObject *o, Material *m) {
    if(!PyTuple_CheckExact(o)||PyTuple_GET_SIZE(o)!=5) return 0;
    m->root=PyTuple_GET_ITEM(o,0); m->domain=PyTuple_GET_ITEM(o,1);
    m->tenant=PyTuple_GET_ITEM(o,2); m->id=PyTuple_GET_ITEM(o,3); m->generation=PyTuple_GET_ITEM(o,4);
    return bytes_len(m->root,32)&&bytes_len(m->domain,16)&&bytes_len(m->tenant,16)&&
        bytes_len(m->id,16)&&bytes_len(m->generation,4)&&memcmp(B(m->generation),"\0\0\0\0",4)!=0;
}
static int derive(Material *m, const unsigned char *info, size_t ilen,
                  unsigned char key[32], int fault, int base) {
    unsigned char salt_tuple[128], salt[32]; size_t slen=0; unsigned int dlen=0;
    EVP_MD *md=NULL; EVP_MD_CTX *dc=NULL; EVP_KDF *kdf=NULL; EVP_KDF_CTX *kc=NULL;
    int ok=0;
    Part parts[]={LIT("CF1/root"),objpart(m->domain),objpart(m->tenant),objpart(m->id),objpart(m->generation)};
    if(!tuple(salt_tuple,sizeof(salt_tuple),parts,5,&slen)) goto done;
    if(fault==base+1 || !(md=EVP_MD_fetch(NULL,"SHA256","provider=default"))) goto done;
    if(fault==base+2 || !(dc=EVP_MD_CTX_new())) goto done;
    if(fault==base+3 || EVP_DigestInit_ex2(dc,md,NULL)!=1) goto done;
    if(fault==base+4 || EVP_DigestUpdate(dc,salt_tuple,slen)!=1) goto done;
    if(fault==base+5 || EVP_DigestFinal_ex(dc,salt,&dlen)!=1 || dlen!=32) goto done;
    if(fault==base+6 || !(kdf=EVP_KDF_fetch(NULL,"HKDF","provider=default"))) goto done;
    if(fault==base+7 || !(kc=EVP_KDF_CTX_new(kdf))) goto done;
    char digest[]="SHA256", props[]="provider=default", mode[]="EXTRACT_AND_EXPAND";
    OSSL_PARAM params[]={
        OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_DIGEST,digest,0),
        OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_PROPERTIES,props,0),
        OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_MODE,mode,0),
        OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_KEY,(void *)B(m->root),32),
        OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_SALT,salt,32),
        OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_INFO,(void *)info,ilen),
        OSSL_PARAM_construct_end()};
    if(fault==base+8 || EVP_KDF_derive(kc,key,32,params)!=1) goto done;
    ok=1;
done:
    EVP_KDF_CTX_free(kc); EVP_KDF_free(kdf); EVP_MD_CTX_free(dc); EVP_MD_free(md);
    OPENSSL_cleanse(salt,sizeof(salt)); OPENSSL_cleanse(salt_tuple,sizeof(salt_tuple));
    return ok;
}
static PyObject *open_impl(PyObject *args, int diagnostic) {
    PyObject *frame,*rep,*domain,*tenant,*field,*digest,*typed,*pm,*sm,*result=NULL;
    Material payload,search; int equality, fault=0, produced=0, final_bytes=0, ignored=0;
    size_t hlen, n=0, capacity=0, ilen=0, alen=0, maclen=0;
    unsigned char info[192], aad[256], key[32]={0}, skey[32]={0}, term[32]={0}, prefix[20];
    unsigned char *out=NULL;
    EVP_CIPHER *cipher=NULL; EVP_CIPHER_CTX *cc=NULL; EVP_MAC *mac=NULL; EVP_MAC_CTX *mc=NULL;
    const char *failure="backend";
    int marked=0, queue_started=0, success=0;
    if(!PyTuple_CheckExact(args) || PyTuple_GET_SIZE(args)!=(diagnostic?10:9)) {
        PyErr_SetString(PyExc_TypeError,"Invalid private arity"); return NULL;
    }
    frame=PyTuple_GET_ITEM(args,0); rep=PyTuple_GET_ITEM(args,1); domain=PyTuple_GET_ITEM(args,2);
    tenant=PyTuple_GET_ITEM(args,3); field=PyTuple_GET_ITEM(args,4); digest=PyTuple_GET_ITEM(args,5);
    typed=PyTuple_GET_ITEM(args,6); pm=PyTuple_GET_ITEM(args,7); sm=PyTuple_GET_ITEM(args,8);
    if(diagnostic) {
        PyObject *f=PyTuple_GET_ITEM(args,9);
        if(!PyLong_CheckExact(f)) {PyErr_SetString(PyExc_TypeError,"Invalid private selector");return NULL;}
        long v=PyLong_AsLong(f);
        if(PyErr_Occurred()) return NULL;
        if(v<0||v>35) {PyErr_SetString(PyExc_ValueError,"Invalid private selector");return NULL;}
        fault=(int)v;
    }
    if(!PyLong_CheckExact(rep)||!PyBytes_CheckExact(frame)||!bytes_len(domain,16)||!bytes_len(tenant,16)||
       !bytes_len(field,16)||!bytes_len(digest,32)||!PyBytes_CheckExact(typed)||!material(pm,&payload)) goto invalid;
    long r=PyLong_AsLong(rep);
    if(PyErr_Occurred()) return NULL;
    if(r!=0&&r!=1) goto invalid;
    equality=(int)r;
    if(equality ? !material(sm,&search) : sm!=Py_None) goto invalid;
    if(PyBytes_GET_SIZE(typed)!=16 && !(PyBytes_GET_SIZE(typed)==25 &&
       memcmp(B(typed),"\0\0\0\2\0\0\0\5int64\0\0\0\10",17)==0)) goto invalid;
    hlen=equality?46:14;
    if((size_t)PyBytes_GET_SIZE(frame)<hlen+28 || (size_t)PyBytes_GET_SIZE(frame)>MAX_TEXT+hlen+28) goto invalid;
    if(memcmp(B(frame),"CF1\0\1",5)!=0 || B(frame)[5]!=(unsigned char)equality ||
       memcmp(B(frame)+6,"\0\0\0\0",4)==0 ||
       (memcmp(B(frame)+10,"\0\0\0\0",4)!=0)!=equality) goto invalid;
    /* Material generation/context are trusted resolution outputs, not inferred
     * from active policy. No root/material cache or retained input reference. */
    n=(size_t)PyBytes_GET_SIZE(frame)-hlen-28;
    if(n>INT_MAX || n>SIZE_MAX-EVP_MAX_BLOCK_LENGTH) goto invalid;
    capacity=n+EVP_MAX_BLOCK_LENGTH;
    marked=ERR_peek_error()!=0;
    if(marked && ERR_set_mark()!=1) goto done;
    queue_started=1;
    Part pi[]={LIT("CF1/payload-key"),objpart(field),objpart(typed)};
    if(!tuple(info,sizeof(info),pi,3,&ilen)||!derive(&payload,info,ilen,key,fault,0)) goto done;
    Part aa[]={LIT("CF1/payload"),objpart(domain),objpart(tenant),objpart(field),objpart(typed),objpart(digest),{B(frame),hlen}};
    if(!tuple(aad,sizeof(aad),aa,7,&alen) || alen>INT_MAX) goto done;
    if(fault==10 || !(cipher=EVP_CIPHER_fetch(NULL,"AES-256-GCM-SIV","provider=default"))) goto done;
    if(EVP_CIPHER_get_key_length(cipher)!=32||EVP_CIPHER_get_iv_length(cipher)!=12) goto done;
    if(fault==11 || !(cc=EVP_CIPHER_CTX_new())) goto done;
    if(fault==12 || EVP_DecryptInit_ex2(cc,cipher,key,B(frame)+hlen,NULL)!=1) goto done;
    /* Reserve unexposed Python result before authentication. Unlike pyca,
     * no unused encrypt base, context copy, or reinit fallback is present. */
    if(fault==13 || !(result=PyBytes_FromStringAndSize(NULL,(Py_ssize_t)n))) goto done;
    if(n) memset(PyBytes_AS_STRING(result),0,n);
    if(fault==14 || !(out=OPENSSL_malloc(capacity))) goto done;
    if(fault==15 || EVP_CIPHER_CTX_ctrl(cc,EVP_CTRL_AEAD_SET_TAG,16,(void *)(B(frame)+hlen+12+n))!=1) goto done;
    if(fault==16 || EVP_DecryptUpdate(cc,NULL,&ignored,aad,(int)alen)!=1) goto done;
    failure="data-processing";
    if(fault==17 || EVP_DecryptUpdate(cc,out,&produced,B(frame)+hlen+12,(int)n)!=1) goto done;
    if(produced<0||(size_t)produced>n) goto done;
    if(fault==18 || EVP_DecryptFinal_ex(cc,out+produced,&final_bytes)!=1) goto done;
    if(final_bytes<0||(size_t)final_bytes>capacity-(size_t)produced||(size_t)produced+(size_t)final_bytes!=n) goto done;
    failure="backend";
    if(equality) {
        Part si[]={LIT("CF1/search-key"),objpart(field),LIT("utf8-exact/v1"),LIT("identity/v1"),LIT("equality")};
        if(!tuple(info,sizeof(info),si,5,&ilen)||!derive(&search,info,ilen,skey,fault,20)) goto done;
        if(fault==30 || !(mac=EVP_MAC_fetch(NULL,"HMAC","provider=default"))) goto done;
        if(fault==31 || !(mc=EVP_MAC_CTX_new(mac))) goto done;
        char dg[]="SHA256", props[]="provider=default";
        OSSL_PARAM mp[]={OSSL_PARAM_construct_utf8_string(OSSL_MAC_PARAM_DIGEST,dg,0),
            OSSL_PARAM_construct_utf8_string(OSSL_MAC_PARAM_PROPERTIES,props,0),OSSL_PARAM_construct_end()};
        if(fault==32 || EVP_MAC_init(mc,skey,32,mp)!=1) goto done;
        be32(prefix,2); be32(prefix+4,8); memcpy(prefix+8,"equality",8); be32(prefix+16,(uint32_t)n);
        if(fault==33 || EVP_MAC_update(mc,prefix,sizeof(prefix))!=1) goto done;
        if(fault==34 || EVP_MAC_update(mc,out,n)!=1) goto done;
        if(fault==35 || EVP_MAC_final(mc,term,&maclen,sizeof(term))!=1||maclen!=32) goto done;
#ifndef CF1_SKIP_TERM
        if(CRYPTO_memcmp(term,B(frame)+14,32)!=0) {failure="term";goto done;}
#endif
    }
    if(n) memcpy(PyBytes_AS_STRING(result),out,n);
    success=1;
done:
    EVP_MAC_CTX_free(mc); EVP_MAC_free(mac); EVP_CIPHER_CTX_free(cc); EVP_CIPHER_free(cipher);
    OPENSSL_clear_free(out,capacity); OPENSSL_cleanse(key,sizeof(key)); OPENSSL_cleanse(skey,sizeof(skey));
    OPENSSL_cleanse(term,sizeof(term)); OPENSSL_cleanse(info,sizeof(info)); OPENSSL_cleanse(aad,sizeof(aad));
    if(queue_started) { if(marked) (void)ERR_pop_to_mark(); else ERR_clear_error(); }
    if(!success) {
        if(result && n) OPENSSL_cleanse(PyBytes_AS_STRING(result),n);
        Py_XDECREF(result); PyErr_Clear(); PyErr_SetString(PyExc_RuntimeError,failure); return NULL;
    }
    return result;
invalid:
    PyErr_SetString(PyExc_ValueError,"Invalid bounded private input"); return NULL;
}
static PyObject *open_encoded(PyObject *self,PyObject *args) {(void)self;return open_impl(args,0);}
#ifdef CF1_DIAGNOSTIC
static PyObject *open_fault(PyObject *self,PyObject *args) {(void)self;return open_impl(args,1);}
#endif
static PyObject *backend_version(PyObject *self,PyObject *args) {
    (void)self;(void)args;return PyUnicode_FromString(OpenSSL_version(OPENSSL_VERSION));
}
static PyMethodDef methods[]={
    {"open_encoded",open_encoded,METH_VARARGS,"Private fresh CF1 encoded read."},
#ifdef CF1_DIAGNOSTIC
    {"open_fault",open_fault,METH_VARARGS,"Diagnostic-only site refusal."},
#endif
    {"backend_version",backend_version,METH_NOARGS,"Linked library version."},
    {NULL,NULL,0,NULL}};
static struct PyModuleDef module={PyModuleDef_HEAD_INIT,"native_cf1","Public-fixture research only",-1,methods,NULL,NULL,NULL,NULL};
PyMODINIT_FUNC PyInit_native_cf1(void) {return PyModule_Create(&module);}
