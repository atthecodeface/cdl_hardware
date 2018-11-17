/** @copyright (C) 2016-2017,  Gavin J Stark.  All rights reserved.
 *
 * @copyright
 *    Licensed under the Apache License, Version 2.0 (the "License");
 *    you may not use this file except in compliance with the License.
 *    You may obtain a copy of the License at
 *     http://www.apache.org/licenses/LICENSE-2.0.
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 *
 * @file   picoriscv_types.cdl
 * @brief  Internal types and constants for Pico-RISC-V microcomputer
 *
 */

/*a Includes
 */
include "cpu/riscv/riscv.h"

/*t t_prv_mem_control */
/**
 * This structure conveys memory management to the
 * Pico-RISC-V CDL implementation and various peripherals and other
 * logic
 */
typedef struct {
    bit dmem_request;
    bit ifetch_request;
    bit dmem_set_reg;
    bit ifetch_set_reg;
    bit ifetch_use_reg;
    bit io_enable;
} t_prv_mem_control;

/*t t_prv_clock_control */
/**
 * This structure conveys clock gating and reset information to the
 * Pico-RISC-V CDL implementation and various peripherals and other
 * logic
 */
typedef struct {
    bit riscv_clk_enable;
    bit[4] debug;
} t_prv_clock_control;

/*t t_prv_clock_status */
/**
 * This structure conveys information in to the clock control module
 * from the RISC-V.
 */
typedef struct {
    bit imem_request;
    bit io_request;
    bit io_ready;
    bit dmem_read_enable;
    bit dmem_write_enable;
} t_prv_clock_status;

/*t t_prv_csr_select
 */
typedef enum[16] {
    prv_csr_select_clocks=0,
} t_prv_csr_select;

/*t t_prv_keyboard
 */
typedef struct {
    bit[64] keys_low;
} t_prv_keyboard;


