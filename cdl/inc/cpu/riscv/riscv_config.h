/*a Configuration constants
 */
constant integer rv_cfg_i32c_force_disable=0;
constant integer rv_cfg_e32_force_enable=0;
constant integer rv_cfg_i32m_force_disable=0;
constant integer rv_cfg_i32_bitmap_enhanced_shift_enable=1;
constant integer rv_cfg_i32_bitmap_others_enable=1;
constant integer rv_cfg_i32_custom0_enable=1;
constant integer rv_cfg_i32_custom0_as_load=1;
constant integer rv_cfg_i32_custom0_as_store=0;
constant integer rv_cfg_i32_custom1_enable=1;
constant integer rv_cfg_i32_custom1_as_load=1;
constant integer rv_cfg_i32_custom1_as_store=0;
constant integer rv_cfg_i32_custom2_enable=0;
constant integer rv_cfg_i32_custom2_as_load=1;
constant integer rv_cfg_i32_custom2_as_store=0;
constant integer rv_cfg_i32_custom3_enable=0;
constant integer rv_cfg_i32_custom3_as_load=1;
constant integer rv_cfg_i32_custom3_as_store=0;
constant integer rv_cfg_memory_abort_disable=0;
constant integer rv_cfg_memory_late_abort_enable=1;
constant integer rv_cfg_coproc_force_disable=0;
constant integer rv_cfg_debug_force_disable=0;
constant integer rv_cfg_supervisor_mode_enable=0;
constant integer rv_cfg_user_mode_enable=1;
constant integer rv_cfg_user_irq_mode_enable=0;

/*a CSR constants */
constant integer mimpid = 0;
constant integer misa = 0;
constant integer mvendorid = 0;
constant integer marchid = 0;
constant integer mhartid = 0;

/*a Types
 */
typedef struct {
    bit[32] mhartid   "ORred with constant";
    bit[32] misa      "ORred with constant";
    bit[32] mvendorid "ORred with constant";
    bit[32] marchid   "ORred with constant";
    bit[32] mimpid    "ORred with constant";
} t_riscv_csr_access_custom;
