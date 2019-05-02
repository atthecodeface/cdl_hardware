[header_comment]: # (This files is written in Markdown; it may be
compiled to PDF using, for example, pandoc file.md
--pdf-engine=pdflatex -o file.pdf; however it should be
readable in text form)

---
Title: book
documentclass: book
author: "Gavin J Stark"
---

# Overview

The RISC-V implementations here were originally designed to
investigate the future development of the CDL language; to achieve
this goal they have to pass regression tests for RISC-V, and cope with
being targeted at silicon implementation (through verilog/synthesis),
FPGA implementation (again through verilog/synthesis), and C-based
simulation.

Part of this original goal was to provide for a range of pipeline
depths and resultant silicon costs, and to also provide for
enhancements by replacing modules and overriding default type
structures with enhanced type structures (for example in the
instruction decode/ALU) to allow enhancements which require multiple
submodule changes. In a more modern language these features would be
handled with parametrized types, polymorphic modules, and type
classes.

Since the original implementations were completed, the goals have
grown somewhat; this has encouraged a slightly more structured
approach to the implementation, which leads to this more structured
documentation.

This document, then, is an implementation specification which is
driving the final pipeline implementation.

# Pipeline architecture

The basic architecture of the pipeline for the RISC-V implementation is
fetch, decode, register file read, execute (ALU + memory request),
memory access, and register file write. There are, initially, three
interfaces to the pipeline: instruction fetch (request and response);
memory operation (request and response) and instruction
commit/flow/completion (for trace).

![Pipeline](pipeline.svg "Pipeline"){ width=80% }

## Architecture Overview

The RISC-V implementation is architected around the concept of a
processing pipeline that may be broken into different stage lengths:
one implementation may have decode, ALU, and memory access all on a
single cycle, while another may have them in separate cycles.

A simple CPU pipeline has to fetch instructions, decode, read register
files, perform an ALU operation or determine branching and control
flow, start memory transactions, receive results from memory
transactions, and update the register file. In addition to this
processing pipeline there is a need to control the pipeline - to
determine what program counter to insert into the fetching logic, to
flush pipeline stages on control flow changes, to support debug, and
to handle exceptions (memory aborts for example) or interrupts.

The CDL hardware design language has what some people believe is a
flaw, in its C model generation backend; this is the feature where the
logic in a module can have a path that is combinatorial from input to
output, but the module cannot have two such paths that would operate
at different stages of a clock cycle (one early, say, and one late in
the cycle). This means that a CDL design module must have, if it has
combinatorial paths, a defined point in the clock cycle where it is
expected to fit. This 'flaw', though, helps enforce a flow of
architecture where each step with a clock cycle is bounded; it means
that the architecture for the RISC-V implementation is built around
discrete processing steps with pipeline control and the pipeline being
managed explicitly.

The architecture of the implementation of the RISC-V can then be
discussed by looking at the steps involved in the pipeline, and
separately looking at the pipeline control.

## Fetch stage

The fetch stage - also known sometimes as the prefetch logic -
provides the flow of instructions to the pipeline, in response to
fetch control information from the pipeline control.

Unlike the other pipeline stages the fetch stage is not supplied as
part of the pipeline code. This is because the fetch stage is very
dependent on the system that the pipeline froms part of.

The fetch stage may contain buffering for future instruction fetches,
by reading ahead in a memory. This is made simpler to use with the
fetch requests indicating whether they want sequential instruction
data, for example. If the fetch stage does contain this buffering then
there is a requirement that it be flushed on an appropriate memory
fence instruction - so that just-in-time compiled code may be used,
for example.

In simple implementations the fetch stage can use an asynchronous SRAM
to read instructions directly from the address provided in a fetch
request. Other simple implementations can use a synchronous SRAM with
a multi-cycle CPU clock - reading the SRAM in the second sub-CPU clock
cycle, for example. For a high speed but simple implementation the
fetch logic can use a registered version of the requested address and
only provide valid data if a retry or sequential fetch are requested.

