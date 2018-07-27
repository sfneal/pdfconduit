import codecs
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.filters import decodeStreamData
from PyPDF2.generic import StreamObject, DictionaryObject, encode_pdfdocencoding, chr_, TextStringObject, utils, \
    decode_pdfdocencoding, DecodedStreamObject, EncodedStreamObject, readNonWhitespace, readObject, skipOverComment, \
    PdfStreamError, readHexStringFromStream, BooleanObject, readStringFromStream, NumberSigns, IndirectPattern, ObjectPrefix
from PyPDF2.pdf import md5, ByteStringObject, ArrayObject, NameObject, NumberObject, b_, str_, \
    _encryption_padding, _alg32, ord_, _alg33_1, PageObject, IndirectObject, u_, NullObject


def readObject2(stream, pdf):
    tok = stream.read(1)
    stream.seek(-1, 1) # reset to start
    idx = ObjectPrefix.find(tok)
    if idx == 0:
        # name object
        return NameObject.readFromStream(stream, pdf)
    elif idx == 1:
        # hexadecimal string OR dictionary
        peek = stream.read(2)
        stream.seek(-2, 1) # reset to start
        if peek == b_('<<'):
            return DictionaryObject2.readFromStream(stream, pdf)
        else:
            return readHexStringFromStream(stream)
    elif idx == 2:
        # array object
        return ArrayObject.readFromStream(stream, pdf)
    elif idx == 3 or idx == 4:
        # boolean object
        return BooleanObject.readFromStream(stream)
    elif idx == 5:
        # string object
        return readStringFromStream(stream)
    elif idx == 6:
        # null object
        return NullObject.readFromStream(stream)
    elif idx == 7:
        # comment
        while tok not in (b_('\r'), b_('\n')):
            tok = stream.read(1)
        tok = readNonWhitespace(stream)
        stream.seek(-1, 1)
        return readObject(stream, pdf)
    else:
        # number object OR indirect reference
        if tok in NumberSigns:
            # number
            return NumberObject.readFromStream(stream)
        peek = stream.read(20)
        stream.seek(-len(peek), 1) # reset to start
        if IndirectPattern.match(peek) != None:
            return IndirectObject.readFromStream(stream, pdf)
        else:
            return NumberObject.readFromStream(stream)


class DecodedStreamObject2(DecodedStreamObject):
    import inspect
    # print(inspect.stack()[1])
    def getData(self):
        return self._data

    def setData(self, data):
        self._data = data


class EncodedStreamObject2(EncodedStreamObject):
    def getData(self):
        if self.decodedSelf:
            # cached version of decoded object
            return self.decodedSelf.getData()
        else:
            # create decoded object
            decoded = DecodedStreamObject2()

            decoded._data = decodeStreamData(self)
            for key, value in list(self.items()):
                if not key in ("/Length", "/Filter", "/DecodeParms"):
                    decoded[key] = value
            self.decodedSelf = decoded
            return decoded._data

    def setData(self, data):
        raise utils.PdfReadError("Creating EncodedStreamObject is not currently supported")


class TextStringObject2(TextStringObject):
    def writeToStream(self, stream, encryption_key):
        # Try to write the string out as a PDFDocEncoding encoded string.  It's
        # nicer to look at in the PDF file.  Sadly, we take a performance hit
        # here for trying...
        try:
            bytearr = encode_pdfdocencoding(self)
        except UnicodeEncodeError:
            bytearr = codecs.BOM_UTF16_BE + self.encode("utf-16be")
        if encryption_key:
            bytearr = RC4_encrypt(encryption_key, bytearr)
            obj = ByteStringObject(bytearr)
            obj.writeToStream(stream, None)
        else:
            stream.write(b_("("))
            for c in bytearr:
                if not chr_(c).isalnum() and c != b_(' '):
                    stream.write(b_("\\%03o" % ord_(c)))
                else:
                    stream.write(b_(chr_(c)))
            stream.write(b_(")"))


class IndirectObject2(IndirectObject):
    def writeToStream(self, stream, encryption_key):
        stream.write(b_("%s %s R" % (self.idnum, self.generation)))

    def getObject(self):
        return self.pdf.getObject(self).getObject()


