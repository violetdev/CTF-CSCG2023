
from pwn import *
from sage.all import *

prime = int("""
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF""".replace('\n', '').replace(' ', ''), 
16)

conn = remote('bd9508b840e0d70bd1ce6f47-casino.challenge.master.cscg.live', 31337, ssl=True)

conn.recvuntil(b'> ', timeout=1000)
conn.sendline(b'1')

while True:
    conn.recvline()
    conn.recvline()
    res = conn.recvline()
    print(res) # prints balance
    conn.recvline()
    conn.recvline()
    res = conn.recvuntil(b'> ', timeout=1000)
    res = res[12:-3]
    res = res.decode("utf-8") 
    dh = res.split(', ')
    #print(dh)
    lsa = kronecker(dh[0], prime)
    lsb = kronecker(dh[1], prime)
    lsc = kronecker(dh[2], prime)

    guess = 1

    if (lsa == 1 and lsb == 1) and lsc != 1:
        guess = 0
    if (lsa == 1 and lsb != 1) and lsc != 1:
        guess = 0
    if (lsa != 1 and lsb == 1) and lsc != 1:
        guess = 0
    if (lsa != 1 and lsb != 1) and lsc == 1:
        guess = 0

    conn.sendline(b'1' if guess == 1 else b'0')

conn.close()

#CSCG{I_should_have_used_prime_order_groups_instead}

