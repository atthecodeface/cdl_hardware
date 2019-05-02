# Interfacing to Reve-R

## Fetch interface

The fetch interface is a fetch request, valid at the start of the
cycle (with the address field valid later than the other fields), and
a fetch response which is required at the end of the cycle. The fetch
response should depend on the fetch request.

For high-speed implementations the request type of the fetch request
can be used to provide the response, without requiring any
combinatorial address decode; the fetch logic can determine the
expected response for a sequential or repeat access in the *next*
cycle based on its *current* state and the *current* request, and register
those for presentation in the next cycle. A non-sequential request,
which requires using the address in the request combinatorially, is
not required.

If a lower clock speed is acceptable then the address in the request
may be used combinatorially, and hence more logic between the pipeline
state generating the request and the fetch response.

### Fetch request

The fetch interface request structure is implemented with the *t_riscv_fetch_req* structure. This contains the following
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

error (2-bit)
:  If asserted then the fetch had an error, and the error type will
   indicate the error type

error_type (*t_riscv_fetch_error_type*)
:  The kind of error in the fetch; ignored if valid or error are deasserted.

data (32-bit)
:  The data fetched. All 32 bits must be valid.


## Data read/write/atomics

The memory access bus has a request and a response.

Each request has to be acknowledged in the same cycle that it is
presented. The acknowledgement must not depend on the request; hence
there are two signals provided, one for sequential requests and one
for arbitrary requests. This permits some write gathering in a single
address write buffer in simple implementations.

### Memory access request

The memory access interface uses the *t_riscv_mem_access_req* structure. This contains the following
elements:

valid (bit)
:  Indicates that a memory access request is valid. If this is
    deasserted then the rest of the structure should be ignored.

mode (*t_riscv_mode*)
:  The mode of the code performing the fetch

req_type (*t_riscv_mem_access_req_type*)
:  The kind of request required in this cycle - idle, read, write, or
    an atomic. If atomics are not configured then only idle, read or
    write will ever be presented.

address (32-bit)
:  The address to be accessed. For atomic transactions this is
    guaranteed to be word aligned. For a read operation the address is
    that requested by the read instruction; no distinction is made
    between the size of read, but if the address is not word-aligned
    then the memory subsystem need only supply the bytes of the
    requested address within the word-aligned word address requested
    (i.e. the memory subsystem must not read beyond the four bytes
    starting at a word-aligned version of the requested address). For
    a write operation the byte enables indicate which bytes of the
    word-aligned address are requested to be written, but the address
    will be the full 32-bit address from the instruction.

sequential (bit)
:  A hint bit indicating that the address is word-aligned and
    precisely one word further on than the previous request, and a
    read or a write, and the same type as the last cycle. This hint
    bit will only be set on specific instruction encoding sequences,
    such as might be seen in reading and writing the stack.

byte_enable (4-bit)
:  A mask of which bytes are being written for write operations. The
    value here should be ignored for atomic or read operations.

write_data (32-bit)
:  The data to be written, or to be used in conjunction with memory
    data for atomics

The *t_riscv_mem_access_req_type* enumeration includes

* rv_mem_access_idle: address and data are invalid 

* rv_mem_access_read: read of address is requested; byte_enable and
  write_data should be ignored
  
* rv_mem_access_write : write of address is requested using the
  byte_enable signals to determine which bytes to write, and using the
  write_data for the transaction

### Memory access response

The memory access response uses the *t_riscv_mem_access_resp* structure. This contains the following
elements:

ack_if_seq (bit)
:  If a valid access with sequential is being presented then the
    request will be taken by the memory subsystem. Must not depend on
    the request being presented.

ack (bit)
:  If a valid access with or without sequential is being presented then the
    request will be taken by the memory subsystem. Must not depend on
    the request being presented.

abort_req (bit)
: If asserted then the data transaction must abort. This signal is
    valid in the data phase of a transaction (not the request phase);
    asserting this signal should cause a load access or store access
    fault trap on the current instruction program counter. The
    pipeline must be configured to support aborts. The pipeline can be
    configured to accept aborts only on the cycle after a memory
    access is requested (early aborts), or it may be configured to
    support aborts at any stage - if the latter, then subsequent
    instructions *must* not be committed to until an abort may no
    longer take place, hence the performance of the pipeline drops.

may_still_abort (bit)
: If the pipeline is configured for supporting late abort in memory
    accesses then this signal indicates that an access that is in
    progress may still generate an abort. If this signal is
    deasserted, but the access_complete signal is also deasserted,
    then the memory subsystem has determined that the access will
    complete correctly. This permits subsequent instructions to be
    committed to execution.

access_complete (bit)
:  Valid in the same cycle as read_data; must be set on writes as well
    as reads, as it completes an access

read_data (32-bit)
: Data returned from reading the requested address

Note that the *ack* and *ack_if_seq* signals are valid in the memory
access request phase, while the remaining fields are valid in the
memory data phase.
