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
 * @file   riscv_submodules.cdl
 * @brief  Submodule declarations for building RISC-V implementations
 *
 */

/*a Includes
 */
include "riscv.h"
include "riscv_internal_types.h"

/*a Modules
 */
/*m riscv_i32_decode  */
extern
module riscv_i32_decode( input t_riscv_word instruction,
                         output t_riscv_i32_decode idecode,
                         input  t_riscv_config          riscv_config
)
{
    timing comb input instruction, riscv_config;
    timing comb output idecode;
}

/*m riscv_i32c_decode  */
extern
module riscv_i32c_decode( input t_riscv_word instruction,
                          output t_riscv_i32_decode idecode,
                         input  t_riscv_config          riscv_config
)
{
    timing comb input instruction, riscv_config;
    timing comb output idecode;
}

/*m riscv_e32_decode  */
extern
module riscv_e32_decode( input t_riscv_word instruction,
                         output t_riscv_i32_decode idecode
)
{
    timing comb input instruction;
    timing comb output idecode;
}

/*m riscv_i32_alu  */
extern
module riscv_i32_alu( input t_riscv_i32_decode      idecode,
                      input t_riscv_word            pc,
                      input t_riscv_word            rs1,
                      input t_riscv_word            rs2,
                      output t_riscv_i32_alu_result alu_result
)
{
    timing comb input  idecode, pc, rs1, rs2;
    timing comb output alu_result;
}

/*m riscv_csrs_minimal  */
extern
module riscv_csrs_minimal( clock clk                                   "RISC-V clock",
                           input bit reset_n                           "Active low reset",
                           input t_riscv_csr_access csr_access         "RISC-V CSR access, combinatorially decoded",
                           input t_riscv_word       csr_write_data     "Write data for the CSR access, later in the cycle than @csr_access possibly",
                           output t_riscv_csr_data csr_data            "CSR respone (including read data), from the current @a csr_access",
                           input t_riscv_csr_controls csr_controls     "Control signals to update the CSRs",
                           output t_riscv_csrs_minimal csrs            "CSR values"
    )
{
    timing to   rising clock clk csr_access, csr_write_data, csr_controls;
    timing from rising clock clk csr_data, csrs;
    timing comb input csr_access;
    timing comb output csr_data;
}
