/** @copyright (C) 2019,  Gavin J Stark.  All rights reserved.
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
 * @file   serdes_modules.h
 * @brief  Header files for technology dependent serdes modules
 *
 */
/*a Includes */
include "types/io.h"
include "types/clocking.h"

/*a Modules */
/*m diff_ddr_serializer4 */
extern module diff_ddr_serializer4( clock clk             "Serial clock (as required by technology, maybe data/2)",
                                    clock clk_div2        "Clock for 4-bit wide data",
                                    input bit reset_n     "Active low reset",
                                    input bit[4] data     "Data in",
                                    output t_io_diff pin  "Pin out" )
{
    timing to   rising clock clk_div2 data;
    timing from rising clock clk pin;
}

/*m diff_ddr_deserializer4 */
extern module diff_ddr_deserializer4( clock clk              "Serial clock (as required by technology, maybe data/2)",
                                      clock clk_div2         "Clock for 4-bit wide data",
                                      input bit reset_n      "Active low reset",
                                      input t_io_diff pin    "Pin in",
                                      input t_bit_delay_config   delay_config   "Delay configuration for data",
                                      output t_bit_delay_response delay_response "Response to delay configuration",
                                      output bit[4] data     "Data out",
                                      output bit[4] tracker  "Delayed inverted data out" )
{
    timing to   rising clock clk pin;
    timing from rising clock clk_div2 data, tracker;
    timing to   rising clock clk_div2 delay_config;
    timing from rising clock clk_div2 delay_response;
}

extern module cascaded_delay_pair( clock clk              "Clock to control delay",
                                   input bit reset_n      "Active low reset",
                                   input t_bit_delay_config   delay_config   "Delay configuration for data",
                                   output t_bit_delay_response delay_response "Response to delay configuration",
                                   input bit data_in "Data in prior to delay",
                                   output bit data_out "Delayed data out" )
{
    timing to   rising clock clk data_in;  // Actually not - really comb in to out
    timing from rising clock clk data_out; // Actually not - really comb in to out
    timing to   rising clock clk delay_config;
    timing from rising clock clk delay_response;
}

