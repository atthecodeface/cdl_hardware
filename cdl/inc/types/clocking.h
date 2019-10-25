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
 * @file   clocking.h
 * @brief  Types for various clocking utilities
 *
 * Header file for the types for clocking utilities
 *
 */

/*t t_bit_delay_config */
typedef struct {
    bit    load;
    bit[9] value;
} t_bit_delay_config;

/*t t_bit_delay_response */
typedef struct {
    bit    load_ack;
    bit[9] value;
    bit    sync_value;
} t_bit_delay_response;

/*t t_phase_measure_request
 */
typedef struct {
    bit valid;
} t_phase_measure_request;

/*t t_phase_measure_response
 */
typedef struct {
    bit ack;
    bit abort;
    bit valid;
    bit[9] delay;
    bit[9] initial_delay;
    bit initial_value;
} t_phase_measure_response;
