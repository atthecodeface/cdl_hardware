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