### Fetch request

The pipeline control supplies the fetch control information, within
the *t_riscv_fetch_req* structure. This requires the following
elements:

flush (bit)
:  Indicates that any prefetch requests and data should be flushed;
   this can happen in response to a memory fence instruction, for
   example.
   If this is asserted then no instruction fetch will be requested in
   the same cycle.

mode (*t_riscv_mode*)
:  The mode of the code performing the fetch

req_type (*t_riscv_fetch_req_type*)
:  The kind of request required in this cycle - none, nonsequential,
    repeat, or sequential

address (32-bit)
:  The address to be fetched; valid for every non-none request, but it
    may arrive later in the cycle, so in some implementations it may
    only be utilized after being registered. For RV32IC the address
    may be half-word aligned, in which case the resulting data must be
    the instruction starting at that alignment; if the pipeline
    implementation does not support compressed instructions, though,
    the address will always be word aligned.

The *t_riscv_fetch_req_type* enumeration includes

* rv_fetch_none: address is invalid and flush may be asserted

* rv_fetch_nonsequential: address is unrelated to previous cycle
  address
  
* rv_fetch_repeat : address is same as in previous cycle

* rv_fetch_sequential_16: address is 2 bytes on from previous cycle

* rv_fetch_sequential_32: address is 4 bytes on from previous cycle

### Fetch response

In response to a fetch request, the fetch stage *must* provide a
response. If it cannot provide valid fetch data, then it can indicate
this with a *valid==0* response; there will be a bubble in the
pipeline. It may provide errored fetch data: for example, if the mode
of the fetch did not have sufficient privilege; if the data fetched
had an uncorrectable ECC error; if the memory at the address requested
does not exist. For valid data a complete 32-bit data word must be
returned.

The *t_riscv_fetch_response* structure has, then, requires the following
elements:

valid (bit)
:  Asserted to indicate the remaining fields have valid data; if
   deasserted then the pipeline will have a bubble inserted into it.

error (bit)
:  If asserted then the fetch had an error, and the error type will
   indicate the error type

error_type (*t_riscv_fetch_error_type*)
:  The kind of error in the fetch; ignored if valid or error are deasserted.

data (32-bit)
:  The data fetched. All 32 bits must be valid.

## Decode Stage

The decode stage in the pipeline requires a registered instruction
word, that will have been fetched in the previous cycle.

The decode stage provides outputs to the following stage and pipeline
control based solely on its registered state.

The decode should decode that registered instruction word, and present
the internal decode. It may utilize more than one decoder for this
purpose: there are implementations provided of rv32i, rv32ic, and one
for debug. If a pipeline implementation does not require compressed
instruction support then the compressed decoder need not be
instantiated - or its outputs can be zeroed out, and synthesis will
remove it from the final hardware.

The decoders may support the A- and M- variants (and others!) of the
RISC-V instruction set; the standard implementations can be replaced
with additional custom decoders, or custom instructions can be enabled
in the standard implementation.

The result of the instruction decode includes the length of the
instruction decoded: it may be 16-bit or 32-bit. The reality is that
this decode is very simple, and it should be very few gates. The
result of this decode feeds out to the pipeline control, which can use
it to determine the next instruction fetch request (as sequential
16-bit or 32-bit).

The decode also can supply a branch target (for branch instructions or
JAL instructions) with a branch prediction hint; this can be used by
the pipeline control to present a nonsequential fetch request of a
branch target - where the address will be later in the cycle than the
control signals.

The pipeline control indicates to the decode stage whether it: must
flush - in which case it invalidates its instruction store; is
blocked - and if so, it should not register a new instruction in;
should take any new instruction data in (if valid).

### Decode stage data for pipeline control

The decode stage reports to the pipeline control using the
*t_riscv_pipeline_response_decode* structure:

