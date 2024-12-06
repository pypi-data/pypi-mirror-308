"""
iogp.data.carve: File carving / extraction APIs.

*coin regexes adapted from https://github.com/Concinnity-Risks/RansomCoinPublic

Author: Vlad Topan (vtopan/gmail)
"""
from base64 import b64decode
from logging import error
import mmap
import re
import struct
import zlib


PAT = {
    'Bitcoin Private Key': '5[HJK][1-9A-Za-z][A-HJ-NP-Za-km-z]{48}',
    'Bitcoin Address': '[13][a-km-zA-HJ-NP-Z1-9]{25,34}',
    'Bitcoin Cash Address': '(bitcoincash:)?[qp][a-z0-9]{41}|(BITCOINCASH:)?[QP][A-Z0-9]{41}',
    'Ethereum Address': '0x[a-fA-F0-9]{40}',
    'Litecoin Address': '[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}',
}
RX = {
    'file_magic': (rb'(7z)\xBC\xAF\x27\x1C|(PK)\x01\x02|(BM)|(MZ).{1,200}PE\0\0|\xFF\xD8\xFF\xE0..(JFIF)|\x7F(ELF)|(GIF)8[79]|\x89(PNG)\r\n\x1A\n|\xD0\xCF\x11\xE0(\xA1\xB1)\x1A\xE1|%(PDF)-1\.\d+\x0A|(?:\x0A\x0D\x0D\x0A.{4})?(M<\+)\x1A|(\xD4\xC3\xB2\xA1|\xA1\xB2\xC3\xD4)\x02\0\x04\0|gimp (xcf) (?:file|v\d{3})\0', re.S),
    'text_file': (rb'[\x20-\x7E\x09\x0A\x0D]{512,}',),
    'jpg_end': (rb'\xFF\xD9',),
    'jpg_soi_end': (rb'\xFF[^\x00]',),
    'doc_end_1': ('\0'.join('DocumentSummaryInformation').encode(),),
    'doc_end_2': (rb'\0MSWordDoc\0\x10\0{3}Word.Document.8',),
    'pdf_end': (rb'[\r\n]%%EOF[\r\n]*',),
}
for k in RX:
    RX[k] = re.compile(*RX[k])

MAGIC_MAP = {
    # archive
    b'7z': '7z',
    b'PK': 'zip',
    # executable
    b'ELF': 'elf',
    b'MZ': 'exe',
    # image
    b'BM': 'bmp',
    b'GIF': 'gif',
    b'JFIF': 'jpg',
    b'PNG': 'png',
    # document
    b'\xA1\xB1': 'doc',
    b'PDF': 'pdf',
    # other
    b'M<+': 'pcapng',
    b'\xD4\xC3\xB2\xA1': 'pcap',
    b'\xA1\xB2\xC3\xD4': 'pcap',
    b'xcf': 'xcf',
}

ZIP_POTENTIAL_CDS = set()


def extract_elf(data, offset):
    """
    Extract an ELF binary.
    """
    is64 = data[offset + 4] == 2
    spat, base, size = ('<QQIHHHHH', 0x20, 30) if is64 else ('<IIIHHHHH', 0x1C, 22)
    e_phoff, e_shoff, _, _, e_phentsize, e_phnum, e_shentsize, e_shnum  = struct.unpack(spat, data[offset + base:offset + base + size])
    szmax = 0
    try:
        for i in range(e_shnum):
            offs = e_shoff + e_shentsize * i
            offs, size = struct.unpack('<II', data[offs + 16:offs + 24])
            if size:
                szmax = max(szmax, offs + size)
        for i in range(e_phnum):
            offs = e_phoff + e_phentsize * i
            offs, _, _, size = struct.unpack('<IIII', data[offs + 4:offs + 20])
            if size:
                szmax = max(szmax, offs + size)
    except struct.error:
        error('Failed parsing ELF!')
        szmax = 10 * 1024 * 1024
    return szmax, 'elf'


def extract_exe(data, offset):
    """
    Extract an MZ/PE image.
    """
    if offset + 0x400 > len(data):
        return None, None
    e_lfanew = struct.unpack('<i', data[offset + 0x3C:offset + 0x40])[0]
    peoffs = offset + e_lfanew
    if e_lfanew < 0 or peoffs + 0x1000 > len(data) or data[peoffs:peoffs + 4] != b'PE\0\0':
        return None, None
    seccnt = struct.unpack('<H', data[peoffs + 6:peoffs + 8])[0]
    secoffs = peoffs + 0xF8
    endoffs = -1
    for i in range(seccnt):
        offs = secoffs + i * 40 + 16
        fsize, faddr = struct.unpack('<II', data[offs:offs + 8])
        if fsize:
            endoffs = max(endoffs, faddr + fsize)
    return endoffs, 'exe'


