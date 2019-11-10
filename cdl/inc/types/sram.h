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

/*a Types */
/*t t_sram_access_req
 */
typedef struct {
    bit     valid;
    bit[8]  id;
    bit     read_not_write;
    bit[8]  byte_enable;
    bit[32] address;
    bit[64] write_data;
} t_sram_access_req;

/*t t_sram_access_resp
 */
typedef struct {
    bit     ack;
    bit     valid;
    bit[8]  id;
    bit[64] data;
} t_sram_access_resp;

