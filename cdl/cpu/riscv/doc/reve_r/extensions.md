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

## Multiply divide extension

The base RV32I instruction set does not include multiply and
divide. These are supplied by the RV32M instructions, which are
supported in the CDL RISC-V implementations with a configuration
constant in the instruction decode, and which require a companion
multiply/divide coprocessor. The provided implementation of that
coprocessor is 4-bits-per-cycle multiply and 1-bit-per-cycle divide
(with early termination) and supporting fused operations for full
64-bit multiplication result or quotient/remainder.


