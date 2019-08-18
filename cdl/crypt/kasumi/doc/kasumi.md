# Kasumi

Kasumi has 8 rounds; each round takes 2 cycles in this implementation.

Each round has 8 16-bit key values, which are derived from a 128-bit
register that rotates by 16 bits on each round.
The round key values are either one of the 16-bits rotated, or XORed with a value.

Each round then uses an 'FL' function and an 'FO' function. The 'FO' function takes two cycles.

FL is a simple combinatorial function which uses relatively few gates.
FO is more sophisticated (hence 2 cycles) - it itself consists of 3 subrounds.

FO in essence takes two 16-bit input values, x0 and x1. The actual input is a 32-bit value,
where x0 is [16;16], and x1 is [16;0].
FO then uses function FI (four SBOXes) to convert x0 to x0', and then x2=x1^x0'.
This repeats but with (x1,x2) then (x2,x3) to produce (x3,x4), the output of FO.
i.e.
FO(X) -> (x0,x1)=X, x2=x1^FI(x0); x3=x2^FI(x1); x4=x3^FI(x2); result=(x3,x4)

FO can therefore be performed with two parallel FI operations in one
cycle, and a third FI operation in the second cycle.

This implementation requires that the four SBOXes in FI can operate in
a single cycle, with some multiplexing and FL also. The key generation
is required to be one cycle ahead, so that round key generation does
not impact the critical path.

For even rounds the crypt function required is:
R <= L, L <= R ^ FL(FO(L))
Hence FO operates in its first cycle on the current data

For odd rounds the crypt function required is:
R <= L, L <= R ^ FO((FL(L)))
Hence FO operates in its first cycle on FL(current data)

In the hardware it is simplest to replicate FL for these two options, and multiplex between them.


Note:

If the two sboxes do run in a single cycle then the 8 rounds of Kasumi
take 16 cycles; sbox utilization is 2/3 (half used every cycle, the
rest on half the cycles). This is 4 bits of crypt per cycle.

If the two sboxes do not run in a single cycle then the 8 rounds of
Kasumi (for 64 bits of data) take 32 cycles; sbox efficiency is still
2/3. this is 2 bits per cycle.


Consider the operation of two rounds, an even round and an odd round
R'  <= L,  L'  <= [x3'.x4: x2=FL(L).1^FI(FL(L).0); x3=x2^FI(FL(L).1); x4=x3^FI(x2); x4'=x4^R.1; x3'=x3^R.0 ]
R'' <= L', L'' <= R' ^ FL([x3''.x4'': x2''=x4'^FI(x3'); x3''=x2''^FI(x4'); x4''=x3''^FI(x2'') ]
In parallel one can do FI(FL(L).0) and FI(FL(L).1)
Then in parallel one can do FI(x2) and FI(x3').
Then in parallel one can do FI(x4') and FI(x2'').

Using this method 2 rounds takes three cycles; four rounds of Kasumi
take 12 cycles, for 6 bits of crypt per cycle.

Yet another alternative would be to aim for only 1.5 bits per cycle,
mimizing the amount of silicon used; then one sbox7 and one sbox9
would be used.

The f8 mode of use of Kasumi is for key-stream generation, used to encrypt and decrypt.
It uses a feedback mechanism, using

  a = kasumi_cipher (count||bearer||direction||26b0) (key modified)
  generate_keystream 1 0

with
  
  generate_keystream n ksn =
     key_stream[n] = kasumi_cipher a^(n-1)^ksn key in
     generate_keystream (n+1) key_stream[n]

This mechanism means that the keystream cannot be generated in parallel - value N+1 depends on value N.

The key-stream generates is exclusived ORed with the plain text data (or cipher text) to encrypt (or decrypt)

The f9 mode of use of Kasumi is for authentication.

   generate_mac (0,0) auth_data||message||direction||1b1||padding

with

   generate_mac (a,mac) hd :: tl =
       a = kasumi_cipher (a^hd) key)
       mac ^= a
      generate_mac (a,mac) tl

The final mac is a kasumi_cipher mac (key modified)

So again the mac of word N+1 requires the mac of word N to be complete (which is expected for a mac)
