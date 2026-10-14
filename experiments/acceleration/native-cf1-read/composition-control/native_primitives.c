#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <openssl/evp.h>
#include <openssl/kdf.h>
#include <openssl/core_names.h>
#include <openssl/params.h>
#include <openssl/crypto.h>
#include <openssl/err.h>
#include <string.h>
#include <limits.h>
#include <stdint.h>

/* Research S control. GIL held; no retained references or keyed state.
 * Diagnostic selectors are absent from normal entry points/builds.
 * Failure labels describe observable stages, never inferred EVP causes. */
#define MAX_TEXT ((Py_ssize_t)16*1024*1024)
#define B(o) ((unsigned char *)PyBytes_AS_STRING(o))
#define N(o) PyBytes_GET_SIZE(o)
#ifdef S_DIAGNOSTIC
#define FAIL(site) (fault==(site))
#else
#define FAIL(site) 0
#endif
static int bounded(PyObject *o, Py_ssize_t lo, Py_ssize_t hi) {
    return PyBytes_CheckExact(o) && N(o)>=lo && N(o)<=hi;
}
static int unpack(PyObject *args, Py_ssize_t n, int diagnostic, int maxsite, int *fault) {
    *fault=0;
    if(!PyTuple_CheckExact(args)||PyTuple_GET_SIZE(args)!=n+diagnostic) {
        PyErr_SetString(PyExc_TypeError,"Invalid private arity"); return 0;
    }
    if(diagnostic) {
        PyObject *v=PyTuple_GET_ITEM(args,n);
        if(!PyLong_CheckExact(v)) {PyErr_SetString(PyExc_TypeError,"Invalid private selector");return 0;}
        long k=PyLong_AsLong(v);
        if(PyErr_Occurred()) {PyErr_Clear();PyErr_SetString(PyExc_ValueError,"Invalid private selector");return 0;}
        if(k<0||k>maxsite) {PyErr_SetString(PyExc_ValueError,"Invalid private selector");return 0;}
        *fault=(int)k;
    }
    return 1;
}
static PyObject *invalid(void) {
    PyErr_SetString(PyExc_ValueError,"Invalid bounded private input"); return NULL;
}
typedef struct {int marked, started;} Queue;
static int begin(Queue *q) {
    q->marked=ERR_peek_error()!=0; q->started=0;
    if(q->marked && ERR_set_mark()!=1) return 0;
    q->started=1; return 1;
}
static PyObject *finish(Queue *q, PyObject *r, int ok, const char *failure) {
    if(q->started) {if(q->marked) (void)ERR_pop_to_mark(); else ERR_clear_error();}
    if(ok) return r;
    if(r) {if(N(r)) OPENSSL_cleanse(B(r),(size_t)N(r));Py_DECREF(r);}
    PyErr_Clear();PyErr_SetString(PyExc_RuntimeError,failure);return NULL;
}
static PyObject *sha_impl(PyObject *args,int diagnostic) {
    int fault=0,ok=0;unsigned int size=0;Queue q={0,0};
    PyObject *r=NULL,*data;EVP_MD *md=NULL;EVP_MD_CTX *ctx=NULL;
    if(!unpack(args,1,diagnostic,6,&fault)) return NULL;
    data=PyTuple_GET_ITEM(args,0);if(!bounded(data,0,1024)) return invalid();
    if(!begin(&q)) goto done;
    if(FAIL(1)||!(md=EVP_MD_fetch(NULL,"SHA256","provider=default"))) goto done;
    if(FAIL(2)||!(ctx=EVP_MD_CTX_new())) goto done;
    if(FAIL(3)||!(r=PyBytes_FromStringAndSize(NULL,32))) goto done;
    memset(B(r),0,32);
    if(FAIL(4)||EVP_DigestInit_ex2(ctx,md,NULL)!=1) goto done;
    if(FAIL(5)||EVP_DigestUpdate(ctx,B(data),(size_t)N(data))!=1) goto done;
    if(FAIL(6)||EVP_DigestFinal_ex(ctx,B(r),&size)!=1||size!=32) goto done;
    ok=1;
done:
    EVP_MD_CTX_free(ctx);EVP_MD_free(md);return finish(&q,r,ok,"backend");
}
static PyObject *hkdf_impl(PyObject *args,int diagnostic) {
    int fault=0,ok=0;Queue q={0,0};PyObject *r=NULL,*key,*salt,*info,*length;
    EVP_KDF *kdf=NULL;EVP_KDF_CTX *ctx=NULL;
    if(!unpack(args,4,diagnostic,4,&fault)) return NULL;
    key=PyTuple_GET_ITEM(args,0);salt=PyTuple_GET_ITEM(args,1);info=PyTuple_GET_ITEM(args,2);length=PyTuple_GET_ITEM(args,3);
    if(!bounded(key,1,1024)||!bounded(salt,0,1024)||!bounded(info,0,1024)||!PyLong_CheckExact(length)) return invalid();
    long n=PyLong_AsLong(length);
    if(PyErr_Occurred()) {PyErr_Clear();return invalid();}
    if(n<1||n>64) return invalid();
    if(!begin(&q)) goto done;
    if(FAIL(1)||!(kdf=EVP_KDF_fetch(NULL,"HKDF","provider=default"))) goto done;
    if(FAIL(2)||!(ctx=EVP_KDF_CTX_new(kdf))) goto done;
    if(FAIL(3)||!(r=PyBytes_FromStringAndSize(NULL,n))) goto done;
    memset(B(r),0,(size_t)n);
    char digest[]="SHA256",props[]="provider=default",mode[]="EXTRACT_AND_EXPAND";
    OSSL_PARAM params[]={
      OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_DIGEST,digest,0),
      OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_PROPERTIES,props,0),
      OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_MODE,mode,0),
      OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_KEY,B(key),(size_t)N(key)),
      OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_SALT,B(salt),(size_t)N(salt)),
      OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_INFO,B(info),(size_t)N(info)),
      OSSL_PARAM_construct_end()};
    if(FAIL(4)||EVP_KDF_derive(ctx,B(r),(size_t)n,params)!=1) goto done;
    ok=1;