valid (bit)
:  Asserted to indicate the remaining fields have valid data. If the
    decode instruction register is invalid, this should be low; else this
    should be high

pc (32 bits)
:  PC of the instruction being decoded - this is used to create the
    correct address for sequential accesses

enable_branch_prediction (bit)
:  Deassert this is the branch_target is not valid; this is in general
  a configuration / implementation bit, and is not generated from state.

branch_target (32 bits)
:  This contains the target of a branch, if it would be predicted; if
    branch prediction is not enabled then this is ignored. For
    implementations that use branch prediction and the *address* field of
    the instruction fetch request in the cycle of a fetch this will be
    on the critical path.

idecode (instructon decode)
: The 'is_compressed' field of the decode is used to determine a
    sequential fetch request type; the 'op' and top bit 'immediate'
    field may be used to predict branches (for an idecode.op of
    'riscv_op_branch'); the rest of the decode may be required if
    pipeline coprocessors are provided - but the pipeline control does
    not use these fields

*Note that the use of idecode by pipeline_control may be removed; 
 'backward branch predict' and 'is_compressed' may be added to the
 response structure instead.*

## Register file read

The register file read takes the decode of the instruction and
combinatorially reads the register file.

RISC-V instructions require two read ports on a register file - one
for Rs1 and one for Rs2. In RV32I these are 32-bit registers, and the
simple implementation in the CDL is a flop-based register file so
register file read becomes a set of multiplexers.

In silicon and FPGA implementations, given the RISC-V decode logic,
there is no point having a dedicated pipeline stage for register file
reading; hence there is no provison for registering in this area.

## Execution stage

The execution stage of the pipeline is responsible for gathering input
data for the relevant units, and evaluating results and launching data
memory requests.

It may start with a register stage, which holds the register file read
results and decoded instruction; if this register does not exist in an
implementation (for a slower clock speed, smaller design) then it
takes data directly from the decode and register file read stages -
without any influence on those inputs from the pipeline control.

The first step in the execution stage is to determine if the
instruction execution can start; in a design with separate execution
and memory access stages the execution stage must wait for the memory
access to complete if the instruction requires that data: for example
with an add following a load instruction. This dependency only exists
if the memory access would update a register that is used in the
execution stage as a source register.

The next step is to forward any data for the Rs1/Rs2 fields from
previous cycles; the tracking of forwarding requirements can be
handled in the state registers for the execution stage, but the
implementation requires the actual forwarding to occur at the start of
the execution.

The execution stage reports, based on its state (and potentially state
from the decode stage, for pipelines with fewer registered stages) the
dependency on further (i.e. the memory access) stages to the pipeline
control. It also reports whether it has started (and committed) to
executing the current instruction - some instructions may be
multicycle, and once started they are committed. An example is an
unaligned memory read, which may become two individual memory
accesses; another is a multiply instruction (implemented in a
'coprocessor').

The execution stage can perform any required arithemetic operation,
logical or shift operation, and it can generate the data memory
access request address. This access request is again presented to the
pipeline control logic - and again, from state only, not based on any
inputs from the pipeline control. The pipeline control is responsible
for killing a data access request if the execution stage is blocked,
or if the pipeline control wishes to take a trap (exception or
interrupt).

The execution stage reports out any required CSR access (which may be
a read, or read-write, or write). The CSR logic (external to the
pipeline) must perform the CSR read and present a response.

A mispredicted conditional branch or a JALR instruction require the
execution stage to report out to the pipeline control for a change in
the control flow. The JALR instruction requires the
*pc_if_mispredicted* to contain the result of the ALU arithmetic
operation; a condtional branch should contain the correct branch
target or PC plus either 2 or 4.

Toward the end of a cycle - i.e. in response to coprocessor result
data and csr result data, the execution stage can multiplex result
data to generate the result of the execution stage operation.

