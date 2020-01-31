/** Copyright (C) 2016-2017,  Gavin J Stark.  All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @file   srams.h
 * @brief  SRAM modules used by all the modules
 *
 */

/*a Includes */
include "types/sram.h"

/*a Modules */
/*m se_sram_srw_128x64 */
extern module se_sram_srw_128x64( clock sram_clock,
                                   input bit select,
                                   input bit[7] address,
                                   input bit read_not_write,
                                   input bit write_enable,
                                   input bit[64] write_data,
                                   output bit[64] data_out )
{
    timing to   rising clock sram_clock   select, address, read_not_write, write_data, write_enable;
    timing from rising clock sram_clock   data_out;
}

/*m se_sram_srw_128x45 */
extern module se_sram_srw_128x45( clock sram_clock,
                                   input bit select,
                                   input bit[7] address,
                                   input bit read_not_write,
                                   input bit[45] write_data,
                                   output bit[45] data_out )
{
    timing to   rising clock sram_clock   select, address, read_not_write, write_data;
    timing from rising clock sram_clock   data_out;
}

/*m se_sram_srw_256x7 */
extern module se_sram_srw_256x7( clock sram_clock,
                                   input bit select,
                                   input bit[8] address,
                                   input bit read_not_write,
                                   input bit[7] write_data,
                                   output bit[7] data_out )
{
    timing to   rising clock sram_clock   select, address, read_not_write, write_data;
    timing from rising clock sram_clock   data_out;
}

/*m se_sram_srw_256x40 */
extern module se_sram_srw_256x40( clock sram_clock,
                                   input bit select,
                                   input bit[8] address,
                                   input bit read_not_write,
                                   input bit[40] write_data,
                                   output bit[40] data_out )
{
    timing to   rising clock sram_clock   select, address, read_not_write, write_data;
    timing from rising clock sram_clock   data_out;
}

/*m se_sram_srw_512x32 */
extern module se_sram_srw_512x32( clock sram_clock,
                                   input bit select,
                                   input bit[9] address,
                                   input bit read_not_write,
                                   input bit write_enable,
                                   input bit[32] write_data,
                                   output bit[32] data_out )
{
    timing to   rising clock sram_clock   select, address, read_not_write, write_data, write_enable;
    timing from rising clock sram_clock   data_out;
}

/*m se_sram_srw_512x64 */
extern module se_sram_srw_512x64( clock sram_clock,
                                   input bit select,
                                   input bit[9] address,
                                   input bit read_not_write,
                                   input bit write_enable,
                                   input bit[64] write_data,
                                   output bit[64] data_out )
{
    timing to   rising clock sram_clock   select, address, read_not_write, write_data, write_enable;
    timing from rising clock sram_clock   data_out;
}

/*m se_sram_srw_16384x8 */
extern module se_sram_srw_16384x8( clock sram_clock,
                                   input bit select,
                                   input bit[14] address,
                                   input bit read_not_write,
                                   input bit write_enable,
                                   input bit[8] write_data,
                                   output bit[8] data_out )
{
    timing to   rising clock sram_clock   select, address, read_not_write, write_data, write_enable;
    timing from rising clock sram_clock   data_out;
}

/*m se_sram_srw_65536x8 */
extern module se_sram_srw_65536x8( clock sram_clock,
                                   input bit select,
                                   input bit[16] address,
                                   input bit read_not_write,
                                   input bit write_enable,
                                   input bit[8] write_data,
                                   output bit[8] data_out )
{
    timing to   rising clock sram_clock   select, address, read_not_write, write_data, write_enable;
    timing from rising clock sram_clock   data_out;
}

/*m se_sram_srw_16384x32 */
extern module se_sram_srw_16384x32( clock sram_clock,
                                    input bit select,
                                    input bit[14] address,
                                    input bit write_enable,
                                    input bit read_not_write,
                                    input bit[32] write_data,
                                    output bit[32] data_out )
{
    timing to   rising clock sram_clock   select, address, read_not_write, write_data, write_enable;
    timing from rising clock sram_clock   data_out;
}

/*m se_sram_srw_16384x32_we4 */
extern module se_sram_srw_16384x32_we8( clock sram_clock,
                                    input bit select,
                                    input bit[14] address,
                                    input bit read_not_write,
                                    input bit[4] write_enable,
                                    input bit[32] write_data,
                                    output bit[32] data_out )
{
    timing to   rising clock sram_clock   select, address, read_not_write, write_data, write_enable;
    timing from rising clock sram_clock   data_out;
}

/*m se_sram_srw_16384x40 */
extern module se_sram_srw_16384x40( clock sram_clock,
                                    input bit select,
                                    input bit[14] address,
                                    input bit read_not_write,
                                    input bit[40] write_data,
                                    output bit[40] data_out )
{
    timing to   rising clock sram_clock   select, address, read_not_write, write_data;
    timing from rising clock sram_clock   data_out;
}

/*m se_sram_srw_32768x64 */
extern module se_sram_srw_32768x64( clock sram_clock,
                                   input bit select,
                                   input bit[15] address,
                                   input bit read_not_write,
                                   input bit write_enable,
                                   input bit[64] write_data,
                                   output bit[64] data_out )
{
    timing to   rising clock sram_clock   select, address, read_not_write, write_data, write_enable;
    timing from rising clock sram_clock   data_out;
}