class DictionaryObject2(DictionaryObject):
    def writeToStream(self, stream, encryption_key):
        stream.write(b_("<<\n"))
        for key, value in list(self.items()):
            # print(type(value), key)
            key.writeToStream(stream, encryption_key)
            stream.write(b_(" "))
            value.writeToStream(stream, encryption_key)
            stream.write(b_("\n"))
        stream.write(b_(">>"))

    def readFromStream(stream, pdf):
        debug = False
        tmp = stream.read(2)
        if tmp != b_("<<"):
            raise utils.PdfReadError("Dictionary read error at byte %s: stream must begin with '<<'" % utils.hexStr(stream.tell()))
        data = {}
        while True:
            tok = readNonWhitespace(stream)
            if tok == b_('\x00'):
                continue
            elif tok == b_('%'):
                stream.seek(-1, 1)
                skipOverComment(stream)
                continue
            if not tok:
                # stream has truncated prematurely
                raise PdfStreamError("Stream has ended unexpectedly")

            if debug: print(("Tok:", tok))
            if tok == b_(">"):
                stream.read(1)
                break
            stream.seek(-1, 1)
            key = readObject2(stream, pdf)
            tok = readNonWhitespace(stream)
            stream.seek(-1, 1)
            value = readObject2(stream, pdf)
            if not data.get(key):
                data[key] = value
            elif pdf.strict:
                # multiple definitions of key not permitted
                raise utils.PdfReadError("Multiple definitions in dictionary at byte %s for key %s" \
                                           % (utils.hexStr(stream.tell()), key))
            else:
                warnings.warn("Multiple definitions in dictionary at byte %s for key %s" \
                                           % (utils.hexStr(stream.tell()), key), utils.PdfReadWarning)

        pos = stream.tell()
        s = readNonWhitespace(stream)
        if s == b_('s') and stream.read(5) == b_('tream'):
            eol = stream.read(1)
            # odd PDF file output has spaces after 'stream' keyword but before EOL.
            # patch provided by Danial Sandler
            while eol == b_(' '):
                eol = stream.read(1)
            assert eol in (b_("\n"), b_("\r"))
            if eol == b_("\r"):
                # read \n after
                if stream.read(1)  != b_('\n'):
                    stream.seek(-1, 1)
            # this is a stream object, not a dictionary
            assert "/Length" in data
            length = data["/Length"]
            if debug: print(data)
            if isinstance(length, IndirectObject):
                t = stream.tell()
                length = pdf.getObject(length)
                stream.seek(t, 0)
            data["__streamdata__"] = stream.read(length)
            if debug: print("here")
            #if debug: print(binascii.hexlify(data["__streamdata__"]))
            e = readNonWhitespace(stream)
            ndstream = stream.read(8)
            if (e + ndstream) != b_("endstream"):
                # (sigh) - the odd PDF file has a length that is too long, so
                # we need to read backwards to find the "endstream" ending.
                # ReportLab (unknown version) generates files with this bug,
                # and Python users into PDF files tend to be our audience.
                # we need to do this to correct the streamdata and chop off
                # an extra character.
                pos = stream.tell()
                stream.seek(-10, 1)
                end = stream.read(9)
                if end == b_("endstream"):
                    # we found it by looking back one character further.
                    data["__streamdata__"] = data["__streamdata__"][:-1]
                else:
                    if debug: print(("E", e, ndstream, debugging.toHex(end)))
                    stream.seek(pos, 0)
                    raise utils.PdfReadError("Unable to find 'endstream' marker after stream at byte %s." % utils.hexStr(stream.tell()))
        else:
            stream.seek(pos, 0)
        if "__streamdata__" in data:
            return StreamObject2.initializeFromDictionary(data)
        else:
            retval = DictionaryObject2()
            retval.update(data)
            return retval
    readFromStream = staticmethod(readFromStream)


class StreamObject2(StreamObject):
    def writeToStream(self, stream, encryption_key):
        self[NameObject("/Length")] = NumberObject(len(self._data))
        DictionaryObject2.writeToStream(self, stream, encryption_key)
        del self["/Length"]
        stream.write(b_("\nstream\n"))
        data = self._data
        if encryption_key:
            data = RC4_encrypt(encryption_key, data)
        stream.write(data)
        stream.write(b_("\nendstream"))

    def initializeFromDictionary(data):
        if "/Filter" in data:
            retval = EncodedStreamObject2()
        else:
            retval = DecodedStreamObject2()
        retval._data = data["__streamdata__"]
        del data["__streamdata__"]
        del data["/Length"]
        retval.update(data)
        return retval
    initializeFromDictionary = staticmethod(initializeFromDictionary)


def set_permissions(status):
    if status:
        return -1852
    else:
        return -1


