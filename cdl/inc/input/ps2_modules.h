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
include "types/ps2.h"

/*a Modules */
/*m ps2_host */
extern module ps2_host( clock        clk     "Clock",
                        input bit    reset_n,
                        input t_ps2_pins ps2_in   "Pin values from the outside",
                        output t_ps2_pins ps2_out "Pin values to drive - 1 means float high, 0 means pull low",

                        output t_ps2_rx_data ps2_rx_data,
                        input bit[16] divider
    )
{
    timing to    rising clock clk ps2_in, divider;
    timing from  rising clock clk ps2_out, ps2_rx_data;
}

/*m ps2_host_keyboard */
extern module ps2_host_keyboard( clock                   clk     "Clock",
                          input bit               reset_n,
                          input t_ps2_rx_data     ps2_rx_data,
                          output t_ps2_key_state  ps2_key
    )
{
    timing to    rising clock clk ps2_rx_data;
    timing from  rising clock clk ps2_key;
}