Finally the execution stage can update state - based on its data and a
final late input from the pipeline control, which can: flush the
execution stage; block the execution stage; permit it to move forward
(which may just be move on to the next cycle of execution, rather than
completing execution).

External to the pipeline the CSR access completes if the pipeline
control permits it; similarly a data access request will be started
if, again, the pipeline control permits.

### Exec stage data for pipeline control

The exec stage reports to the pipeline control using the
*t_riscv_pipeline_response_exec* structure:

valid (bit)
:  Asserted to indicate the remaining fields have valid data. If the
    exec stage data is invalid, this should be low; else this
    should be high

pc (32 bits)
:  PC of the instruction being executed - this is used by the pipeline
    control in recording the next instruction PC for traps.

first_cycle (bit)
:  Asserted if the execution stage has not yet committed to execution;
    most instructions are only a single cycle, so this is asserted most of
    the time. However, a multi-cycle memory access (for unaligned memory
    transactions) or coprocessors that take many cycles will have this
    asserted from the first cycle after execution is committed

start_depends_on_mem_access (bit)
:  Asserted if execution start cannot occur if the memory access stage is
    valid. This must only be asserted if first_cycle is asserted.

branch_taken (bit)
:  Asserted if a branch is being taken; if
     *start_depends_on_mem_access* is asserted then this must be
     ignored if the memory access stage is valid.

jalr (bit)
:  Asserted if the instruction is a JALR instruction; if
     *start_depends_on_mem_access* is asserted then this must be
     ignored if the memory access stage is valid.

predicted_branch (bit)
:  Asserted if the instruction at decode predicted a branch; this must
    be set in the state for the exec stage if the decode predicted a
    branch *AND THE PIPELINE CONTROL USED THAT PREDICTION*

pc_if_mispredicted (32 bits)
:  Reports the PC for a mispredicted branch; this must contain the
    target for a JALR instruction, for conditional branches it should
    contain either PC+2/4 or the branch target, depending on whether a
    branch was predicted and whether it was taken; for a JAL
    instruction it should contain the target.

rs1 (32 bits)
:  The value of rs1 being used by the execution stage; this is
    provided to feed coprocessors, not for the pipeline control

rs2 (32 bits)
:  The value of rs2 being used by the execution stage; this is
    provided to feed coprocessors, not for the pipeline control

idecode (instruction decode)
:  The instruction decode of the instruction bein executed,
    provided to feed coprocessors, not for the pipeline control

*Should have a 'last of instruction' indication - or continuation required*

*Need trap and ecall and ret invocation* - currently this uses idecode

*Pipeline control in needs to provide indication of decode instruction
 being a predicted branch, if not blocked*

### Exec stage control from pipeline control

The pipeline control can: flush the execution stage; block the
execution stage from completing its stage; block a data memory access;
permit execution to complete and take decode; it needs to take the
decoded instruction and record if it is a predicted branch or not

## Memory access stage

The memory access stage of the pipeline is responsible for handling
the response for data memory transactions; it can handle data access aborts (if
the data memory provides such ability) and it processes any returned
read data. For instructions that require no memory access then the
stage does nothing.

It may start with a register stage, which holds the ALU result and
controls for its operation.

It takes any response from the data memory - which may be fairly late
in the cycle - and it combines read data to rotate it and sign extend
for a memory result.

The final instruction result can be multiplexed and stored in the
register file.

### Memory access stage data for pipeline control

The memory stage reports to the pipeline control using the
*t_riscv_pipeline_response_mem_access* structure:

valid (bit)
:  Asserted to indicate the remaining fields have valid data. If the
    memory acces stage data register is invalid, this should be low; else this
    should be high

pc (32 bits)
:  PC of the instruction with a memory access; the pipeline control
    can use this for recording data memory access abort exception data.

access_in_progress (bit)
:  Asserted if the execution stage issued a data memory access, and so
    the memory access stage data corresponds to a response from the
    data memory.