# Given a string (either a "str" or "unicode"), create a ByteStringObject or a
# TextStringObject to represent the string.
def createStringObject(string):
    if isinstance(string, utils.string_type):
        return TextStringObject2(string)
    elif isinstance(string, utils.bytes_type):
        try:
            if string.startswith(codecs.BOM_UTF16_BE):
                retval = TextStringObject2(string.decode("utf-16"))
                retval.autodetect_utf16 = True
                return retval
            else:
                # This is probably a big performance hit here, but we need to
                # convert string objects into the text/unicode-aware version if
                # possible... and the only way to check if that's possible is
                # to try.  Some strings are strings, some are just byte arrays.
                retval = TextStringObject2(decode_pdfdocencoding(string))
                retval.autodetect_pdfdocencoding = True
                return retval
        except UnicodeDecodeError:
            return ByteStringObject(string)
    else:
        raise TypeError("createStringObject should have str or unicode arg")


class PdfFileReader2(PdfFileReader):
    def getObject(self, indirectReference):
        debug = False
        if debug: print(("looking at:", indirectReference.idnum, indirectReference.generation))
        retval = self.cacheGetIndirectObject2(indirectReference.generation,
                                                indirectReference.idnum)
        if retval != None:
            return retval
        if indirectReference.generation == 0 and \
                        indirectReference.idnum in self.xref_objStm:
            retval = self._getObjectFromStream(indirectReference)
        elif indirectReference.generation in self.xref and \
                indirectReference.idnum in self.xref[indirectReference.generation]:
            start = self.xref[indirectReference.generation][indirectReference.idnum]
            if debug: print(("  Uncompressed Object", indirectReference.idnum, indirectReference.generation, ":", start))
            self.stream.seek(start, 0)
            idnum, generation = self.readObjectHeader(self.stream)
            if idnum != indirectReference.idnum and self.xrefIndex:
                # Xref table probably had bad indexes due to not being zero-indexed
                if self.strict:
                    raise utils.PdfReadError("Expected object ID (%d %d) does not match actual (%d %d); xref table not zero-indexed." \
                                     % (indirectReference.idnum, indirectReference.generation, idnum, generation))
                else: pass # xref table is corrected in non-strict mode
            elif idnum != indirectReference.idnum:
                # some other problem
                raise utils.PdfReadError("Expected object ID (%d %d) does not match actual (%d %d)." \
                                         % (indirectReference.idnum, indirectReference.generation, idnum, generation))
            assert generation == indirectReference.generation
            retval = readObject2(self.stream, self)

            # override encryption is used for the /Encrypt dictionary
            if not self._override_encryption and self.isEncrypted:
                # if we don't have the encryption key:
                if not hasattr(self, '_decryption_key'):
                    raise utils.PdfReadError("file has not been decrypted")
                # otherwise, decrypt here...
                import struct
                pack1 = struct.pack("<i", indirectReference.idnum)[:3]
                pack2 = struct.pack("<i", indirectReference.generation)[:2]
                key = self._decryption_key + pack1 + pack2
                assert len(key) == (len(self._decryption_key) + 5)
                md5_hash = md5(key).digest()
                key = md5_hash[:min(16, len(self._decryption_key) + 5)]
                retval = self._decryptObject(retval, key)
        else:
            warnings.warn("Object %d %d not defined."%(indirectReference.idnum,
                        indirectReference.generation), utils.PdfReadWarning)
            #if self.strict:
            raise utils.PdfReadError("Could not find object.")
        self.cacheIndirectObject(indirectReference.generation,
                    indirectReference.idnum, retval)
        return retval



