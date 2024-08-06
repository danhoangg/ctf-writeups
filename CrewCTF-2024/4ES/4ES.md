# 4ES (90 solves)
- Author: **7Rocky**
- Themes: **AES**, **Ciphers**
### Description
AES is very robust, but let's quadruple its power!
## Writeup
The script we're given, firstly picks 4 keys, each being a random 3 characters from a specific string
```py
chars = b'crew_AES*4=$!?'  
L = 3  
  
w, x, y, z = (  
    bytes(choices(chars, k=L)),  
    bytes(choices(chars, k=L)),  
    bytes(choices(chars, k=L)),  
    bytes(choices(chars, k=L)),  
)
```
The keys are then calculated by hashing w, x, y, z and are used to encrypt a known plaintext 4 times
```py
pt = b'AES_AES_AES_AES!'  
ct = AES.new(k4, AES.MODE_ECB).encrypt(  
         AES.new(k3, AES.MODE_ECB).encrypt(  
             AES.new(k2, AES.MODE_ECB).encrypt(  
                 AES.new(k1, AES.MODE_ECB).encrypt(  
                     pt  
                 )  
             )  
         )  
     )
```
A final key is created by combining w, x, y, z and is used to encrypt the flag, we're then given pt, ct and the encrypted flag.
Looking at this, it reminded me of the DES cipher, one of it's biggest flaws was the meet-in-the-middle attack, where an attacker could retrieve the private key. This was due to DES encryption method consisting of multiple encryptions and decryptions, like this challenge.
Brute-forcing all 4 keys at the same time would be $14^{12} \approx6\times10^{13}$ possibilities, which is infeasible. However if we get all the possible pt encryptions for 2 keys, store them in a dictionary and then try all possible ct decryptions for 2 keys, we can check for matching values, and if they do, then both pairs of keys make up the w, x, y and z. This lowers the total iterations to a maximum of $14^6 \times 2 \approx 10^7$ which is much lower.
Initialising the variables:
```python
decrypted = {}  
ct_original = 'edb43249be0d7a4620b9b876315eb430'  
ct_original = bytes.fromhex(ct_original)  
pt_original = b'AES_AES_AES_AES!'
```
Putting all possible decryptions into a dictionary:
```python
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
```
Then going through all possible encryptions and checking for an overlap
```python
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
```
`crew{m1tm_at74cK_1s_g0lD_4nd_py7h0n_i5_sl0w!!}`🥳🥳🥳