# Exceptions and interrupts

Clearly a bare minimal RISC-V CPU implementation must provide interrupts,
exceptions and CSRs. This is a more complex implementation than a very
simple embedded controller would require, but it supplies a baseline
for the CDL RISC-V implementations.

## Synchronous exceptions

One can view the exceptions that occur during instruction execution as
synchronous exceptions. They will occur at the same point in the code
independent of external timing.

The first source of synchronous exceptions is illegal
instructions. These exceptions occur at the commit stage of the
pipeline, which for the CDL RISC-V implementations is the execution
stage. The instruction may be illegal because it is misaligned; it had
a fault (access fault or page fault) on instruction fetch; it decodes
to an illegal action (or is just not a legal decode).

Instead of an illegal instruction detection the instruction might be
an explicit synchronous exception - an environment call or breakpoint.

The second source of synchronous exceptions is from data memory
accesses; an access may be miasligned, or it may have fault (access
fault or page fault). In the CDL RISC-V architecture this detection
occurs in the data memory response stage of an instruction execution.

## Asynchronous exceptions

Interrupt support is required by the RISC-V specification; these are
asynchronous exceptions. They are handled in decreasing priority order
of: external interrupts, software interrupts, timer interrupts.

## Exception processing

The second source of synchronous exceptions has to have the highest
priority in the CDL RISC-V implementation, as these exceptions occur
after the commitment point for the instruction execution.

The privilege specification then indicates that all synchrous
exceptions are the lowest priority; for the CDL RISC-V implementation
this means that the interrupts have second priority after the data
memory access stage exceptions.

Finally, the lowest priority is the first source of synchronous
exceptions.

## Implementation

The pipeline control handles exceptions by combining the state of the
pipeline stages (specifically the execution and memory access stages)
with response from the CSR module, data memory access response and
coprocessor responses.

If the memory access stage has a transaction in progress and the data
memory access response indicates (ideally early in a cycle) an abort
is required, then the instruction at the memory access stage must
abort (and be flushed) and the execution stage (and earlier stages)
must be flushed; the execution
stage is also indicated as cannot start and cannot complete.. The PC of the
instruction must be stored in the appropriate (based on delegation!)
exception PC, and appropriate value and cause set. This operation
looks fairly long on paper, and so should be implemented by a first
cycle generating the exception and a second cycle updating the CSRs.

If the memory access stage does not abort and the execution stage is
in its first cycle (i.e. has not committed to starting) then an
interrupt may be taken. The logic for determining this operates on the
CSR state and pending interrupt state in registers (i.e. pending
interrupts are not determined in a prior cycle). An interrupt causes
the execution stage (and earlier stages) to be flushed; the execution
stage is also indicated as cannot start and cannot complete.

If the memory access stage does not abort and an interrupt is not
taken then the execution stage may, if it is in its first cycle *and
the memory access stage is empty or will complete*, abort with an
exception. This forces a flush of the execution stage (and earlier
stages) to be flushed.

In the CDL RISC-V implementation, the pipeline control flow module
implements the exception detection logic. The pipeline control state
machine has to handle the update of the CSR state due to the
exception.

## Interrupt and Exception Delegation

Interrupts and exceptions are complicated by the RISC-V concept of
*delegation*. This is a mechanism that permits the machine mode of the
RISC-V hart to delegate handling of any interrupt or any synchronous
exception to a lower privilege level.

When running in a particular mode the CPU can determine which mode
(which will be a higher-or-same privilege level) any synchronous
exception should be taken in.

If in machine mode, all synchronous exceptions are taken in machine mode.

If in supervisor mode, all synchronous exceptions are taken in machine
mode unless the correspong bit of *medeleg* is set; hence the
exceptions taken in supervisor mode are those marked in *medeleg* and
those taken in machine mode those marked in the negation of *medeleg*.

If in user mode the logic is: the exceptions are taken in user mode
are those marked in *medeleg* AND *sedeleg*; those taken in
supervisor mode are those marked in *medeleg* AND negation of *sedeleg*;
those taken in machine mode those marked in the negation of *medeleg*.

If supervisor mode is not supported then *sedeleg* is assumed to have
all bits set in the above logic.

Interrupt sources:

MTIP and MEIP are from pins; MSIP is externally written if supported.

STIP is a CSR bit, written by machine mode.
SSIP is a CSR bit, written by machine mode or supervisor mode.
SEIP is a CSR bit, written by machine mode, that may be ORred with an external
supervisor-mode interrupt pin for the actual interrupt generation

UTIP is a CSR bit, written by machine mode.
USIP is a CSR bit, written by any mode.
UEIP is a CSR bit, written by machine mode (or supervisor mode?), that may be ORred with an external
user-mode interrupt pin for the actual interrupt generation

A machine interrupt pending (MIP) is asserted if MTIP&MTIE or MSIP&MSIE or
MEIP&MEIE

If in machine mode a CPU takes a machine interrupt if MIP is set and
MIE is set.

If in supervisor mode a CPU takes a machine interrupt if MIP is set,
independent of MIE, UNLESS *mideleg* has the relevant bit set.

If in supervisor mode a CPU takes a supervisor interrupt if MIP is
set, SIE is set, and *mideleg* has the relevant bit set, and *sideleg* has
the relevant bit clear.

If in user mode a CPU takes a machine interrupt if MIP is set,
independent of MIE, UNLESS *mideleg* has the relevant bit set.

If in user mode a CPU takes a supervisor interrupt if MIP is set,
and *mideleg* has the relevant bit set, and *sideleg* has
the relevant bit clear.

If in user mode a CPU takes a user interrupt if MIP is set,
UIE is set, and both *mideleg* and *sideleg* have the relevant bit set,

Interrupt user mode to user mode when (mideleg&sideleg&mip!=0)&UIE

Interrupt user mode to supervisor mode when (mideleg&~sideleg&mip!=0)

Interrupt user mode to machine mode when (~mideleg&mip!=0)

Interrupt supervisor mode to supervisor mode when (mideleg&~sideleg&mip!=0)&SIE

Interrupt supervisor mode to machine mode when (~mideleg&mip!=0)

Interrupt machine mode to machine mode when (~mideleg&mip!=0)&MIE

An alternative way to view this is:

Interrupt to machine mode when (~mideleg&mip!=0)&(MIE || mode is S/U)

Interrupt to supervisor mode when (mideleg&~sideleg&mip!=0)&(SIE || mode is U)

Interrupt to user mode when (mideleg&sideleg&mip!=0)&UIE


An interrupt to machine mode takes precedence over an interrupt to
supervisor mode, which again takes precedence over an interrupt to
user mode.

When an interrupt is taken the cause is the highest bit number which
can have caused the interrupt.


For interrupts the logic is the same except the *mideleg* and
*sideleg* registers are used. However, 

## Implementation

The CDL RISC-V implementations perform exception processing in the
pipeline control flow module.

The memory access stage exceptions are determined from the instruction
in that stage being valid and performing a memory access, and
combining this with the data memory access response.

...

CSRs

...

