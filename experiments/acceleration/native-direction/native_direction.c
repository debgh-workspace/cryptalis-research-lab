#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <openssl/evp.h>
#include <openssl/crypto.h>
#include <openssl/err.h>
#include <limits.h>

/* Standalone public-fixture experiment. No product entry point or cached state. */
static PyObject *decrypt_once(PyObject *self, PyObject *args) {
    (void)self;
    PyObject *key, *nonce, *sealed, *aad, *result = NULL;
    EVP_CIPHER *cipher = NULL;
    EVP_CIPHER_CTX *ctx = NULL;
    unsigned char *out = NULL;
    Py_ssize_t clen, alen;
    int produced = 0, final_bytes = 0, ignored = 0;
    size_t capacity = 0;
    if (!PyArg_ParseTuple(args, "OOOO", &key, &nonce, &sealed, &aad)) return NULL;
    if (!PyBytes_CheckExact(key) || !PyBytes_CheckExact(nonce) ||
        !PyBytes_CheckExact(sealed) || !PyBytes_CheckExact(aad)) {
        PyErr_SetString(PyExc_TypeError, "Exact bytes required"); return NULL;
    }
    clen = PyBytes_GET_SIZE(sealed) - 16;
    alen = PyBytes_GET_SIZE(aad);
    if (PyBytes_GET_SIZE(key) != 32 || PyBytes_GET_SIZE(nonce) != 12 ||
        clen < 0 || clen > 16 * 1024 * 1024 || alen > 16 * 1024 * 1024) {
        PyErr_SetString(PyExc_ValueError, "Invalid bounded input"); return NULL;
    }
    capacity = (size_t)clen + EVP_MAX_BLOCK_LENGTH;
    out = OPENSSL_malloc(capacity);
    if (out == NULL) return PyErr_NoMemory();
    cipher = EVP_CIPHER_fetch(NULL, "AES-256-GCM-SIV", "provider=default");
    ctx = EVP_CIPHER_CTX_new();
    if (cipher == NULL || ctx == NULL) goto failed;
    if (EVP_CIPHER_get_key_length(cipher) != 32 || EVP_CIPHER_get_iv_length(cipher) != 12) goto failed;
    if (EVP_DecryptInit_ex2(ctx, cipher,
            (const unsigned char *)PyBytes_AS_STRING(key),
            (const unsigned char *)PyBytes_AS_STRING(nonce), NULL) != 1) goto failed;
    if (EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_SET_TAG, 16,
            PyBytes_AS_STRING(sealed) + clen) != 1) goto failed;
    if (alen && EVP_DecryptUpdate(ctx, NULL, &ignored,
            (const unsigned char *)PyBytes_AS_STRING(aad), (int)alen) != 1) goto failed;
    /* Exactly one data update, including empty input. Never expose intermediate output. */
    if (EVP_DecryptUpdate(ctx, out, &produced,
            (const unsigned char *)PyBytes_AS_STRING(sealed), (int)clen) != 1) goto failed;
    if (produced < 0 || produced > clen) goto failed;
    if (EVP_DecryptFinal_ex(ctx, out + produced, &final_bytes) != 1) goto failed;
    if (final_bytes < 0 || final_bytes > (int)(capacity - (size_t)produced) ||
            (Py_ssize_t)produced + final_bytes != clen) goto failed;
    result = PyBytes_FromStringAndSize((const char *)out, clen);
    goto cleanup;
failed:
    PyErr_SetString(PyExc_ValueError, "Native operation failed");
cleanup:
    EVP_CIPHER_CTX_free(ctx);
    EVP_CIPHER_free(cipher);
    OPENSSL_clear_free(out, capacity);
    ERR_clear_error();
    return result;
}
static PyObject *backend_version(PyObject *self, PyObject *args) {
    (void)self; (void)args;
    return PyUnicode_FromString(OpenSSL_version(OPENSSL_VERSION));
}
static PyMethodDef methods[] = {
    {"decrypt_once", decrypt_once, METH_VARARGS, "Bounded standalone direction-specific decrypt."},
    {"backend_version", backend_version, METH_NOARGS, "Linked backend identity."},
    {NULL, NULL, 0, NULL}
};
static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT, "native_direction", "Isolated research only", -1, methods,
    NULL, NULL, NULL, NULL
};
PyMODINIT_FUNC PyInit_native_direction(void) { return PyModule_Create(&module); }
