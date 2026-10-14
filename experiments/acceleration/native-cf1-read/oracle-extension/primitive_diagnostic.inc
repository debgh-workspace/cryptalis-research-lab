/* Separate public-fixture oracle entry. Supported EVP APIs only; bounded inputs. */
static PyObject *primitive(PyObject *self, PyObject *args) {
    (void)self;
    PyObject *kind,*a,*b,*c,*d,*ret=NULL;
    EVP_CIPHER *ci=NULL; EVP_CIPHER_CTX *cc=NULL;
    EVP_KDF *kd=NULL; EVP_KDF_CTX *kc=NULL;
    EVP_MAC *ma=NULL; EVP_MAC_CTX *mc=NULL;
    unsigned char out[8192]={0}; size_t len=0; int n=0,last=0,ignored=0,ok=0;
    int marked=0,started=0;
    if(!PyArg_UnpackTuple(args,"primitive",5,5,&kind,&a,&b,&c,&d)) return NULL;
    if(!PyUnicode_CheckExact(kind)||!PyBytes_CheckExact(a)||!PyBytes_CheckExact(b)||
       !PyBytes_CheckExact(c)||!PyBytes_CheckExact(d)) goto invalid_primitive;
    if(PyBytes_GET_SIZE(a)>4096||PyBytes_GET_SIZE(b)>4096||PyBytes_GET_SIZE(c)>4096||PyBytes_GET_SIZE(d)>4096)
        goto invalid_primitive;
    const char *op=PyUnicode_AsUTF8(kind); if(!op) return NULL;
    marked=ERR_peek_error()!=0;
    if(marked && ERR_set_mark()!=1) goto done_primitive;
    started=1;
    if(strcmp(op,"hkdf")==0) {
        if(PyBytes_GET_SIZE(d)!=1||B(d)[0]!=42) goto invalid_after;
        kd=EVP_KDF_fetch(NULL,"HKDF","provider=default"); if(!kd) goto done_primitive;
        kc=EVP_KDF_CTX_new(kd); if(!kc) goto done_primitive;
        char dg[]="SHA256",pr[]="provider=default",mode[]="EXTRACT_AND_EXPAND";
        OSSL_PARAM p[]={OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_DIGEST,dg,0),
          OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_PROPERTIES,pr,0),
          OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_MODE,mode,0),
          OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_KEY,(void *)B(a),(size_t)PyBytes_GET_SIZE(a)),
          OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_SALT,(void *)B(b),(size_t)PyBytes_GET_SIZE(b)),
          OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_INFO,(void *)B(c),(size_t)PyBytes_GET_SIZE(c)),
          OSSL_PARAM_construct_end()};
        len=42; if(EVP_KDF_derive(kc,out,len,p)!=1) goto done_primitive;
    } else if(strcmp(op,"hmac")==0) {
        if(PyBytes_GET_SIZE(c)||PyBytes_GET_SIZE(d)) goto invalid_after;
        ma=EVP_MAC_fetch(NULL,"HMAC","provider=default"); if(!ma) goto done_primitive;
        mc=EVP_MAC_CTX_new(ma); if(!mc) goto done_primitive;
        char dg[]="SHA256",pr[]="provider=default";
        OSSL_PARAM p[]={OSSL_PARAM_construct_utf8_string(OSSL_MAC_PARAM_DIGEST,dg,0),
          OSSL_PARAM_construct_utf8_string(OSSL_MAC_PARAM_PROPERTIES,pr,0),OSSL_PARAM_construct_end()};
        if(EVP_MAC_init(mc,B(a),(size_t)PyBytes_GET_SIZE(a),p)!=1 ||
           EVP_MAC_update(mc,B(b),(size_t)PyBytes_GET_SIZE(b))!=1 ||
           EVP_MAC_final(mc,out,&len,sizeof(out))!=1 || len!=32) goto done_primitive;
    } else if(strcmp(op,"seal")==0||strcmp(op,"open")==0) {
        int enc=strcmp(op,"seal")==0;
        if(!bytes_len(a,32)||!bytes_len(b,12)||(!enc&&PyBytes_GET_SIZE(d)<16)) goto invalid_after;
        size_t input=(size_t)PyBytes_GET_SIZE(d)-(enc?0:16);
        ci=EVP_CIPHER_fetch(NULL,"AES-256-GCM-SIV","provider=default"); if(!ci) goto done_primitive;
        if(EVP_CIPHER_get_key_length(ci)!=32||EVP_CIPHER_get_iv_length(ci)!=12) goto done_primitive;
        cc=EVP_CIPHER_CTX_new(); if(!cc) goto done_primitive;
        if(EVP_CipherInit_ex2(cc,ci,B(a),B(b),enc,NULL)!=1) goto done_primitive;
        if(!enc && EVP_CIPHER_CTX_ctrl(cc,EVP_CTRL_AEAD_SET_TAG,16,(void *)(B(d)+input))!=1) goto done_primitive;
        if(EVP_CipherUpdate(cc,NULL,&ignored,B(c),(int)PyBytes_GET_SIZE(c))!=1 ||
           EVP_CipherUpdate(cc,out,&n,B(d),(int)input)!=1 || n<0 || (size_t)n>input) goto done_primitive;
        if(EVP_CipherFinal_ex(cc,out+n,&last)!=1 || last<0 || (size_t)n+(size_t)last!=input) goto done_primitive;
        len=input;
        if(enc) {if(EVP_CIPHER_CTX_ctrl(cc,EVP_CTRL_AEAD_GET_TAG,16,out+len)!=1) goto done_primitive;len+=16;}
    } else goto invalid_after;
    ret=PyBytes_FromStringAndSize((const char *)out,(Py_ssize_t)len); ok=ret!=NULL;
    goto done_primitive;
invalid_after:
    PyErr_SetString(PyExc_ValueError,"Invalid public diagnostic input");
done_primitive:
    EVP_CIPHER_CTX_free(cc); EVP_CIPHER_free(ci); EVP_KDF_CTX_free(kc); EVP_KDF_free(kd);
    EVP_MAC_CTX_free(mc); EVP_MAC_free(ma); OPENSSL_cleanse(out,sizeof(out));
    if(started) {if(marked) (void)ERR_pop_to_mark(); else ERR_clear_error();}
    if(!ok&&!PyErr_Occurred()) PyErr_SetString(PyExc_RuntimeError,"Public diagnostic failed");
    return ret;
invalid_primitive:
    PyErr_SetString(PyExc_ValueError,"Invalid public diagnostic input"); return NULL;
}
