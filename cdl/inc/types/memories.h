/** Copyright (C) 2019,  Gavin J Stark.  All rights reserved.
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
 * @file   memories.h
 * @brief  Types for external memory devices
 *
 * Header file for the types for external memory devices
 *
 */

/*a Types */
/*t t_mem_flash_out */
typedef struct {
    bit[32] address; // not all bits may be used
    bit we_n;
    bit wp_n;
    bit adv_n;
    bit rst_n;
    bit oe_n;
    bit ce_n;
    bit wait;
    bit clk; // may not be used (if tied to a real clock!)
    bit[32] data;    // not all bits may be used
    bit data_enable; // Not a pin, use in conjunction with data
} t_mem_flash_out;

/*t t_mem_flash_in */
typedef struct {
    bit[32] data;
} t_mem_flash_in;

/*t t_sdio_out */
typedef struct {
    bit cmd;
    bit clk;
    bit[4] data;
    bit    data_enable; // Not a pin, use in conjunction with data
} t_sdio_out;

/*t t_sdio_in */
typedef struct {
    bit[4] data;
    bit    cd "Card detect";
} t_sdio_in;


