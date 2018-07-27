from pdfwatermarker.thirdparty.PyPDF2 import PdfFileWriter
from pdfwatermarker.thirdparty.PyPDF2.pdf import md5, ByteStringObject, ArrayObject, _alg33, _alg34, _alg35, NameObject, DictionaryObject, \
    NumberObject, b_
from pdfwatermarker.thirdparty.PyPDF2.utils import b_, ord_


def set_permissions(status):
    if status:
        return -1852
    else:
        return -1


class PdfFileWriter2(PdfFileWriter):
    def encrypt(self, user_pwd, owner_pwd=None, use_128bit=True, restrict_permission=False):
        """This is an override method of PdfFileWriter built to control permissions parameter (P)"""
        import time, random
        if owner_pwd == None:
            owner_pwd = user_pwd
        if use_128bit:
            V = 2
            rev = 3
            keylen = int(128 / 8)
        else:
            V = 1
            rev = 2
            keylen = int(40 / 8)
        # permit everything:
        P = set_permissions(restrict_permission)
        O = ByteStringObject(_alg33(owner_pwd, user_pwd, rev, keylen))
        ID_1 = ByteStringObject(md5(b_(repr(time.time()))).digest())
        ID_2 = ByteStringObject(md5(b_(repr(random.random()))).digest())
        self._ID = ArrayObject((ID_1, ID_2))
        if rev == 2:
            U, key = _alg34(user_pwd, O, P, ID_1)
        else:
            assert rev == 3
            U, key = _alg35(user_pwd, rev, keylen, O, P, ID_1, False)
        encrypt = DictionaryObject()
        encrypt[NameObject("/Filter")] = NameObject("/Standard")
        encrypt[NameObject("/V")] = NumberObject(V)
        if V == 2:
            encrypt[NameObject("/Length")] = NumberObject(keylen * 8)
        encrypt[NameObject("/R")] = NumberObject(rev)
        encrypt[NameObject("/O")] = ByteStringObject(O)
        encrypt[NameObject("/U")] = ByteStringObject(U)
        encrypt[NameObject("/P")] = NumberObject(P)
        self._encrypt = self._addObject(encrypt)
        self._encrypt_key = key


def RC4_encrypt(key, plaintext):
    S = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + S[i] + ord_(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]
    i, j = 0, 0
    retval = b_("")
    for x in range(len(plaintext)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = S[(S[i] + S[j]) % 256]
        retval += b_(chr(ord_(plaintext[x]) ^ t))
    return retval
