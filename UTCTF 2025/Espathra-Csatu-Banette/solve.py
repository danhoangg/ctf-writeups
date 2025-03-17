from pwn import *
from Crypto.Util.number import long_to_bytes

flag_len = 38
r = remote('challenge.utctf.live', 7150)
count = 11
flag = ''
while count <= 48:
    for i in string.printable:
        x = i * count
        chksum = sum(ord(c) for c in x) % (len(x) + 1)
        if chksum == count:
            print(f'using {x}')
            break
    r.recvuntil(b': ')
    r.sendline(x.encode())
    b = long_to_bytes(int(r.recvuntil(b'\n')[2:-1], 16))[48:64]

    for i in string.printable:
        for j in string.printable:
            x = (j * 10) + i + flag
            chksum = sum(ord(c) for c in x) % (len(x) + 1)
            if chksum < len(x) - len(flag):
                print(f'trying {i} and {x}')
                break

        r.recvuntil(b': ')
        r.sendline(x.encode())
        b2 = long_to_bytes(int(r.recvuntil(b'\n')[2:-1], 16))[48:64]
        if b == b2:
            flag = i + flag
            print(f'flag: {flag}')
            break
    count += 1
