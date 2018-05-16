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
 * @file   riscv.h
 * @brief  Header file for RISC-V implementations
 *
 */

/*a Constants
 *
 * Constants for the RISC-V implementation; can be overridden in CDL
 * builds with a dc: option in the model_list
 */
constant integer RISCV_DATA_ADDR_WIDTH = 14;
constant integer RISCV_INSTR_ADDR_WIDTH = 14;

/*a Basic types
 */
/*t t_riscv_mem_access_req
 */
typedef struct {
    bit[32]  address;
    bit[4]   byte_enable;
    bit      write_enable;
    bit      read_enable;
    bit[32]  write_data;
} t_riscv_mem_access_req;

/*t t_riscv_mem_access_resp */
typedef struct {
    bit                  wait;
    bit[32]              read_data;
} t_riscv_mem_access_resp;

/*t t_riscv_word
 */
typedef bit[32] t_riscv_word;

/*t t_riscv_fetch_req
 */
typedef struct {
    bit      valid;
    bit[32]  address;
    bit      sequential;
} t_riscv_fetch_req;

/*t t_riscv_fetch_resp
 */
typedef struct {
    bit      valid;
    bit      debug;
    bit[32]  data;
} t_riscv_fetch_resp;

/*a Implementations */
/*m riscv_minimal
 */
extern
module riscv_minimal( clock clk,
                     input bit reset_n,
                     output t_riscv_mem_access_req  dmem_access_req,
                     input  t_riscv_mem_access_resp dmem_access_resp,
                     output t_riscv_mem_access_req  imem_access_req,
                     input  t_riscv_mem_access_resp imem_access_resp
)
{
    timing from rising clock clk dmem_access_req, imem_access_req;
    timing to   rising clock clk dmem_access_resp, imem_access_resp;
}

/*m riscv_i32c_minimal
 */
extern
module riscv_i32c_minimal( clock clk,
                     input bit reset_n,
                     output t_riscv_mem_access_req  dmem_access_req,
                     input  t_riscv_mem_access_resp dmem_access_resp,
                     output t_riscv_mem_access_req  imem_access_req,
                     input  t_riscv_mem_access_resp imem_access_resp
)
{
    timing from rising clock clk dmem_access_req, imem_access_req;
    timing to   rising clock clk dmem_access_resp, imem_access_resp;
}
/*m riscv_i32c_pipeline
 */
extern
module riscv_i32c_pipeline( clock clk,
                            input bit reset_n,
                            output t_riscv_fetch_req       ifetch_req,
                            input  t_riscv_fetch_resp      ifetch_resp,
                            output t_riscv_mem_access_req  dmem_access_req,
                            input  t_riscv_mem_access_resp dmem_access_resp
)
{
    timing from rising clock clk dmem_access_req, ifetch_req;
    timing to   rising clock clk dmem_access_resp, ifetch_resp;
}

/*m riscv_i32c_pipeline3
 */
extern
module riscv_i32c_pipeline3( clock clk,
                            input bit reset_n,
                            output t_riscv_fetch_req       ifetch_req,
                            input  t_riscv_fetch_resp      ifetch_resp,
                            output t_riscv_mem_access_req  dmem_access_req,
                            input  t_riscv_mem_access_resp dmem_access_resp
)
{
    timing from rising clock clk dmem_access_req, ifetch_req;
    timing to   rising clock clk dmem_access_resp, ifetch_resp;
}
