import hashlib
from datetime import datetime

def decode(txt, ts):
    h = hashlib.md5(str(int(ts)).encode()).hexdigest()
    res = ""
    for i, c in enumerate(txt):
        if c.isalpha():
            v = (int(h[i % len(h)], 16) + i * 3) % 26
            if c.isupper():
                res += chr((ord(c) - v - 65) % 26 + 65)
            else:
                res += chr((ord(c) - v - 97) % 26 + 97)
        else:
            res += c
    return res

enc = "INNVC{rJXKrb_FFg_NFTx_FMHDWFmX!!}"
ts = datetime(2024, 3, 15, 14, 30, 0).timestamp()

print("Decrypted:", decode(enc, ts))
