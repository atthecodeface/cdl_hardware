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
 * @file   input_devices.h
 * @brief  Input device header file for CDL modules
 *
 * Header file for the types and CDL modules for input devices
 *
 */

/*a Includes */
include "bbc_micro_types.h"

/*a Types */
/*t t_dprintf_req_4 */
typedef struct {
    bit valid;
    bit[16] address;
    bit[64] data_0;
    bit[64] data_1;
    bit[64] data_2;
    bit[64] data_3;
} t_dprintf_req_4;

/*t t_dprintf_req_2 */
typedef struct {
    bit valid;
    bit[16] address;
    bit[64] data_0;
    bit[64] data_1;
} t_dprintf_req_2;

/*t t_dprintf_resp */
typedef struct {
    bit ack;
} t_dprintf_resp;

/*t t_dprintf_byte
 *
 * Validated byte with address; the output of the dprintf module
 */
typedef struct {
    bit valid;
    bit[8]  data;
    bit[16] address;
} t_dprintf_byte;

