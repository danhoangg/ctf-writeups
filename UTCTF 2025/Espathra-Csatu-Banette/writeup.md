# Espathra-Csatu-Banette (149 solves, 781 points)
- Author: **Sasha (@kyrili on discord)**
- Themes: **AES ECB**

### Description
Everyone keeps telling me how ECB isn't meta-viable and that I should stop playing it to tournaments. Well, I love ECB so I've added some new tech that should hopefully get me some better results!

## Writeup
The source code for the server is short and simple, your input is encrypted and the flag is placed within your input, according to a custom checksum function
```py
x = input()
chksum = sum(ord(c) for c in x) % (len(x)+1)
```
First thing to find out is the flag length, the program is using `Crypto.Util.Padding.pad` and so I just keep sending `aaaa` until the encrypted output's number of blocks change. 
Sending an input of length 10, the encrypted output becomes 64 bytes long, and we can conclude that flag must be 38 bytes long.
We also know that the last block is simply (b'\x10' * 16) due to the padding. 

Going back to `chksum = sum(ord(c) for c in x) % (len(x)+1)`. If we find an input where the checksum is the length of the input, we would essentially be encryption (input + flag).
Getting an input of length 11 and checksum of 11, would push the last byte of the flag into the last block, I get my checksum of 11 by just going through the characters and checking the checksum:
```py
count = 11
for i in string.printable:
    x = i * count
    chksum = sum(ord(c) for c in x) % (len(x) + 1)
    if chksum == count:
        print(f'using {x}')
        break
```
We get `8fe44858cf9f9a43085c8792876907ed 2927539b79db724ac3424a43cb83d639 6777369a7d000b4d7ffdafda21767483 afa0cbf89467e26fef03fa11174142c5` when sending this input in `%%%%%%%%%%%` 

Next we can choose an input of length 11 with a checksum of less than 11, this would let us encrypt the last letter of our input.
We can bruteforce all the possible printable strings and therefore we can figure out the flag by bruteforcing one byte at a time!
I do this by going through the printable characters until I get a checksum I want:
```py
flag = ''
# i is the character we're trying to see if it matches the flag character
# j is filler characters, which still need to conform to the checksum
for i in string.printable:
    for j in string.printable: 
        x = (j * 10) + i + flag
        chksum = sum(ord(c) for c in x) % (len(x) + 1)
        if chksum < len(x) - len(flag):
            break
```
Sending in an input of `aaaaaaaaaa}` returns us `97e6ed11d3b10676379059c57fb18919 7f5bc9e524fb0a8f19104c819e164bc5 b4f50b4f260bdc6350d83397c2cac665 afa0cbf89467e26fef03fa11174142c5`.
Look, the last block is exactly the same, therefore we know the last character of the flag is a `}`.

We can do this for every byte in the flag until we get all 38 bytes: `utflag{st0p_r0ll1ng_y0ur_0wn_crypt0!!}` 😎😎😎
