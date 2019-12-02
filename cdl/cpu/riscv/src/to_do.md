# To do

pipeline_control_fetch_req needs riscv_config to use i32c enable for
blocking branch prediction of misaligned targets

mepc and dpc etc should have bits [2;0] zeroed if i32c not configured at all
mepc and dpc etc should have bit [0] zeroed always (?)

mepc and dpc etc should have bit[1] ignored if i32c is configured but
disabled

deleg for user N mode

trace pack should be better with PCs - probably misses interrupt restarts and the like