def extract_zip(data, offset):
    """
    Extract a zip archive.
    """
    if offset in ZIP_POTENTIAL_CDS:
        return None, None
    # regex finds central directory entries, must validate each one - can mark checked ones though
    crt_offs = cd_start = offset
    delta = 28
    while 1:
        ZIP_POTENTIAL_CDS.add(crt_offs)
        base = crt_offs + delta
        fmt = '<HHHHHII'
        fmt_size = struct.calcsize(fmt)
        fn_len, ext_len, cmt_len, _, _, _, lfh_offs = struct.unpack(fmt, data[base:base + fmt_size])
        crt_offs += delta + fmt_size + fn_len + ext_len + cmt_len
        next_magic = data[crt_offs:crt_offs + 4]
        if next_magic[:2] != b'PK':
            return None, None
        if next_magic[2:4] != b'\x01\x02':
            if next_magic[2:4] == b'\x06\x06':
                # EOCDR64
                fmt = '<IQHHIIQQQQ'
                _, size, _, _, _, _, _, _, _, rel_offs = struct.unpack(fmt, data[crt_offs:crt_offs + struct.calcsize(fmt)])
                crt_offs += 12 + size
                next_magic = data[crt_offs:crt_offs + 4]
                if next_magic[:2] != b'PK':
                    return None, None
            if next_magic[2:4] == b'\x06\x07':
                # EOCDL64
                crt_offs += 20
                next_magic = data[crt_offs:crt_offs + 4]
                if next_magic[:2] != b'PK':
                    return None, None
            if next_magic[2:4] == b'\x05\x06':
                # EOCD
                fmt = '<IHHHHIIH'
                _, _, _, _, _, _, rel_offs, cmt_len = struct.unpack(fmt, data[crt_offs:crt_offs + struct.calcsize(fmt)])
                crt_offs += 22 + cmt_len
                start = cd_start - rel_offs
                if start < 0 or data[start:start + 4] != b'PK\x03\x04':
                    return None, None
                return (crt_offs - start, 'zip', start)
            else:
                return None, None


def extract_7z(data, offset):
    """
    Extract a 7z archive.
    """
    magic, ver_maj, ver_min, crc, next_offs, next_size, next_crc = struct.unpack('<6sBBIQQI', data[offset:offset + 32])
    if ver_maj != 0 or ver_min > 10:
        return None, None
    size = 32 + next_offs + next_size
    if offset + size > len(data):
        return None, None
    return size, '7z'


def extract_jpg(data, offset):
    """
    Extract a JPG image.
    """
    if offset == 0 or offset + 0x100 > len(data):
        return None, None
    end = offset + 2
    while end < len(data):
        hdr = data[end:end + 4]
        if len(hdr) == 2:
            hdr += b'\0\0'
        marker, size = struct.unpack(">HH", hdr)
        if marker == 0xffd9:
            break
        elif 0xffd0 <= marker <= 0xffda:
            pos = RX['jpg_soi_end'].search(data, pos=end + 4).start()
            end = pos
        else:
            end += size + 2
        if end - offset > 64 * 1024 * 1024:
            # this is probably a damaged JPG or false positive
            break
    return end - offset, 'jpg'


def extract_bmp(data, offset):
    """
    Extract a bitmap image.
    """
    magic, size, zero, offs = struct.unpack('<2sIII', data[offset:offset + 14])
    if zero != 0 or offset + offs > len(data) or offset + size > len(data):
        return None, None
    return size, 'bmp'


def extract_png(data, offset):
    """
    Extract a PNG image.
    """
    crt = offset + 8
    while crt + 8 < len(data):
        if crt - offset > 64 * 1024 * 1024:
            # this is probably a damaged PNG or false positive
            break
        size, ctype = struct.unpack('>I4s', data[crt:crt + 8])
        crt += size + 12
        if ctype == b'IEND':
            break
    return crt - offset, 'png'


