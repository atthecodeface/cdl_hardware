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
 * @file   apb.h
 * @brief  Types for the APB bus
 *
 * Header file for the types for an APB bus, but no modules
 *
 */

/*a Types */
/*t t_apb_request */
typedef struct {
    bit[32] paddr;
    bit     penable;
    bit     psel;
    bit     pwrite;
    bit[32] pwdata;
} t_apb_request;

/*t t_apb_response */
typedef struct {
    bit[32] prdata;
    bit     pready;
    bit     perr;
} t_apb_response;

/*t t_apb_processor_response */
typedef struct {
    bit acknowledge;
    bit rom_busy;
} t_apb_processor_response;

/*t t_apb_processor_request */
typedef struct {
    bit valid;
    bit[16] address;
} t_apb_processor_request;

/*t t_apb_rom_request */
typedef struct {
    bit enable;
    bit[16] address;
} t_apb_rom_request;

