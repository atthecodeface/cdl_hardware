# Modes

A minimal RISC-V CPU implementation need only support the machine mode
of execution. Although it is not clear yet (there are no public
RISC-V platform specifications) the CPU must include a memory-mapped
timer peripheral that supplies a timer interrupt to the CPU.
Additionally the CPU must support illegal instruction, instruction
address misaligned and environment call from machine mode exception
traps.

## Rationale

Most CPUs support various operating modes or privilege levels. The
different privilege levels provide different degrees of system
accessibility: the highest privilege level provides full access to the
system. The ARMv7 architecture supports user, supervisor and
hypervisor privilege levels, for example; older architectures
supported just user and supervisor.

For deeply embedded systems the complete software stack may be able
to run at the highest privilege level - for example, it may be
operating the state machine for SERDES interfaces, in which case it
may only be running a few hundred instructions.

The current RISC-V privileged specification draft (v1.10) supports
three operating modes. The defined purpose of the modes is (very
broadly): user mode, for applications; supervisor mode, for the
operating system; machine mode, for making the hardware operate
cleanly and to provide (in software) features to lower privilege modes
that the hardware does not support. There is a notable lack of
hypervisor mode. The reasoning is that it should be possible to run a
guest OS in user mode; this may (re)appear in later versions of the
specification.

Another mode is described in the RISC-V specifications: debug mode;
this is required if an external debugger is to operate according to
the RISC-V standards.

The RISC-V specifications allow for an implementation to support just
machine mode; machine mode and user mode; or all three operating
modes. Debug mode can be added to any of these operating mode subsets.

The complete set of modes provided by a specific implementation
may vary according to the needs of the system into which the
implementation is placed.

## Machine mode

Machine mode is the most basic mode in a RISC-V CPU. It is required to
be supported in any RISC-V CPU, as it provides any abstraction
required for the hardware; some operations are only permitted in
machine mode. It can be viewed as the 'bare metal' mode of operation
of the CPU.

Machine mode must provide exception handling and appropriate registers
to enable this; these are defined by the RISC-V specifications to be
CSRs. There are then a few privilege mode instructions for software
exception handling (invocation and return).

Machine mode is obliged to handle (in some manner) most processor
exceptions. These include illegal instructions, page faults, access
faults, and so on.

One of the features of machine mode is to enable support for standard
software operation with hardware that does not provide a complete
implementation; hence it is possible for a RISC-V CPU implementation
to not include hardware suport for multiply or divide instructions,
but to provide that capability in machine mode software by trapping
such instructions and executing the behaviour in, effectively,
microcode. Similar areas of functionality cover support for unaligned
load/store transactions and software page table walking.

## User mode

On an embedded CPU, with no need for anything other than basic CPU
operation, machine mode is all that is required. For embedded CPUs
where some form of protection is required it may be handy to also have
user mode; this allows for some software to be written as simple
applications, while the real-time embedded system runs in machine mode
underneath.

Hence user mode provides a minimum privilege level of operation. In
essence it requires no CSRs to operate; some instructions that are
legal in machine mode become illegal in user mode. To invoke machine
mode code from user mode (for example, to ask the real-time subsystem
to interact with hardare) there is a mechanism for an exception call
(the *ECALL* instruction).

The RISC-V specification also has a draft to define user mode
interrupts; this further enhances user mode with the ability to enable
and disable various interrupts using a few CSRs. This provides a very
simple user application model with a real-time machine mode, where the
user mode still needs to support timers and some hardware
interaction. The user mode interrupt routines can interrupt user
applications, but at any point the machine mode may take an interrupt
at a higher priority level.

## Supervisor mode

Supervisor mode is an intermediate privilege level between user mode
and machine mode. Until the CDL RISC-V implementations support it,
though, the reader should look at other documents to find out more.

## Debug mode

Debug mode is the highest privilege mode in RISC-V, but it is not
meant to be used as an operating mode. It enables support for
debugging software (of any operating mode).

To support debug mode an implementation must have a few extra CSRs -
when debug mode is entered, for example, the program counter of the
next instruction and the CPU operating mode must be preserved, and for
this purpose there are the *DPC* and *DCSR* registers.

In general debug mode can only be entered by hardware mechanisms: a
hardware breakpoint, or a debugger halting the RISC-V hart.

## Implementation

The CDL RISC-V implementations currently support just debug and machine modes; in
the very near future it will cover also user mode.

The impact of supporting the additional modes is relatively
light. Each mode requires some more CSRs, and the transitions between
modes have to be handled by the pipeline control. There is a fair
degree of complexity in the specification for the interrupts and
exception delegation, which affects this.

The support for various modes can be configured in the compilation of
the CDL.

The implementation impacts of the modes are that the pipeline
execution has to operate in a privilege mode. To this purpose the
pipeline control state machine maintains the knowledge of the current
privilege mode for the hart; when a mode change is required the
pipeline control has to flush the pipeline and any instruction fetch,
and restart the pipeline with a new fetch request in the new privilege
mode.

To support debug mode the pipeline control also interacts with a debug
target state machine; the pipeline can be halted and resumed, and when
halted the pipeline control can be forced to run the pipeline with
debug instructions.

