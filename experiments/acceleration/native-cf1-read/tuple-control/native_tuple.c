/* Isolated T control: no crypto, retained inputs, caches, or GIL release. */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>
#include <string.h>
#define MAX_PARTS 7
#define MAX_ENCODED ((Py_ssize_t)16777216 + 512)

static void put32(unsigned char *p, uint32_t n) {
    p[0] = (unsigned char)(n >> 24); p[1] = (unsigned char)(n >> 16);
    p[2] = (unsigned char)(n >> 8); p[3] = (unsigned char)n;
}
static PyObject *assemble(PyObject *args, int fail_alloc) {
    Py_ssize_t count = PyTuple_GET_SIZE(args), total = 4, i, n;
    PyObject *out;
    unsigned char *p;
    if (count > MAX_PARTS) {
        PyErr_SetString(PyExc_ValueError, "Invalid tuple shape"); return NULL;
    }
    /* All pointers/lengths are borrowed under the GIL. No buffer callbacks. */
    for (i = 0; i < count; ++i) {
        PyObject *part = PyTuple_GET_ITEM(args, i);
        if (!PyBytes_CheckExact(part)) {
            PyErr_SetString(PyExc_ValueError, "Invalid tuple shape"); return NULL;
        }
        n = PyBytes_GET_SIZE(part);
        /* Subtraction bounds additions and ensures every length fits uint32. */
        if (n > MAX_ENCODED - 4 || total > MAX_ENCODED - 4 - n) {
            PyErr_SetString(PyExc_ValueError, "Invalid tuple shape"); return NULL;
        }
        total += 4 + n;
    }
    if (fail_alloc) return PyErr_NoMemory();
    out = PyBytes_FromStringAndSize(NULL, total);
    if (out == NULL) return NULL;
    p = (unsigned char *)PyBytes_AS_STRING(out);
    put32(p, (uint32_t)count); p += 4;
    for (i = 0; i < count; ++i) {
        PyObject *part = PyTuple_GET_ITEM(args, i);
        n = PyBytes_GET_SIZE(part);
        put32(p, (uint32_t)n); p += 4;
        if (n) memcpy(p, PyBytes_AS_STRING(part), (size_t)n);
        p += n;
    }
    return out; /* one owned reference transfers; no fallible operation after allocation */
}
static PyObject *tuple_bytes(PyObject *self, PyObject *args) {
    (void)self; return assemble(args, 0);
}
#ifdef TUPLE_DIAGNOSTIC
/* Explicit diagnostic call, no persistent selector state. Never timed. */
static PyObject *tuple_alloc_failure(PyObject *self, PyObject *args) {
    (void)self; return assemble(args, 1);
}
#endif
static PyMethodDef methods[] = {
    {"tuple_bytes", tuple_bytes, METH_VARARGS, "Private bounded CF1 tuple assembly."},
#ifdef TUPLE_DIAGNOSTIC
    {"tuple_alloc_failure", tuple_alloc_failure, METH_VARARGS, "Diagnostic refusal before allocation."},
#endif
    {NULL, NULL, 0, NULL}
};
static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT, "native_tuple", NULL, -1, methods, NULL, NULL, NULL, NULL
};
PyMODINIT_FUNC PyInit_native_tuple(void) { return PyModule_Create(&module); }
