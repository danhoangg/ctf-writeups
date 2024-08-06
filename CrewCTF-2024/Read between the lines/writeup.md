# ## Read between the lines (43 solves)
- Author: **7Rocky**
- Themes: **RSA, Lattices, LLL**
### Description
Small numbers and RSA do not get on well, but can I group them together?
## Writeup
The script we're given is short, it uses RSA to encrypt individual characters in an array, and then sums them up. It initialises by asserting the flag length is less than 100 and creating the array `encoded_flag`
```python
assert len(FLAG) < 100

encoded_flag = []
for i, b in enumerate(FLAG):  
    encoded_flag.extend([i + 0x1337] * b)
```
This creates a list where the index is represented with `i + 0x1337` and it's repeated `b` times, b being the ASCII value of the letter at that index. \
`e`, `p`, `q` and `n` are all generated in a standard fashion for RSA and each element in the list is encrypted. The list is summed up and the result stored in c.
```python
c = sum(pow(m, e, n) for m in encoded_flag) % n
```
c can be written as $$c=\sum_{i=0}^{99}b_i(i+0x1337)^e\mod n$$
$b_i$ is within the ASCII printable range and therefore is very small compared to everything else so it seems obvious to construct a lattice and apply LLL to get our target vector. \
Moving everything to one side and removing the mod: $$c - b_0(0+0x1337)^e-b_1(1+0x1337)^e-...+kn=0$$
We can then construct the lattice like so: $$
\begin{bmatrix}
1 & 0 & 0 & \dots & c \\
0 & 1 & 0 & \dots & (0+0x1337)^e \\
0 & 0 & 1 & \dots & (1+0x1337)^e \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
0 & 0 & 0 & \dots & n \\
\end{bmatrix}
$$
```python
encs = [pow(i + 0x1337, e, n) for i in range(100)]

M = identity_matrix(len(cts) + 2)
M[0, -1] = c
for i in range(1, 101):
    M[i, -1] = cts[i-1]
M[-1, -1] = n
```
Reducing this matrix, we look for the target vector $(1, -b_0, -b_1, \dots, 0)$
```python
res = M.LLL()
for r in res:
    if r[0] == 1:
        flag = r
```
If this is the correct vector, we can print it out and get our flag!
```python
for i in range(1, len(flag)-1):
    print(chr(-flag[i]), end='')
```
`crew{D1d_y0u_3xp3cT_LLL_t0_b3_h1Dd3n_b3tw3en_th3_l1n3s???}` 🥶🥶🥶