### Memory access stage control from pipeline control

The pipeline control can: flush the memory stage; block the memory
stage; permit it to take the execution stage output.

## Register file write stage

In a pipeline implementation that uses latches for register files
there can be a need for the write to take place in a register file
write stage. However, even in cases without an RFW stage the RISC-V
CDL pipeline architecture has a register file write stage to record
the data that has just been written to the register file and to record
other information - this can be used for tracing instruction execution

# Pipeline implementation

## Stuff

### Debug master request

The debug master request *t_riscv_debug_mst* structure:

select (bit[6])
:  Hart(s) to select


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

# Interrupt and Exception Delegation

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

# Pipeline control

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

# Debug infrastructure

The RISC-V debug specification is not approved as of Jan 2019. The
architecture of the debug, though, is probably not going to change.

## RISC-V debug specification

The RISC-V debug infrastructure starts at the CPU itself. To support
debug a *debug* execution mode is really required; this is a higher
privilege level even than machine mode. It requires special CSRs that
record the state of the CPU when a debug exception occurs. A debug
exception can be a halt due to debugger request or a breakpoint (of
some form). These CSRs include the *dpc* CSR, which records the
program counter of the instruction that would have been executed if
the CPU had not halted.

At its most basic, the debugger system can resume and halt a CPU. When
halted it may interrogate and set register and CSR state. It may also
execute very small programs - again, the most basic is a single
instruction. Note: somewhat surprisingly, this single instruction can
(according to v0.13 of the specification) be a jump or branch
instruction, which may then be expected to be followed and the
remaining code executed; the program supplied by the debugger is
expected to have an explicit breakpoint instruction in it to halt
execution, although this may be an 'implicit' explicit breakpoint if
the debug module only supports a single 32-bit debug program buffer.

With this infrastructure the debugger can halt the CPU; read all the
register and CPU state; read memory and I/O (by setting registers and
executing 'load' instructions). It may then update any state also, and
it can resume execution. This provides for pretty much any debugger
requirements.

## RISC-V debug architecutre

The RISC-V debug specification defines a *Debug Module* (DM) that interacts
with one or more RISC-V hardware threads (harts); this is specified to
be an I/O peripheral that has a specific register set and
operation. The interaction between the DM and the RISC-V hart is not
defined by the specification - that is purely implementation
dependent.

The DM's bus is called the *Debug Module Interface* (DMI); this is
again not defined, but an APB interface it is identified in the
specification as one possible implementation. It must have
address/data/read/write semantics. It must be connected to a *Debug
Transport Module* (DTM). This module provides a mapping from (for
example) USB or JTAG to the DM register interactions.

## CDL RISC-V debug architecture

The CDL hardware design repository provides a JTAG TAP controller
harness and an APB master JTAG TAP controller that conforms to the
JTAG DTM specified in v0.13 of the RISC-V debug specification. This
provides for a JTAG DTM with an APB as the DMI.

The CDL RISC-V debug arcthiecture must therefore supply a *Debug Module* (DM) which
has an APB interface; the approach of the architecture is to support
many RISC-V cores simultaneously, and so the DM needs an interface to
individual RISC-V harts that supports the
halt/resume/read/write/execute semantics required by the RISC-V debug
specification; it also requires a multi-target bus to report back
status of every hart.

The approach taken in the CDL RISC-V debug architecture is to have a
debug request
*t_riscv_debug_mst* bus that is driven by the DM, and which can be
pipelined as required to harts (with a requirement that the same depth of pipelining
is used for different harts). This bus has two purposes: the first is
to permit polling of up to 64 harts for status; the second is to
permit debug operations to be invoked.

The status of harts is interrogated using a 6-bit mask/select system;
when a hart receives a debug request which selects it, then it may
drive the response bus (a *t_riscv_debug_tgt*) on the next cycle. The
information on that bus includes status such as *halted*, *resumed*,
and *hit_breakpoint*. When a hart is not selected in a cycle it must
drive its debug response bus low.

