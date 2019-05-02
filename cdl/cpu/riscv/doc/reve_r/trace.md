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

