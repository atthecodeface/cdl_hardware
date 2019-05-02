# Pipeline implementation


Probably this has two subchapters, for different pipeline lengths.

Pipeline control should be in a different chapter.

## Pipeline control

The pipeline control is implemented in the pipeline control state
machine and various other combinatorial modules.

Pipeline control is formed from two parts that are somewhat distinct: 
instruction fetch request generation, which uses the current fetching
CPU mode, PC, and decode output (for branch prediction etc);
synchronous and asynchronous exception control and pipeline
blocking. The latter is effectively the execution control flow, and
the former is a feed of the pipeline.

The state of the pipeline control is where these two parts merge. This
has a state machine that will normally continue to fetch instructions
using the instruction fetch generation; when a trap occurs, though, it
will move to a state that that flushes the pipeline and restarts the
fetch at the new PC.

## Trap interposer

The trap interposer is responsible for determining whether and which trap is
to be taken. It operates very early in the clock cycle.

Memory access valid and abort (causes memory access exception, PC of
the memory access stage; only if so configured).
If the memort access abort is configured then it may be configured for
first cycle of memory access only, or for any cycle of access (using
the access_complete to terminate memory access cycles). If it
is configured for any cycle then a subsequent exec instruction must be
blocked until the access is valid.

Interrupt (not if exec is valid and blocking interrupts -
i.e. multicycle that has already started)

Exec instruction illegal or fetched invalid

Exec mret, ecall, ebreak

## Control flow interposer

The control flow interposer determines which stages of the pipeline
should be blocked, flushed, or permitted to move on. It operates late
in the cycle. As part of this it will kill data memory accesses or
coprocessor starts.
Some of its outputs go to the data memory access, CSRs
and coprocessors. These modules must only use the control flow
interposer outputs to gate registers and clear valid signals (on flush).

A memory stage trap is always taken; it flushes the pipeline up to an
including the exec stage, and invalidates thw memory stage.

An exec stage trap is taken if the memory stage is invalid, or if the
memory stage is not trapping or aborts are configured for only the
first cycle of a memory access. This includes interrupts. Hence an
exec stage trap is not taken (including interrupts) if the memory
stage access is valid and abort is configured to be permitted on any
memory access cycle.

The exec stage instruction is blocked from starting:
if the memory access stage is valid and it is not completing and abort
is configured to be permitted on any memory access cycle

The exec stage instruction is blocked from completing:
if the memory access stage is valid and it is not completing

JALR or mispredicted branch

