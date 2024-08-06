from Crypto.Cipher import AES
from hashlib import sha256
from itertools import product
from tqdm import tqdm

chars = b'crew_AES*4=$!?'
L = 3

decrypted = {}
ct_original = 'edb43249be0d7a4620b9b876315eb430'
ct_original = bytes.fromhex(ct_original)
pt_original = b'AES_AES_AES_AES!'

for y in tqdm(product(chars, repeat=L)):
    for z in product(chars, repeat=L):
        y = bytes(y)
        z = bytes(z)

        k3 = sha256(y).digest()
        k4 = sha256(z).digest()

        pt = AES.new(k3, AES.MODE_ECB).decrypt(
            AES.new(k4, AES.MODE_ECB).decrypt(
                ct_original
            )
        )

        decrypted[pt] = (y, z)

for w in tqdm(product(chars, repeat=L)):
    for x in product(chars, repeat=L):
        w = bytes(w)
        x = bytes(x)

        k1 = sha256(w).digest()
        k2 = sha256(x).digest()

        ct = AES.new(k2, AES.MODE_ECB).encrypt(
            AES.new(k1, AES.MODE_ECB).encrypt(
                pt_original
            )
        )

        if ct in decrypted:
            print(w, x, decrypted[ct])
            w, x, y, z = w, x, decrypted[ct][0], decrypted[ct][1]
            key = sha256(w + x + y + z).digest()
            enc_flag = 'e5218894e05e14eb7cc27dc2aeed10245bfa4426489125a55e82a3d81a15d18afd152d6c51a7024f05e15e1527afa84b'
            enc_flag = bytes.fromhex(enc_flag)

            print(AES.new(key, mode=AES.MODE_ECB).decrypt(enc_flag))

            exit()
