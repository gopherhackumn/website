#First decode the table

ptxt = b"AAAAAA"

keybase = b"AAAAAA"

def tobin(b): return "".join("{0:08b}".format(i) for i in b)
def xor(a, b): return "".join(str(int(c) ^ int(d)) for c, d in zip(a, b))
def frombin(b): return int(b, 2).to_bytes((len(b) + 7) // 8, byteorder="big")

keybasebin = tobin(keybase)

tdesired = ""
for msb in range(4):
    for lsb in range(4):
        desired = "{0:02b}".format(msb) + "{0:02b}".format(lsb)
        print(msb, lsb, desired)
        tdesired += desired

tdesired2 = tdesired + "0" * (48 - len(tdesired) % 48)
print(frombin(keybasebin))

for i in range(0, len(tdesired2), 48):
    seg = tdesired2[i:i+48]
    seg = xor(seg, keybasebin)
    print(bytes.hex(frombin(seg)))

results = [
    "010101011001101101110011010001000101100001111000101000011110011101101110",
    "111100110001010010101010010101010101010101010101010101010101010101010101",
]

result = (results[0] + results[1])[:len(tdesired) * 3 // 2]
print(len(result), result)

exptable = {}
revexptable = {}
cur = 0
for msb in range(4):
    for lsb in range(4):
        res = result[cur:cur+6]
        exptable[msb, lsb] = res
        revexptable[res] = (msb, lsb)
        # print(res)
        cur += 6

print(exptable)

# Decode

import secrets
randkey = b'\x1d9\x8e\x1a\xbfM' # secrets.token_bytes(6)
print(randkey, bytes.hex(randkey))

def decode(ctxt, key):
    keybin = tobin(key)

    res = ""
    for i in range(0, len(ctxt), 6):
        seg = ctxt[i:i+6]
        msb, lsb = revexptable[seg]
        msblsb = "{0:02b}".format(msb) + "{0:02b}".format(lsb)
        res += msblsb

    ptxt = ""
    for i in range(0, len(res), 48):
        seg = res[i:i+48]
        ptxt += xor(seg, keybin)

    return frombin(ptxt)

ctxt = "000101000101000101111100010010101101111000100001110001010101100001011001110011110001010001010010010010011001100001101000110001110011101101011110110011111100011001011110010010110011111000101010110001010101110011011101"

print(decode(ctxt, randkey))

# Flag

flagctxt = "111100010001010001101000000101110001010001100001100001100001000101101010010010010001100001101010000101010010111000011001010001101110111000101110010010010001111000000101101101110001010001110001010001000101000101111100010010010101000101110001111000010101100001011001010001011110011001010001101010010010100001010010010001011001111000110011010001010010010001010101111100101010100001101010101101110001100001010001011001110011000101100001010010110011101101010010100001110011011001101101101101011001101101100001"

# Probably starts with TUCTF
flagkey = b"AAAAAA"
for i, c in enumerate(b"TUCTF{"):
    for j in range(256):
        newflagkey = list(flagkey)
        newflagkey[i] = j
        newflagkey = bytes(newflagkey)
        flagptxt = decode(flagctxt, newflagkey)
        if flagptxt[i] == c:
            flagkey = newflagkey
            break
    print(c)

print(flagkey)
print(decode(flagctxt, flagkey))


