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
 * @file   clock_divider.h
 * @brief  Types for clock divider modules
 *
 * Header file for the types for clock dividers
 *
 */

/*a Types */
/*t t_clock_divider_control */
typedef struct {
    bit     write_config "Asserted if clock divider configuration should be written";
    bit[32] write_data   "Data to be used if write_config is asserted";
    bit     start        "Assert to start the clock divider - deassert if running";
    bit     stop         "Assert to stop the clock divider - only used if running";
    bit     disable_fractional "Assert to disable fractional mode";
} t_clock_divider_control;

/*t t_clock_divider_output */
typedef struct {
    bit[32] config_data   "Current configuration, as last written (defaults to 0)";
    bit     running       "Asserted if the clock divider has been started";
    bit     clock_enable  "Output from the clock divider";
} t_clock_divider_output;