The debug response buses from the harts may be wire-ored and pipelined
back to the DM; the pipeline depths from all harts must again be the
same (so that the select/respond operation requires no
acknowledgements).

The DM normally slowly polls the harts for their status; it will (when
idle) run through select/mask values to test all the harts that it is
configured to know about.

However, to improve performance on systems with many harts, a hart may
request attention. For this purpose there is a *attention* bit in the
debug response bus. This is again wire-ored back to the DM. When the
DM sees the attention bit high it can poll the harts faster, and it
may intelligently select for polling any hart that it has requested an
operation for (since they are more likely to need attention). The DM
could utilize a divide-and-conquer approach to polling (by using
masking of the selects) - but the current implementation always uses a
mask of all 1s.

To invoke an operation in a hart the DM drives the debug request bus
with the desired select and a mask of all ones; it also sets a *valid*
bit and specifies a *t_riscv_debug_op* debug operation to perform
along with a 16-bit argument and 32-bit data word. The possible
operations include: set requests, providing the ability to set the
request for halt, resume, step; read and write, to read and write GPRs
and CSRs; and execute progbuf, to execute an instruction provided by
the 32-bit data word.

### Debug master request

The debug master request *t_riscv_debug_mst* structure:

select (bit[6])
:  Hart(s) to select

mask (bit[6])
:  Mask of hart(s) to select - all ones means a specific hart is selected

valid (bit)
: Asserted if op is valid; has no effect on mask and attention

op (*t_riscv_debug_op op*)
:  Operation for selected PDM to perform

arg (bit[16])
:  Argument for debug op

data (bit[32])
: Data for writing or instruction execution

### Debug master request operation types (*t_riscv_debug_op*)

rv_debug_acknowledge
:  Acknowledge halt, breakpoint hit, status; removes attention
    signal. In fact this is used for any simple polling request
    
rv_debug_set_requests
:  Make hart set request bits for halt and resume

rv_debug_read
:  Request the hart read a GPR/CSR; the *arg* field indicates which
   register

rv_debug_write
:  Request the hart write a GPR/CSR; the *arg* field indicates which
   register, and the *data* field is the data to write

rv_debug_execute_progbuf
:  Request the hart to execute the instruction provided by *data*


### Debug target response

The debug target response (*t_riscv_debug_tgt*) structure:

attention (bit)
: Asserted by a hart while it has unacknowledged change in halted,
    resumed or  breakpoint hit status.

valid (bit)
:  Asserted if the response is being driven; if this is low, all other
   bits should be low except *attention*

selected (bit[6])
:  Number of the hart driving the bus

halted (bit)
:  Asserted if the selected hart is halted 

resumed (bit)
: Asserted if the selected hart has resumed; this is set when a hart
   resumes after a set_requests operation with resume set; it is
   cleared if resume_req is taken away by clearing using a
   set_requests operation
   
hit_breakpoint (bit)
: Semantics not currently defined (but they need to be?)
   
hit_breakpoint (bit)
: Semantics not currently defined (but they need to be?)

resp (*t_riscv_debug_resp)
:  Response from a requested op - only one op should be requested for
    each response

data (bit[32])
:  Data from a completed transaction - this may be the CSR or GPR read
   data, for example

### Debug target response types (*t_riscv_debug_resp*)

rv_debug_resp_acknowledge
:  If *valid* then the debug response acknowledges the receipt of a
   command (actually, this is used for every response EXCEPT for
   read/write completed)

rv_debug_resp_read_write_complete
:  If *valid* then this debug response indicates that a read or write
    transaction has completed and that, for reads, the data on the bus is
    the data read for the transaction


# Trace infrastructure

