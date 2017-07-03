import random
import base64


def sieve_primes_to(n):
    size = n // 2
    sieve = [1] * size
    limit = int(n**0.5)
    for i in range(1, limit):
        if sieve[i]:
            val = 2*i + 1
            tmp = ((size-1) - i) // val
            sieve[i+val::val] = [0] * tmp
    return [i*2 + 1 for i, v in enumerate(sieve) if v and i > 0]


def euc_mod_inv(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return (lastx * (-1 if aa < 0 else 1)) % bb


def calc_blocksize(n):
    blocksize = 1
    while 127**(blocksize+1) <= n:
        blocksize += 1
    return blocksize


def gen_tokens(p, q):

    n = p * q
    phi = (p-1) * (q-1)

    # print([x for x in sieve_primes_to(50) if phi % x != 0])
    # e = random.choice([x for x in sieve_primes_to(phi) if phi % x != 0])
    e = 65537
    d = euc_mod_inv(e, phi)

    return n, phi, e, d, calc_blocksize(n)


def en_block(data, bsize):
    blocks = [0] * -(-len(data) // bsize)
    for i in range(0, len(data), bsize):
        for k in range(bsize):
            if i+k < len(data):
                blocks[i // bsize] += data[i+k] * 127**(bsize-k-1)
    return blocks


def de_block(blocks, bsize):
    data = []
    for block in blocks:
        tmp = [0] * (bsize)
        for k in range(bsize):
            block, tmp[bsize-k-1] = divmod(block, 127)
        data.extend(tmp)
    return data


def rsa_encode(m, e, n):
    blocksize = calc_blocksize(n)
    blocks = en_block([ord(x) for x in m], blocksize)
    enc = [pow(i, e, n) for i in blocks]
    bb = de_block(enc, blocksize+1)
    c = base64.b64encode(bytes(bb)).decode()
    return c


def rsa_decode(c, d, n):
    blocksize = calc_blocksize(n)
    bb = list(base64.b64decode(c))
    blocks = en_block(bb, blocksize+1)
    dec = [pow(i, d, n) for i in blocks]
    asc = de_block(dec, blocksize)
    z = ''.join([chr(i) for i in asc]).rstrip('\0')
    return z


# p = 997
# q = 991
p = 499999996723
q = 49999996589
p = 13144131834269512219260941993714669605006625743172006030529504645527800951523697620149903055663251854220067020503783524785523675819158836547734770656069477
q = 12288506286091804108262645407658709962803358186316309871205769703371233115856772658236824631092740403057127271928820363983819544292950195585905303695015971

n, phi, e, d, blocksize = gen_tokens(p, q)

print('MODULO    :', n)
print('TOTIENT   :', phi)
print('BLOCKSIZE :', blocksize)
print('PUBLIC    :', e)
print('PRIVATE   :', d)
print()


m = 'Conveying or northward offending admitting perfectly my. Colonel gravity get thought fat smiling add but. Wonder twenty hunted and put income set desire expect. Am cottage calling my is mistake cousins talking up.'

c = rsa_encode(m, e, n)

print('CLEARTEXT:', m)
print('ENCRYPTED:', c)

z = rsa_decode(c, d, n)

print('DECRYPTED:', z)

print('Ratio: ', int(len(c) / len(m) * 100), '%')
print()