done:
    EVP_KDF_CTX_free(ctx);EVP_KDF_free(kdf);return finish(&q,r,ok,"backend");
}
static PyObject *hmac_impl(PyObject *args,int diagnostic) {
    int fault=0,ok=0;size_t size=0;Queue q={0,0};PyObject *r=NULL,*key,*message;
    EVP_MAC *mac=NULL;EVP_MAC_CTX *ctx=NULL;
    if(!unpack(args,2,diagnostic,6,&fault)) return NULL;
    key=PyTuple_GET_ITEM(args,0);message=PyTuple_GET_ITEM(args,1);
    if(!bounded(key,1,1024)||!bounded(message,0,MAX_TEXT+20)) return invalid();
    if(!begin(&q)) goto done;
    if(FAIL(1)||!(mac=EVP_MAC_fetch(NULL,"HMAC","provider=default"))) goto done;
    if(FAIL(2)||!(ctx=EVP_MAC_CTX_new(mac))) goto done;
    if(FAIL(3)||!(r=PyBytes_FromStringAndSize(NULL,32))) goto done;
    memset(B(r),0,32);
    char digest[]="SHA256",props[]="provider=default";
    OSSL_PARAM params[]={OSSL_PARAM_construct_utf8_string(OSSL_MAC_PARAM_DIGEST,digest,0),
      OSSL_PARAM_construct_utf8_string(OSSL_MAC_PARAM_PROPERTIES,props,0),OSSL_PARAM_construct_end()};
    if(FAIL(4)||EVP_MAC_init(ctx,B(key),(size_t)N(key),params)!=1) goto done;
    if(FAIL(5)||EVP_MAC_update(ctx,B(message),(size_t)N(message))!=1) goto done;
    if(FAIL(6)||EVP_MAC_final(ctx,B(r),&size,32)!=1||size!=32) goto done;
    ok=1;
done:
    EVP_MAC_CTX_free(ctx);EVP_MAC_free(mac);return finish(&q,r,ok,"backend");
}
static PyObject *decrypt_impl(PyObject *args,int diagnostic) {
    int fault=0,ok=0,produced=0,tail=0,ignored=0;size_t cap=0,n=0;Queue q={0,0};
    PyObject *r=NULL,*key,*nonce,*sealed,*aad;unsigned char *scratch=NULL;
    EVP_CIPHER *cipher=NULL;EVP_CIPHER_CTX *ctx=NULL;const char *failure="backend";
    if(!unpack(args,4,diagnostic,9,&fault)) return NULL;
    key=PyTuple_GET_ITEM(args,0);nonce=PyTuple_GET_ITEM(args,1);sealed=PyTuple_GET_ITEM(args,2);aad=PyTuple_GET_ITEM(args,3);
    if(!bounded(key,32,32)||!bounded(nonce,12,12)||!bounded(sealed,16,MAX_TEXT+16)||!bounded(aad,0,256)) return invalid();
    n=(size_t)N(sealed)-16;
    if(n>INT_MAX||n>SIZE_MAX-EVP_MAX_BLOCK_LENGTH) return invalid();
    cap=n+EVP_MAX_BLOCK_LENGTH;
    if(!begin(&q)) goto done;
    if(FAIL(1)||!(cipher=EVP_CIPHER_fetch(NULL,"AES-256-GCM-SIV","provider=default"))) goto done;
    if(EVP_CIPHER_get_key_length(cipher)!=32||EVP_CIPHER_get_iv_length(cipher)!=12) goto done;
    if(FAIL(2)||!(ctx=EVP_CIPHER_CTX_new())) goto done;
    if(FAIL(3)||EVP_DecryptInit_ex2(ctx,cipher,B(key),B(nonce),NULL)!=1) goto done;
    if(FAIL(4)||!(r=PyBytes_FromStringAndSize(NULL,(Py_ssize_t)n))) goto done;
    if(n) memset(B(r),0,n);
    if(FAIL(5)||!(scratch=OPENSSL_malloc(cap))) goto done;
    if(FAIL(6)||EVP_CIPHER_CTX_ctrl(ctx,EVP_CTRL_AEAD_SET_TAG,16,B(sealed)+n)!=1) goto done;
    if(FAIL(7)||EVP_DecryptUpdate(ctx,NULL,&ignored,B(aad),(int)N(aad))!=1) goto done;
    failure="data-processing";
    if(FAIL(8)||EVP_DecryptUpdate(ctx,scratch,&produced,B(sealed),(int)n)!=1) goto done;
    if(produced<0||(size_t)produced>n) goto done;
    if(FAIL(9)||EVP_DecryptFinal_ex(ctx,scratch+produced,&tail)!=1) goto done;
    if(tail<0||(size_t)tail>cap-(size_t)produced||(size_t)produced+(size_t)tail!=n) goto done;
    if(n) memcpy(B(r),scratch,n);
    ok=1;
done:
    EVP_CIPHER_CTX_free(ctx);EVP_CIPHER_free(cipher);OPENSSL_clear_free(scratch,cap);
    return finish(&q,r,ok,failure);
}
#define WRAP(name,impl) static PyObject *name(PyObject *self,PyObject *args) {(void)self;return impl(args,0);}
WRAP(sha256,sha_impl)
WRAP(hkdf_sha256,hkdf_impl)
WRAP(hmac_sha256,hmac_impl)
WRAP(decrypt,decrypt_impl)
#ifdef S_DIAGNOSTIC
#define FAULT_WRAP(name,impl) static PyObject *name(PyObject *self,PyObject *args) {(void)self;return impl(args,1);}
FAULT_WRAP(sha256_fault,sha_impl)
FAULT_WRAP(hkdf_sha256_fault,hkdf_impl)
FAULT_WRAP(hmac_sha256_fault,hmac_impl)
FAULT_WRAP(decrypt_fault,decrypt_impl)
#endif
static PyMethodDef methods[]={
 {"sha256",sha256,METH_VARARGS,"Private bounded fresh SHA256."},
 {"hkdf_sha256",hkdf_sha256,METH_VARARGS,"Private bounded fresh full HKDF."},
 {"hmac_sha256",hmac_sha256,METH_VARARGS,"Private bounded fresh HMAC."},
 {"decrypt",decrypt,METH_VARARGS,"Private bounded fresh authenticated decrypt."},
#ifdef S_DIAGNOSTIC
 {"sha256_fault",sha256_fault,METH_VARARGS,"Diagnostic-only refusal."},
 {"hkdf_sha256_fault",hkdf_sha256_fault,METH_VARARGS,"Diagnostic-only refusal."},
 {"hmac_sha256_fault",hmac_sha256_fault,METH_VARARGS,"Diagnostic-only refusal."},
 {"decrypt_fault",decrypt_fault,METH_VARARGS,"Diagnostic-only refusal."},
#endif
 {NULL,NULL,0,NULL}};
static struct PyModuleDef module={PyModuleDef_HEAD_INIT,"native_primitives","Research S only",-1,methods,NULL,NULL,NULL,NULL};
PyMODINIT_FUNC PyInit_native_primitives(void) {return PyModule_Create(&module);}
