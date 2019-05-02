# Coprocessors

Coprocessors may be added to execute in parallel with the execution
stage of a CDL RISC-V implementation.

Caveat: currently only fully pipelined processors operate with
coprocessors. This is due to implementation time and regression test
capability.

The concept behind the CDL RISC-V coprocessors is that they receive
the instruction and data that the execution unit does, and they
perform an operation whose result is returned to the execution unit -
effectively they appear as a combinatorial operation on 32-bits of rs1
and rs2 data producing a result. However, the coprocessor can take
multiple cycles to operate, and so it may indicate to the pipeline
control that it has started execution but that it has not completed.

An example of a coprocessor is the multipy/divide unit; this utilizes
the instruction decoder to decode the instructions, and it takes the
decode to operate a state machine that performs a 4-bit-per-cycle
multiply or a 1-bit-per-cycle divide. The logic in the coprocessor is
optimized for die area, and the data pipeline for multiply and divide
is common. The coprocessor can also perform fused operations: these
are, for example, where two 32-bit numbers are multiplied and the
full 64-bits of result are required; two successive instructions of
the right form allow the first to do the full multiply (returning half
the result) while the second can then complete in a single cycle
(returning the other half of the result). In order to achieve this the
coprocessor requires a 'look-ahead' at the next instruction to be
executed - i.e. it needs a decode stage that is valid while the
current instruction is in the execute stage.

The coprocessor can also indicate that it is not ready to even *start*
an instruction; this may be because its resources are otherwise
busy. In this case the pipeline control can continue to try to execute
the instruction in the next cycle. Unlike an inability to complete,
though, the inability to start permits the pipeline control to
*interrupt* the instruction execution (flushing the instruction in the
execution stage). This is a better method of holding execution from a
coprocessor if the reason that the coprocessor cannot execute is due
to external signals.



