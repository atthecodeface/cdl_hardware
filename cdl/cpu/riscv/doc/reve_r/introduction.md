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

