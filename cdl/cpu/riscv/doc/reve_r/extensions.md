# Extensions

Part of the benefit of RISC-V's open instruction set is the ability
that this provides to hardware designers to extend the instruction
set; normally these additional instructions must be specially included
in code from hand-crafted libraries, but they may perform very
task-specific operations that would otherwise take the CPU many
cycles, or indeed not be possible.

## Extension mechanisms

The CDL RISC-V implementations allow for any decoder to replace the
standard instruction decoder modules; this is the most obvious way to
add additional instruction encodings. When this is done, there may be
a requirement to pass additional inforamtion with the instruction
decode: there is an extension structure that can be used in the
instruction decode for this purpose.

The pipeline control is not affected by the instruction decode
extensions, and indeed the rest of the change for instructions may be
even entirely within the ALU logic; for this purpose, it is best to
swap in a replacement ALU submodule.

If the instruction extensions are to change the control flow then this
can be handled again by changing the execution logic - perhaps by
reporting a branch unpredicted being taken.

Another potential extension mechanism would be different memory
accesses, which would require an extension of the data memory access
requests and associated logic.

Additional CSRs can be added by replacing the CSR module; this is
another common extension approach.

Finally, for larger scale extensions the CDL RISC-V has the concept of
coprocessors; these are modules that run in parallel with the
execution stages of the CDL RISC-V pipeline. They are described in
more detail in the *Coprocessors* section.

## Compressed instruction extension

The RV32C compressed instruction extension provides a parallel
instruction decoder to the RV32I decoder. It is normally instantiated
in all implementations, and if the logic is not required then its
outputs are zeroed out by a configuration constant. In this way the
logic of the decoder is not synthesised, and the cost to the design
is zero.

The compressed instructions, though, require a PC that can operate at
16-bit boundaries; there are various points in the pipeline and
execution stage logic that utilize the *is_compressed* field of the
instruction decode, or a configuration constant, to enable PC+2
operations.

## Atomic memory operations extension

The RV32A atomic memory instructions can be added to the standard
RV32I decoder, and disabled with a configuration constant if they are
not actually required to be supported. The only impact that these have
on the design is in the execution stage where it affects the data
memory access request that is presented.

## Bit mainpulation extension

There is no standard bit manipulation extension for RISC-V. There have
been a few attempts at adding bit manipulation, most notably in
Pulpino and by Clifford Wolf. These implementations supply some of the
same operations, but are not minimalist designs.

There will be a bit manipulation extension for the CDL RISC-V
implementation, supporting bit some shift extensions, rotate, and
count leading/trailing zeros, byte extract, byte swap, and bit swap;
possibly it will include pop count.

This extension will be an example of a configuration constant
extension, and it will be extending the instruction decode (for RV32I
only) and the ALU.

### ALU Shifter / Rotate architecture

The logic of a shifter is to, for each of 32 output bits, select one
of the 32 input bits, zero, or one. The amount to shift by is, in
RV32I, a 5-bit value indicating zero to thirty-one bits. There is no
way to shift by 32 bits or more.

A logical shift right by N sets output bit x to be input bit x+N for x+N<32, and
a value of zero otherwise.

An arithmetic shift right by N sets output bit x to be input bit x+N for x+N<32, and
a value of input bit 31 otherwise.

A shift left by N sets output bit x to be input bit x-N for x>=N, and
a value of zero otherwise. This may alternatively be viewed as N'=32-N
and output bit x to be input bit x+N' for x>=32-N'

Conceptually a shifter to implement all of these requires a rotate
right of an input I by a value N providing R and a mask generate for N
bits. The mask has the top N bits set.

Logical shift right by N is (R and ~mask).

Arithmetic shift right by N is (R and ~mask) | (I[31]?mask:0).

Shift left by N' uses N=32-N', with a result of (R and mask)

Rotation is very similar to shifting, but removing the masking. Hence
there is very little logic change to support rotation.

An extension of rotate right by N sets output bit x to be input bit
(x+N) mod 32. Rotate right by N is R.

