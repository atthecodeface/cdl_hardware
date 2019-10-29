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

/*t t_bit_delay_op */
typedef enum [2] {
    bit_delay_op_none,
    bit_delay_op_load,
    bit_delay_op_inc,
    bit_delay_op_dec
} t_bit_delay_op;

/*t t_bit_delay_config */
typedef struct {
    bit    select  "If a delay pair, which delay to update";
    t_bit_delay_op op;
    bit[9] value;
} t_bit_delay_config;

/*t t_bit_delay_response */
typedef struct {
    bit    op_ack;
    bit[9] delay_value;
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

/*t t_eye_track_request
 */
typedef struct {
    bit enable         "If deasserted, stop tracking and seeking. Do not assert until phase_width is stable and valid";
    bit measure        "Assert to start a measurement of the eye";
    bit seek_enable    "If asserted and enabled, then data delay can be adjusted by one; otherwise eye width is measured and centre determined by data delay is not adjusted";
    bit track_enable    "If asserted and enabled, then data delay can be adjusted in steps; otherwise eye width is measured and centre determined by data delay is not adjusted";
    bit[9] phase_width "Width in taps of a phase of clock - no eye can be wider than this! Must be valid if enable is asserted";
    bit[9] min_eye_width "Width in taps of a phase of clock - no eye can be wider than this! Must be valid if enable is asserted";
} t_eye_track_request;

/*t t_eye_track_response
 */
typedef struct {
    bit measure_ack    "Asserted to acknowledge a request to measure the eye - later eye_data_valid will be asserted";
    bit locked         "Asserted if enabled and measured eye width is large enough and data is sufficiently centred";
    bit eye_data_valid "Asserted for a single clock tick when eye data measurements are valid";
    bit[9] data_delay;
    bit[9] eye_width;
    bit[9] eye_center;
} t_eye_track_response;
