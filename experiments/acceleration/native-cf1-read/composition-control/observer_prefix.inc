#define PY_SSIZE_T_CLEAN
/* Diagnostic only, GIL-held counters. Counts owned acquisition/release calls,
 * not allocator internals or leak freedom. Never linked into normal builds. */
#include <Python.h>
#include <openssl/evp.h>
#include <openssl/kdf.h>
#include <openssl/err.h>
#include <openssl/crypto.h>
static long s_acquire[9],s_release[9],s_transfer;
/* Slots: MD, MD_CTX, KDF, KDF_CTX, MAC, MAC_CTX, CIPHER, CIPHER_CTX, scratch. */
/* Explicit wrappers avoid changing input/provider properties. */
static EVP_MD *s_md_fetch(OSSL_LIB_CTX *c,const char *n,const char *p) {EVP_MD *v=EVP_MD_fetch(c,n,p);if(v)s_acquire[0]++;return v;}
static void s_md_free(EVP_MD *v) {if(v)s_release[0]++;EVP_MD_free(v);}
static EVP_MD_CTX *s_md_new(void) {EVP_MD_CTX *v=EVP_MD_CTX_new();if(v)s_acquire[1]++;return v;}
static void s_md_ctx_free(EVP_MD_CTX *v) {if(v)s_release[1]++;EVP_MD_CTX_free(v);}
static EVP_KDF *s_kdf_fetch(OSSL_LIB_CTX *c,const char *n,const char *p) {EVP_KDF *v=EVP_KDF_fetch(c,n,p);if(v)s_acquire[2]++;return v;}
static void s_kdf_free(EVP_KDF *v) {if(v)s_release[2]++;EVP_KDF_free(v);}
static EVP_KDF_CTX *s_kdf_new(EVP_KDF *k) {EVP_KDF_CTX *v=EVP_KDF_CTX_new(k);if(v)s_acquire[3]++;return v;}
static void s_kdf_ctx_free(EVP_KDF_CTX *v) {if(v)s_release[3]++;EVP_KDF_CTX_free(v);}
static EVP_MAC *s_mac_fetch(OSSL_LIB_CTX *c,const char *n,const char *p) {EVP_MAC *v=EVP_MAC_fetch(c,n,p);if(v)s_acquire[4]++;return v;}
static void s_mac_free(EVP_MAC *v) {if(v)s_release[4]++;EVP_MAC_free(v);}
static EVP_MAC_CTX *s_mac_new(EVP_MAC *m) {EVP_MAC_CTX *v=EVP_MAC_CTX_new(m);if(v)s_acquire[5]++;return v;}
static void s_mac_ctx_free(EVP_MAC_CTX *v) {if(v)s_release[5]++;EVP_MAC_CTX_free(v);}
static EVP_CIPHER *s_cipher_fetch(OSSL_LIB_CTX *c,const char *n,const char *p) {EVP_CIPHER *v=EVP_CIPHER_fetch(c,n,p);if(v)s_acquire[6]++;return v;}
static void s_cipher_free(EVP_CIPHER *v) {if(v)s_release[6]++;EVP_CIPHER_free(v);}
static EVP_CIPHER_CTX *s_cipher_new(void) {EVP_CIPHER_CTX *v=EVP_CIPHER_CTX_new();if(v)s_acquire[7]++;return v;}
static void s_cipher_ctx_free(EVP_CIPHER_CTX *v) {if(v)s_release[7]++;EVP_CIPHER_CTX_free(v);}
static void *s_malloc(size_t n) {void *v=OPENSSL_malloc(n);if(v)s_acquire[8]++;return v;}
static void s_clear_free(void *p,size_t n) {if(p)s_release[8]++;OPENSSL_clear_free(p,n);}
static long s_reserved,s_decref;
static PyObject *s_bytes(const char *p,Py_ssize_t n) {PyObject *v=PyBytes_FromStringAndSize(p,n);if(v)s_reserved++;return v;}
static PyObject *s_reset(PyObject *self,PyObject *args) {
 (void)self;(void)args;for(int i=0;i<9;i++)s_acquire[i]=s_release[i]=0;
 s_reserved=s_decref=s_transfer=0;Py_RETURN_NONE;
}
static PyObject *s_snapshot(PyObject *self,PyObject *args) {
 (void)self;(void)args;PyObject *a=PyList_New(9),*r=PyList_New(9),*out=NULL;
 if(!a||!r) {Py_XDECREF(a);Py_XDECREF(r);return NULL;}
 for(int i=0;i<9;i++) {
  PyObject *x=PyLong_FromLong(s_acquire[i]),*y=PyLong_FromLong(s_release[i]);
  if(!x||!y) {Py_XDECREF(x);Py_XDECREF(y);Py_DECREF(a);Py_DECREF(r);return NULL;}
  PyList_SET_ITEM(a,i,x);PyList_SET_ITEM(r,i,y);
 }
 out=Py_BuildValue("{s:O,s:O,s:l,s:l,s:l}","acquire",a,"release",r,"reserved",s_reserved,"decref",s_decref,"transfer",s_transfer);
 Py_DECREF(a);Py_DECREF(r);return out;
}
/* Only harness-owned ordinary unmarked sentinel queues; no marked/overflow claim.
 * Seed refuses a preexisting queue instead of clearing unrelated errors. */
static PyObject *s_queue_seed(PyObject *self,PyObject *args) {
 (void)self;int count;
 if(!PyArg_ParseTuple(args,"i",&count))return NULL;
 if(count<0||count>2||ERR_peek_error()!=0) {PyErr_SetString(PyExc_RuntimeError,"Queue precondition");return NULL;}
 for(int i=0;i<count;i++)ERR_raise(ERR_LIB_USER,101+i);
 Py_RETURN_NONE;
}
static PyObject *s_queue_take(PyObject *self,PyObject *args) {
 (void)self;(void)args;PyObject *r=PyList_New(0);unsigned long code;
 if(!r)return NULL;
 while((code=ERR_get_error())!=0) {
  PyObject *v=PyLong_FromUnsignedLong(code);
  if(!v||PyList_Append(r,v)<0){Py_XDECREF(v);Py_DECREF(r);return NULL;}Py_DECREF(v);
 }
 return r;
}
#define EVP_MD_fetch s_md_fetch
#define EVP_MD_free s_md_free
#define EVP_MD_CTX_new s_md_new
#define EVP_MD_CTX_free s_md_ctx_free
#define EVP_KDF_fetch s_kdf_fetch
#define EVP_KDF_free s_kdf_free
#define EVP_KDF_CTX_new s_kdf_new
#define EVP_KDF_CTX_free s_kdf_ctx_free
#define EVP_MAC_fetch s_mac_fetch
#define EVP_MAC_free s_mac_free
#define EVP_MAC_CTX_new s_mac_new
#define EVP_MAC_CTX_free s_mac_ctx_free
#define EVP_CIPHER_fetch s_cipher_fetch
#define EVP_CIPHER_free s_cipher_free
#define EVP_CIPHER_CTX_new s_cipher_new
#define EVP_CIPHER_CTX_free s_cipher_ctx_free
#undef OPENSSL_malloc
#define OPENSSL_malloc s_malloc
#undef OPENSSL_clear_free
#define OPENSSL_clear_free s_clear_free
#define PyBytes_FromStringAndSize s_bytes
