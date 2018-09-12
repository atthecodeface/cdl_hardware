riscv_i32_alu
-------------

riscv_i32_decode
----------------

riscv_i32c_decode
----------------

riscv_i32c_pipeline
----------------

* single stage execution pipeline (decode, fetch, execute)
* dmem_access_req valid during the cycle
* dmem_access_resp must be valid with read data at the end of the
cycle
* ifetch_req valid during the cycle
* ifetch_resp must be valid with read data at the end of the
cycle
* supports coprocessor (e.g. for multiply)
* includes:
+ riscv_i32_decode
+ riscv_i32c_decode
+ riscv_i32_alu


riscv_minimal
----------------

* needs to be removed and changed to riscv_i32c_minimal
 * I/E32 instruction set + optionally compressed only (multiply etc
 disabled)
 * set riscv_config.i32c to 1 for RV32IC support
 * set riscv_config.i32c to 0 for no RV32IC support
 * set riscv_config.e32 to 1 for RV32E only (with/without C)
 * set riscv_config.e32 to 0 for no RV32E only (with/without C)
 * set riscv_config.i32m should be 0
 * minimal CSRs (machine mode only)
 * Includes:
   +  riscv_i32c_pipeline

Test benches
------------

tb_riscv_minimal
----------------

* I32C minimal CSRs instantiation without debug
* riscv_config.{e32=0, i32c=0, i32m=0}
* Includes:
+  riscv_minimal (Needs to change to riscv_i32c_minimal

tb_riscv_i32c_minimal
----------------

* I32C minimal CSRs instantiation without debug
* riscv_config.{e32=0, i32c=1, i32m=0}
* Includes:
+  riscv_minimal (Needs to change to riscv_i32c_minimal

tb_riscv_i32c_pipeline3
----------------

* I32C minimal CSRs instantiation with debug
* riscv_config.{e32=0, i32c=1, i32m=0}
* Includes:
 + riscv_i32c_pipeline3
 + riscv_i32_trace
 
tb_riscv_i32mc_pipeline3
----------------

* I32C minimal CSRs instantiation with debug
* riscv_config.{e32=0, i32c=1, i32m=1}
* Includes:
 + jtag_tap
 + riscv_jtag_apb_dm
 + riscv_i32_debug
 + riscv_i32_pipeline_debug
 + riscv_i32c_pipeline3
 + riscv_i32_muldiv
 + riscv_i32_trace
 