class PdfFileWriter2(PdfFileWriter):
    def __init__(self):
        self._header = b_("%PDF-1.3")
        self._objects = []  # array of indirect objects

        # The root of our page tree node.
        pages = DictionaryObject2()
        pages.update({
            NameObject("/Type"): NameObject("/Pages"),
            NameObject("/Count"): NumberObject(0),
            NameObject("/Kids"): ArrayObject(),
        })
        self._pages = self._addObject(pages)

        # info object
        info = DictionaryObject2()
        info.update({
            NameObject("/Producer"): createStringObject(codecs.BOM_UTF16_BE + u_("PyPDF2").encode('utf-16be'))
        })
        self._info = self._addObject(info)

        # root object
        root = DictionaryObject2()
        root.update({
            NameObject("/Type"): NameObject("/Catalog"),
            NameObject("/Pages"): self._pages,
        })
        self._root = None
        self._root_object = root

    def _addObject(self, obj):
        # print(type(obj))
        self._objects.append(obj)
        return IndirectObject2(len(self._objects), 0, self)

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
        encrypt = DictionaryObject2()
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

    def write(self, stream):
        """
        Writes the collection of pages added to this object out as a PDF file.

        :param stream: An object to write the file to.  The object must support
            the write method and the tell method, similar to a file object.
        """
        if hasattr(stream, 'mode') and 'b' not in stream.mode:
            warnings.warn("File <%s> to write to is not in binary mode. It may not be written to correctly." % stream.name)
        debug = False
        import struct

        if not self._root:
            self._root = self._addObject(self._root_object)

        externalReferenceMap = {}

        # PDF objects sometimes have circular references to their /Page objects
        # inside their object tree (for example, annotations).  Those will be
        # indirect references to objects that we've recreated in this PDF.  To
        # address this problem, PageObject's store their original object
        # reference number, and we add it to the external reference map before
        # we sweep for indirect references.  This forces self-page-referencing
        # trees to reference the correct new object location, rather than
        # copying in a new copy of the page object.
        for objIndex in range(len(self._objects)):
            obj = self._objects[objIndex]
            if isinstance(obj, PageObject) and obj.indirectRef != None:
                data = obj.indirectRef
                if data.pdf not in externalReferenceMap:
                    externalReferenceMap[data.pdf] = {}
                if data.generation not in externalReferenceMap[data.pdf]:
                    externalReferenceMap[data.pdf][data.generation] = {}
                externalReferenceMap[data.pdf][data.generation][data.idnum] = IndirectObject2(objIndex + 1, 0, self)

        self.stack = []
        if debug: print(("ERM:", externalReferenceMap, "root:", self._root))
        self._sweepIndirectReferences(externalReferenceMap, self._root)
        del self.stack

        # Begin writing:
        object_positions = []
        stream.write(self._header + b_("\n"))
        for i in range(len(self._objects)):
            idnum = (i + 1)
            obj = self._objects[i]
            object_positions.append(stream.tell())
            stream.write(b_(str(idnum) + " 0 obj\n"))
            key = None
            if hasattr(self, "_encrypt") and idnum != self._encrypt.idnum:
                pack1 = struct.pack("<i", i + 1)[:3]
                pack2 = struct.pack("<i", 0)[:2]
                key = self._encrypt_key + pack1 + pack2
                assert len(key) == (len(self._encrypt_key) + 5)
                md5_hash = md5(key).digest()
                key = md5_hash[:min(16, len(self._encrypt_key) + 5)]
            print(type(obj))
            obj.writeToStream(stream, key)
            import inspect
            # print(inspect.stack()[1])
            stream.write(b_("\nendobj\n"))

        # xref table
        xref_location = stream.tell()
        stream.write(b_("xref\n"))
        stream.write(b_("0 %s\n" % (len(self._objects) + 1)))
        stream.write(b_("%010d %05d f \n" % (0, 65535)))
        for offset in object_positions:
            stream.write(b_("%010d %05d n \n" % (offset, 0)))

        # trailer
        stream.write(b_("trailer\n"))
        trailer = DictionaryObject2()
        trailer.update({
            NameObject("/Size"): NumberObject(len(self._objects) + 1),
            NameObject("/Root"): self._root,
            NameObject("/Info"): self._info,
        })
        if hasattr(self, "_ID"):
            trailer[NameObject("/ID")] = self._ID
        if hasattr(self, "_encrypt"):
            trailer[NameObject("/Encrypt")] = self._encrypt
        trailer.writeToStream(stream, None)

        # eof
        stream.write(b_("\nstartxref\n%s\n%%%%EOF\n" % (xref_location)))

    def _sweepIndirectReferences(self, externMap, data):
        debug = False
        if debug: print((data, "TYPE", data.__class__.__name__))
        if isinstance(data, DictionaryObject):
            for key, value in list(data.items()):
                origvalue = value
                value = self._sweepIndirectReferences(externMap, value)
                if isinstance(value, StreamObject):
                    # a dictionary value is a stream.  streams must be indirect
                    # objects, so we need to change this value.
                    value = self._addObject(value)
                data[key] = value
            return data
        elif isinstance(data, ArrayObject):
            for i in range(len(data)):
                value = self._sweepIndirectReferences(externMap, data[i])
                if isinstance(value, StreamObject):
                    # an array value is a stream.  streams must be indirect
                    # objects, so we need to change this value
                    value = self._addObject(value)
                data[i] = value
            return data
        elif isinstance(data, IndirectObject):
            # internal indirect references are fine
            if data.pdf == self:
                if data.idnum in self.stack:
                    return data
                else:
                    self.stack.append(data.idnum)
                    realdata = self.getObject(data)
                    self._sweepIndirectReferences(externMap, realdata)
                    return data
            else:
                newobj = externMap.get(data.pdf, {}).get(data.generation, {}).get(data.idnum, None)
                if newobj == None:
                    try:
                        newobj = data.pdf.getObject(data)
                        self._objects.append(None) # placeholder
                        idnum = len(self._objects)
                        newobj_ido = IndirectObject(idnum, 0, self)
                        if data.pdf not in externMap:
                            externMap[data.pdf] = {}
                        if data.generation not in externMap[data.pdf]:
                            externMap[data.pdf][data.generation] = {}
                        externMap[data.pdf][data.generation][data.idnum] = newobj_ido
                        newobj = self._sweepIndirectReferences(externMap, newobj)
                        self._objects[idnum-1] = newobj
                        return newobj_ido
                    except ValueError:
                        # Unable to resolve the Object, returning NullObject instead.
                        return NullObject()
                return newobj
        else:
            return data