It can be very useful to get an execution trace from a CPU to aid
debugging, particularly for embedded CPUs. The depth and breadth of
trace can effect the quality of debug available; at some points in
embedded debug it may be useful to count the number of times a
particular program counter is set; at other points it may be useful to
get a high level trace of thousands of instruction cycles; and at
other points a very detailed trace of instruction execution and
register contents may be beneficial.

The trace infrastructure in the CDL RISC-V architecture does not
prescribe a particular trace capability. It does, though, allow for a
great breadth of debug, with instantiating implementations then
supporting whatever depth and subsets of the breadth they desire.

The basic concept behind the CDL RISC-V trace infrastructure is to
deliver a trace of instruction flow and committed register writes from
the end of the pipeline. This trace data comes out in the
*t_riscv_i32_trace* structure. The trace can then be packed in to a
*t_risc_i32_packed_trace*, which combines the data from successive CPU
clock cycles: this packed trace includes fields, for example, for a
count of sequential instructions executed, and details on
non-sequential instruction flow. The packed trace can then be
compressed in to a structured sequence of nybbles, which in turn can
be stored in a FIFO for later unpacking - this permits a great depth
of debug.

The trace packing provided by the CDL RISC-V implementation is
configurable so that the packed trace includes a full instruction
flow, or perhaps the committed register file writes; it also permits
optional tracking of traps and instructions marked as 'tracepoints'.

## Compressed trace

The compressed trace in the CDL RISC-V implementations consists of a
structured sequence of nybbles. The sequence has control nybbles, some
of which have subsequent count and data nybbles. The control nybbles
are:

0000
: Skip - i.e. a nybble of 0 is ignored

0001 - 0111 (treated as 0SSS)
:  SSS (i.e. 1 to 7) sequential instructions were executed since the last nybble reported

1000
:  Non-sequential flow; a branch was taken

1001
:  Non-sequential flow; a JAL/JALR instruction was taken

1010
:  Non-sequential flow; an exception or interrupt was taken

1011
:  Non-sequential flow; a return from exception was taken

1100 (expects another nybble of form RNNN)
:  Data for a PC or RFW or other data; the 'reason' is R (0=PC, 1=RFW
   data) and the data consist of th next 2*NNN nybbles zero-extended
   to the requires length.

1101 (expects another nybble of form NNNN)
:  Trace point of type NNNN seen

111x
:  Reserved

For a particular CPU cycle the compressed trace may record a
sequential control field (indicating that *prior* to this cycle that
many sequential instructions were executed), a non-sequential control
field (indicating that this cycle was a particular control flow
change), a data field for a PC, and a trace point (if the instruction
being executed were somehow marked for tracing by the pipeline).

Note that this order is important; for a cycle the compression specifies
first sequential data, then non-sequential reason, then data, then
trace.

Note also that in a standard compressed
sequence there is no way to have two consecutive nybbles of zero
unless the second is a *Skip*. This provides a means for synchronizing
streams, by inserting a standard number (say 4) of zero nybbles every,
for example, 128 nybbles.

## Recording a compressed trace

A compressed trace is a sequence of nybbles. When recorded in larger
bit strings (e.g. in a 32-bit word) they are defined to be recorded
little-endian; hence the first nybble is in the lowest data nybble at
the lowest address of the addressing scheme for the data words.

As noted above, a compressed trace can only have a multiple of zero
nybbles if the latter ones are *Skip* control nybbles. Hence the
insertion by a compressed trace recorder of 16-bits of zero between
compressed data sequences provides a decoder to synchronize back to
the compressed trace (should this be required).

Hence the recording of a compressed trace should be performed by an
implementation by packing data little-endian, and inserting
quad-nybbles of zero between cycles of data from the packed trace at
regular intervals.

A compressed trace may then be stored in a circular buffer
structure. On overflow the circular buffer could halt recording, or it
may continue to overwrite the earliest trace data. On replay of the
recording the trace can be decoded by synchronizing first and then
uncompressing the packed trace nybbles.

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



