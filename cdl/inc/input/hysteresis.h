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
 * @file   utils.h
 * @brief  Header file for utilities
 *
 * Header file for the types and CDL modules for generic utilities
 *
 */

/*a Types */

/*a Modules */
/*m hysteresis_switch */
extern
module hysteresis_switch( clock clk,
                          input bit reset_n,
                          input bit clk_enable "Assert to enable the internal clock; this permits I/O switches to easily use a slower clock",
                          input bit input_value,
                          output bit output_value,
                          input bit[16] filter_period "Period over which to filter the input - the larger the value, the longer it takes to switch, but the more glitches are removed",
                          input bit[16] filter_level  "Value to exceed to switch output levels - the larger the value, the larger the hysteresis; must be less than filter_period"
    )
{
    timing to   rising clock clk clk_enable;
    timing to   rising clock clk input_value, filter_period, filter_level;
    timing from rising clock clk output_value;
}