def extract_doc(data, offset):
    """
    Extract a MS Word document.
    """
    if data[0x1A:0x1F] != b'\x03\0\xFE\xFF\x09':
        # todo: other docfiles
        return None, None
    if m := RX['doc_end_1'].search(data, pos=offset + 8, endpos=offset + 32 * 1024 * 1024):
        end = m.end() + 0x200
    elif m := RX['doc_end_2'].search(data, pos=offset + 8, endpos=offset + 32 * 1024 * 1024):
        end = m.end() + 0x100
    else:
        end = offset + 4 * 1024 * 1024
    return end - offset, 'doc'


def extract_pdf(data, offset):
    """
    Extract a PDF document.
    """
    if m := RX['pdf_end'].search(data, pos=offset + 8, endpos=offset + 32 * 1024 * 1024):
        end = m.end()
    else:
        end = offset + 4 * 1024 * 1024
    return end - offset, 'pdf'


def extract_embedded_files(data, whitelist=None, to_eof=False):
    """
    Extract embedded files from the given `bytes` buffer (or `mmap` object), returns

    :param whitelist: List of extensions to extract (default: all known).
    :return: Yields tuples (offset, size, extension); size is None if unknown.
    """
    global ZIP_POTENTIAL_CDS
    ZIP_POTENTIAL_CDS = set()
    for m in RX['file_magic'].finditer(data, pos=1):
        magic = [x for x in m.groups() if x][0]
        if whitelist and MAGIC_MAP[magic] not in whitelist:
            continue
        ext = MAGIC_MAP[magic]
        offset = m.start()
        extractor = globals().get('extract_' + ext)
        if extractor and not to_eof:
            res = extractor(data, offset)
            size, ext = res[:2]
            if len(res) == 3:
                offset = res[-1]
            if size == 0:
                size = len(data) - offset
        else:
            size = len(data) - offset
        if ext is not None:
            yield (offset, size, ext)



def find_encoded_data(data, all=False, compressed=False, base64=False, hex=False,
        max_comp_size=4 * 1024 * 1024, min_hex=6, min_base64=6):
    """
    Find Base64, hex, zlib and gzip encoded data.

    :param data: A bytes object (or similar).
    :return: yields tuples (offset, size, data, encoding)
    """
    rx = []
    if all or compressed:
        rx.append(rb'(?P<z>x[\x01\x5E\x9C\xDA])|(?P<g>\x1F\x8B)')
    if all or base64:
        # min len: 12 (=> min. len. 7 of original string)
        rx.append(rb'\b(?P<b>(?:[A-Za-z0-9/+]{4}){2,}(?:[A-Za-z0-9/+][AQgw]==|[A-Za-z0-9/+]{2}[AEIMQUYcgkosw048]=)?)\b')
    if all or hex:
        rx.append(rb'\b(?P<h>(?:[A-Fa-f0-9]{2}[ ,;:-]?){%d,})\b' % min_hex)
    rx = re.compile(b'|'.join(e for e in rx))
    camel_rx = re.compile(rb'[A-Z][0-9a-z]+[A-Z]+[0-9a-z]+[A-Z]')   # heuristic for Base64
    for m in rx.finditer(data):
        offs = m.start()
        size = m.end() - m.start()
        if m['z'] or m['g']:
            try:
                args = {'wbits': 31} if m['g'] else {}
                dobj = zlib.decompressobj(**args)
                buf = dobj.decompress(data[offs:offs + max_comp_size])
                size = max_comp_size - len(dobj.unused_data)
                yield offs, size, buf, 'zlib' if m['z'] else 'gzip'
            except zlib.error:
                pass
        elif buf := m['b']:
            if buf[-1] == '=' or camel_rx.search(buf):
                if len(buf) >= min_base64:
                    yield offs, size, b64decode(buf), 'Base64'
        else:
            yield offs, size, bytes.fromhex(re.sub(b'[^A-Fa-f0-9]+', b'', m['h']).decode()), 'hex'


if __name__ == '__main__':
    import glob
    import os
    import sys

    whitelist = None if len(sys.argv) < 3 else [x.strip().lower() for x in sys.argv[2].split(',')]
    for f in glob.glob(sys.argv[1]):
        print(f'[*] Carving {f}...')
        fh = open(f, 'rb')
        data = mmap.mmap(f.fileno(), 0)
        for offs, size, ext in extract_embedded_files(data, whitelist):
            fn = f'{os.path.basename(f)}.emb@{offs:X}.{ext}'
            print(f'[-]   - found {ext} @ 0x{offs:X}[{size}] - saving as {fn}...')
            open(fn, 'wb').write(data[offs:offs + size])
