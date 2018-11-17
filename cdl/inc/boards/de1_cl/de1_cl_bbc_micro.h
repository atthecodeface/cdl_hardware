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
 * @file   de1_cl.h
 * @brief  Input file for DE1 cl inputs and boards
 *
 * Header file for the types and CDL modules for input devices
 *
 */

/*a Includes */
include "boards/de1_cl/de1_cl.h"
include "bbc/bbc_types.h"
include "types/csr.h"
include "types/video.h"
include "types/input_devices.h"

/*a Modules */
/*m bbc_micro_de1_cl_bbc */
extern
module bbc_micro_de1_cl_bbc( clock clk          "50MHz clock from DE1 clock generator",
                             clock video_clk    "9MHz clock from PLL, derived from 50MHz",
                             input bit reset_n  "hard reset from a pin - a key on DE1",
                             input bit bbc_reset_n,
                             input bit framebuffer_reset_n,
                             output t_bbc_clock_control clock_control,
                             input t_bbc_keyboard bbc_keyboard,
                             output t_video_bus video_bus,
                             input t_csr_request csr_request,
                             output t_csr_response csr_response
    )
{
    timing from rising clock clk clock_control;
    timing to   rising clock clk bbc_keyboard, csr_request;
    timing from rising clock clk csr_response;
    timing from rising clock video_clk video_bus;
}

/*m bbc_micro_de1_cl_io */
extern
module bbc_micro_de1_cl_io( clock clk          "50MHz clock from DE1 clock generator",
                            clock video_clk    "9MHz clock from PLL, derived from 50MHz",
                            input bit reset_n  "hard reset from a pin - a key on DE1",
                            input bit bbc_reset_n,
                            input bit framebuffer_reset_n,
                            input t_de1_inputs de1_inputs,
                            input t_bbc_clock_control clock_control,
                            output t_bbc_keyboard bbc_keyboard,
                            output t_video_bus video_bus,
                            output t_csr_request csr_request,
                            input t_csr_response csr_response,
                            input t_ps2_pins ps2_in   "PS2 input pins",
                            output t_ps2_pins ps2_out "PS2 output pin driver open collector",
                            input  t_de1_cl_inputs_status   inputs_status  "DE1 CL daughterboard shifter register etc status",
                            output t_de1_cl_inputs_control  inputs_control "DE1 CL daughterboard shifter register control",
                            output t_de1_leds de1_leds,
                            output bit lcd_source,
                            output bit led_chain
    )
{
    timing to   rising clock clk clock_control;
    timing to   rising clock clk de1_inputs;
    timing from rising clock clk lcd_source, de1_leds;
    timing from rising clock clk bbc_keyboard, csr_request;
    timing to   rising clock clk csr_response;
    timing from rising clock video_clk video_bus;
    timing to   rising clock clk ps2_in, inputs_status;
    timing from rising clock clk ps2_out, inputs_control, led_chain;
}