/*m se_sram_srw_32768x32 */
extern module se_sram_srw_32768x32( clock sram_clock,
                                   input bit select,
                                   input bit[15] address,
                                   input bit read_not_write,
                                   input bit write_enable,
                                   input bit[32] write_data,
                                   output bit[32] data_out )
{
    timing to   rising clock sram_clock   select, address, read_not_write, write_data, write_enable;
    timing from rising clock sram_clock   data_out;
}

/*m se_sram_srw_65536x32 */
extern module se_sram_srw_65536x32( clock sram_clock,
                                   input bit select,
                                   input bit[16] address,
                                   input bit read_not_write,
                                   input bit write_enable,
                                   input bit[32] write_data,
                                   output bit[32] data_out )
{
    timing to   rising clock sram_clock   select, address, read_not_write, write_data, write_enable;
    timing from rising clock sram_clock   data_out;
}

/*m se_sram_mrw_2_16384x48 */
extern module se_sram_mrw_2_16384x48( clock sram_clock_0,
                                      input bit select_0,
                                      input bit[14] address_0,
                                      input bit read_not_write_0,
                                      input bit[48] write_data_0,
                                      output bit[48] data_out_0,

                                      clock sram_clock_1,
                                      input bit select_1,
                                      input bit[14] address_1,
                                      input bit read_not_write_1,
                                      input bit[48] write_data_1,
                                      output bit[48] data_out_1)
{
    timing to   rising clock sram_clock_0   select_0, address_0, read_not_write_0, write_data_0;
    timing from rising clock sram_clock_0   data_out_0;
    timing to   rising clock sram_clock_1   select_1, address_1, read_not_write_1, write_data_1;
    timing from rising clock sram_clock_1   data_out_1;
}

/*m se_sram_mrw_2_2048x32 */
extern module se_sram_mrw_2_2048x32( clock sram_clock_0,
                                      input bit select_0,
                                      input bit[11] address_0,
                                      input bit read_not_write_0,
                                      input bit[32] write_data_0,
                                      output bit[32] data_out_0,

                                      clock sram_clock_1,
                                      input bit select_1,
                                      input bit[11] address_1,
                                      input bit read_not_write_1,
                                      input bit[32] write_data_1,
                                      output bit[32] data_out_1)
{
    timing to   rising clock sram_clock_0   select_0, address_0, read_not_write_0, write_data_0;
    timing from rising clock sram_clock_0   data_out_0;
    timing to   rising clock sram_clock_1   select_1, address_1, read_not_write_1, write_data_1;
    timing from rising clock sram_clock_1   data_out_1;
}

/*m se_sram_mrw_2_512x32 */
extern module se_sram_mrw_2_512x32( clock sram_clock_0,
                                      input bit select_0,
                                      input bit[9] address_0,
                                      input bit read_not_write_0,
                                      input bit[32] write_data_0,
                                      output bit[32] data_out_0,

                                      clock sram_clock_1,
                                      input bit select_1,
                                      input bit[9] address_1,
                                      input bit read_not_write_1,
                                      input bit[32] write_data_1,
                                      output bit[32] data_out_1)
{
    timing to   rising clock sram_clock_0   select_0, address_0, read_not_write_0, write_data_0;
    timing from rising clock sram_clock_0   data_out_0;
    timing to   rising clock sram_clock_1   select_1, address_1, read_not_write_1, write_data_1;
    timing from rising clock sram_clock_1   data_out_1;
}

/*m se_sram_mrw_2_512x64 */
extern module se_sram_mrw_2_512x64( clock sram_clock_0,
                                      input bit select_0,
                                      input bit[9] address_0,
                                      input bit read_not_write_0,
                                      input bit[64] write_data_0,
                                      output bit[64] data_out_0,

                                      clock sram_clock_1,
                                      input bit select_1,
                                      input bit[9] address_1,
                                      input bit read_not_write_1,
                                      input bit[64] write_data_1,
                                      output bit[64] data_out_1)
{
    timing to   rising clock sram_clock_0   select_0, address_0, read_not_write_0, write_data_0;
    timing from rising clock sram_clock_0   data_out_0;
    timing to   rising clock sram_clock_1   select_1, address_1, read_not_write_1, write_data_1;
    timing from rising clock sram_clock_1   data_out_1;
}

/*m se_sram_mrw_2_16384x8 */
extern module se_sram_mrw_2_16384x8( clock sram_clock_0,
                                      input bit select_0,
                                      input bit[14] address_0,
                                      input bit read_not_write_0,
                                      input bit[8] write_data_0,
                                      output bit[8] data_out_0,

                                      clock sram_clock_1,
                                      input bit select_1,
                                      input bit[14] address_1,
                                      input bit read_not_write_1,
                                      input bit[8] write_data_1,
                                      output bit[8] data_out_1)
{
    timing to   rising clock sram_clock_0   select_0, address_0, read_not_write_0, write_data_0;
    timing from rising clock sram_clock_0   data_out_0;
    timing to   rising clock sram_clock_1   select_1, address_1, read_not_write_1, write_data_1;
    timing from rising clock sram_clock_1   data_out_1;
}