An extension of rotate left by N sets output bit x to be input bit
(x+N') mod 32 where N'=32-N. Rotate left by N' uses N=32-N', with a result of R

### Byte and bit extraction

To extract a bit of byte can be performed with a right shift and an
and operation. This is two compressed instructions: shift left
immediate (if it is not the top bit/byte), and shift right immediate
by 31 or 24. There is little benefit, then to an extension for these.

### Replace bit or byte of RS2 with bottom bit or byte from RS1

This is a relatively complex operation for instructions, but simple
for the shifter architecture outlined above. The approach would be to
left shift RS1 by the correct amount, and generate the mask required
(top 32-N bits of 1). The final result is rotate output and mask and
mask<<(1 or 8) ORred with RS2 masked by the inverse of the combined
mask.

One difficulty with this extension is that the shift has to be an
immediate value, as RS2 is required. Hence this should use the SLL
instruction encoding, but with additional fields to indicate the shift
amount and size of the operation; this reduces the decode overhead.

This extension supports clearing a bit or a byte in RS2, if x0 is used
for RS1.

### Bit reverse, byte reverse, half-word swap

Endinanness conversion benefits from these instructions, which are
expensive otherwise. A swap-half-word instruction is RORI 16; the
others are more complex for coding.

A generalized reverse operation can swap nybbles or bit-pairs also;
this is of little use in general though (data is either big- or
little-endian formatted, rarely swapped only on a bit-pair boundary!).

Clearly, since the half-word swap is already supported, there is
commonality between the shifter and a byte reverser. This is because
the shifter is a mux tree.

The first stage of the shifter can be to mux the top and bottom
half-words of the data.

The second stage of the shifter is an 8-bit shift; this actually
byte-swaps byte 1 in to byte 0, and byte 3 in to byte 2; the other
bytes are not swapped for a byte reverse, though.

The bit-reverse operation then really replaces the last three stages
of the shifter tree, with an additional multiplexer. This can be
handled effectively as a replacement for the last level of the shifter
mux tree.

The cost of this implementation, then is to convert half of the second stage
shifter mux from two-input to three-input muxes, and convert the last
stage of the shifter mux from two-input to three-input muxes.

### Count leading/trailing ones/zeros

Count trailing ones/zeros is not required; this is covered by a word
reverse and a count leading.

Count leading ones/zeros/top bit is useful for floating point
conversion, compression, and other applications, yet is quite complex
for instructions.

### Population count

Counting the number of bits set in a register can be useful for parity
generation and so on, but has limited uses otherwise. This is seen to
not be a worthwhile addition to the instruction set - the cost to
logic is hundreds of gates, but with little if no benefit.

### Comments on Pulpino RI5CY extensions

The RI5CY instruction set includes instructions for arbitrary bit
length extract (signed and unsigned); arbitrary bit length insertion;
arbitrary bit length clear and set; find first set, last set, and
count leading bit; population count; rotate right (by register).

The Reve-R bit manipulation extensions do not support arbitrary bit
length extraction:
this requires two compressed instructions, and so is deemed to be not
worthwhile.

The Reve-R bit manipulation extensions do not support arbitrary bit
length insertion, but single bit or byte insertion only. This covers
the majority of use cases.

RI5CY leaves out byte swap and bit reverse, and rotate left.

### Comments on Xbitmanip draft (0.37)

The Xbitmanip draft (at 0.37) provides count leading/trailing zeros,
population count, shift ones in (rather than zeros or arithmetic),
rotate left/right, generalized reverse and shuffle, and arbitrary bit
extract and deposit.

It requires a considerable amount of silicon for this full feature
set; the comparison made is that it is equivalent to a 16x16 multiply
with 32-bit result - which can be considered to be, say, roughly 10k
gates (say). This is roughly equivalent to 10 times the size of the
standard Reve-R ALU.

### Instruction encoding for bit manipulation

The bit manipulation instruction extension is optional in Reve-R. If
it is not configured then there is should be no additional cost in the
logic. This benefits from a simple instruction encoding, using an
extension of the SLL, SRL and SRA instruction encodings.

These encodings require the top 7 bits (funct7) of the encoding to be
either 7b0000000 or 7b0100000. The base Reve-R must decode anything with
different values of funct7 to be illegal. The bit manipulation
extension removes this check (saving logic), and uses these bits for
the additional instruction encodings.

Note that the RV32M encodings use 'R' encodings for ALU operations
with funct7 7b0000001; hence it might be wise to utilizes the top 4
bits of f7 as a 'minor shift opcode', with 4b0000 and 4b0100 reserved
for SLL/SRL/SRA, and 4b0001 reserved for mul/div.

In this mode 4b1000 can be shift in ones (left/right depending on f3).
In this mode 4b1001 can be rotate (left/right depending on f3).
In this mode 4b1010 can be bit/byte/half swap (sll)
In this mode 4b1010 can be count leading bit (bit 31 of rs2) (srl)
(can do count leading bits count leading ones, with 1 inst)
In this mode 4b1100 can be replace byte (which byte in bottom 2 bits)
Does replace byte work with immediate? Normally that provides the
shift, but for this it would supply 12-bit immediate using f7, so that
does not work. Hence replace byte ONLY works in 'R' encoding (like
multiply).
This is a similar argument for count leading. It only works in 'R' mode.

Hence:
Shift left, shifting in zeros    - sll with funct7   of 7b0000000
Shift right, shifting in zeros   - srl/a with funct7 of 7b0000000
Shift right, shifting in bit[31] - srl/a with funct7 of 7b0100000

Shift left, shifting in ones  - sll with funct7   of 7b1000000
Shift right, shifting in ones - srl/a with funct7 of 7b1000000
 (was 7b1100000)

Rotate left  - sll with funct7   of 7b1001000
Rotate right - srl/a with funct7 of 7b1001000

Count leading bit - srl/a with funct7 of 7b1010000
Bit/byte/half-word swap - sll with funct7 of 7b1010000; half-word swap
if shift amount[4] is set; byte swap if shift amount[3] is set; bit
swap if shift amount[0] is set - so swap can be register or immediate

Replace byte 0 of RS2 with data from RS1 - sll with funct7 of 7b1100000
Replace byte 1 of RS2 with data from RS1 - sll with funct7 of 7b1100001
Replace byte 2 of RS2 with data from RS1 - sll with funct7 of 7b1100010
Replace byte 3 of RS2 with data from RS1 - sll with funct7 of 7b1100011

All bit manipulation extensions are SLL/SRA with funct7 top bit
set. They can also be used for up to 128 bit operations since the
bottom 2 bits of the f7 field for immediates is unused by then
encoding, and insert byte would require 4b110x which are all available
(to encode a 4-bit byte number). Also count leading bit can use bit 64
if a 64-bit SRL variant is used.

## Multiply divide extension

The base RV32I instruction set does not include multiply and
divide. These are supplied by the RV32M instructions, which are
supported in the Reve-R implementations with a configuration
constant in the instruction decode, and which require a companion
multiply/divide coprocessor.

The provided implementation of the multiply/divide coprocessor is
4-bits-per-cycle multiply and 1-bit-per-cycle divide (with early
termination) and supporting fused operations for full 64-bit
multiplication result or quotient/remainder. The gate cost is roughly
5k gates; faster or smaller implementations can be used directly
replacing the coprocessor, without affecting the processor pipeline
(the bare minimum might be about 2k gates, but an FPGA implementation
could use a hardware multiplier which would be faster with lower gate count).


