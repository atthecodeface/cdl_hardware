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

last_cycle (bit)
:  If asserted then the exec stage of the instruction will complete if
    the exec stage is not blocked. This is true for most instructions
    in RISC-V; however, misaligned read or write transactions (when
    supported) cause multicycle execution, for example.

cannot_start (bit)
:  Asserted if execution start cannot occur because of some internal
    dependency within the pipeline. Must only be asserted if
    first_cycle is asserted.

branch_taken (bit)
:  Asserted if a branch is being taken. If this is asserted then
    last_cycle must also be asserted.

jalr (bit)
:  Asserted if the instruction is a JALR instruction. If this is asserted then
    last_cycle must also be asserted.

predicted_branch (bit)
:  Asserted if the instruction at decode predicted a branch; this must
    be set in the state for the exec stage if the decode predicted a
    branch *and the pipeline control used that prediction*

pc_if_mispredicted (32 bits)
:  Reports the PC for a mispredicted branch; this must contain the
    target for a JALR instruction, for conditional branches it should
    contain either PC+2/4 or the branch target, depending on whether a
    branch was predicted and whether it was taken; for a JAL
    instruction it should contain the target.

branch_condition_met (bit)
:  Asserted if a branch condition was met; only valid if instruction
    being decoded is a branch

dmem_access_req (t_riscv_mem_access_req)
:  Data memory access request

csr_access (t_riscv_csr_access)
:  CSR access decoded from the instruction with correct write data

rs1 (32 bits)
:  The value of rs1 being used by the execution stage; this is
    provided to feed coprocessors, not for the pipeline control

rs2 (32 bits)
:  The value of rs2 being used by the execution stage; this is
    provided to feed coprocessors, not for the pipeline control

idecode (instruction decode)
:  The instruction decode of the instruction bein executed,
    provided to feed coprocessors, not for the pipeline control

instruction (32-bit)
:  The instruction being executed, for trace purposes. If trace is not
    required then this may be optimized out in synthesis.


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