# Implementation of algorithm 3.3 of the PDF standard security handler,
# section 3.5.2 of the PDF 1.6 reference.
def _alg33(owner_pwd, user_pwd, rev, keylen):
    # steps 1 - 4
    key = _alg33_1(owner_pwd, rev, keylen)
    # 5. Pad or truncate the user password string as described in step 1 of
    # algorithm 3.2.
    user_pwd = b_((user_pwd + str_(_encryption_padding))[:32])
    # 6. Encrypt the result of step 5, using an RC4 encryption function with
    # the encryption key obtained in step 4.
    val = RC4_encrypt(key, user_pwd)
    # 7. (Revision 3 or greater) Do the following 19 times: Take the output
    # from the previous invocation of the RC4 function and pass it as input to
    # a new invocation of the function; use an encryption key generated by
    # taking each byte of the encryption key obtained in step 4 and performing
    # an XOR operation between that byte and the single-byte value of the
    # iteration counter (from 1 to 19).
    if rev >= 3:
        for i in range(1, 20):
            new_key = ''
            for l in range(len(key)):
                new_key += chr(ord_(key[l]) ^ i)
            val = RC4_encrypt(new_key, val)
    # 8. Store the output from the final invocation of the RC4 as the value of
    # the /O entry in the encryption dictionary.
    return val


# Implementation of algorithm 3.4 of the PDF standard security handler,
# section 3.5.2 of the PDF 1.6 reference.
def _alg34(password, owner_entry, p_entry, id1_entry):
    # 1. Create an encryption key based on the user password string, as
    # described in algorithm 3.2.
    key = _alg32(password, 2, 5, owner_entry, p_entry, id1_entry)
    # 2. Encrypt the 32-byte padding string shown in step 1 of algorithm 3.2,
    # using an RC4 encryption function with the encryption key from the
    # preceding step.
    U = RC4_encrypt(key, _encryption_padding)
    # 3. Store the result of step 2 as the value of the /U entry in the
    # encryption dictionary.
    return U, key


# Implementation of algorithm 3.4 of the PDF standard security handler,
# section 3.5.2 of the PDF 1.6 reference.
def _alg35(password, rev, keylen, owner_entry, p_entry, id1_entry, metadata_encrypt):
    # 1. Create an encryption key based on the user password string, as
    # described in Algorithm 3.2.
    key = _alg32(password, rev, keylen, owner_entry, p_entry, id1_entry)
    # 2. Initialize the MD5 hash function and pass the 32-byte padding string
    # shown in step 1 of Algorithm 3.2 as input to this function.
    m = md5()
    m.update(_encryption_padding)
    # 3. Pass the first element of the file's file identifier array (the value
    # of the ID entry in the document's trailer dictionary; see Table 3.13 on
    # page 73) to the hash function and finish the hash.  (See implementation
    # note 25 in Appendix H.)
    m.update(id1_entry.original_bytes)
    md5_hash = m.digest()
    # 4. Encrypt the 16-byte result of the hash, using an RC4 encryption
    # function with the encryption key from step 1.
    val = RC4_encrypt(key, md5_hash)
    # 5. Do the following 19 times: Take the output from the previous
    # invocation of the RC4 function and pass it as input to a new invocation
    # of the function; use an encryption key generated by taking each byte of
    # the original encryption key (obtained in step 2) and performing an XOR
    # operation between that byte and the single-byte value of the iteration
    # counter (from 1 to 19).
    for i in range(1, 20):
        new_key = b_('')
        for l in range(len(key)):
            new_key += b_(chr(ord_(key[l]) ^ i))
        val = RC4_encrypt(new_key, val)
    # 6. Append 16 bytes of arbitrary padding to the output from the final
    # invocation of the RC4 function and store the 32-byte result as the value
    # of the U entry in the encryption dictionary.
    # (implementator note: I don't know what "arbitrary padding" is supposed to
    # mean, so I have used null bytes.  This seems to match a few other
    # people's implementations)
    return val + (b_('\x00') * 16), key


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

