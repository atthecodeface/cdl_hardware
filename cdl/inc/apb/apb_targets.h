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
 * @file   apb_peripherals.h
 * @brief  Modules of various simple APB peripherals
 *
 * Header file for the modules for some very simple APB peripherals
 *
 */

/*a Includes */
include "types/apb.h"
include "types/timer.h"
include "types/axi.h"
include "types/dprintf.h"
include "types/sram.h"
include "types/ps2.h"

/*a Modules - see also csr_target_apb, csr_master_apb in csr_interface.h */
/*m apb_target_timer */
extern module apb_target_timer( clock clk         "System clock",
                                input bit reset_n "Active low reset",

                                input  t_apb_request  apb_request  "APB request",
                                output t_apb_response apb_response "APB response",

                                output bit[3] timer_equalled
    )
{
    timing to   rising clock clk apb_request;
    timing from rising clock clk apb_response, timer_equalled;

    timing comb input  apb_request;
    timing comb output apb_response; // since response depends on request address usually
}

/*m apb_target_rv_timer */
extern
module apb_target_rv_timer( clock clk             "System clock",
                            input bit reset_n     "Active low reset",
                            input t_timer_control timer_control "Control of the timer", 

                            input  t_apb_request  apb_request  "APB request",
                            output t_apb_response apb_response "APB response",

                            output t_timer_value  timer_value
    )
{
    timing to   rising clock clk apb_request, timer_control;
    timing from rising clock clk apb_response, timer_value;
}

/*m apb_target_gpio */
extern module apb_target_gpio( clock clk         "System clock",
                               input bit reset_n "Active low reset",

                               input  t_apb_request  apb_request  "APB request",
                               output t_apb_response apb_response "APB response",

                               output bit[16] gpio_output,
                               output bit[16] gpio_output_enable,
                               input bit[16]  gpio_input,
                               output bit     gpio_input_event
    )
{
    timing to   rising clock clk apb_request;
    timing from rising clock clk apb_response;
    timing from rising clock clk gpio_output, gpio_output_enable, gpio_input_event;
    timing to   rising clock clk gpio_input;
}

/*m apb_target_sram_interface */
extern
module apb_target_sram_interface( clock clk         "System clock",
                                  input bit reset_n "Active low reset",

                                  input  t_apb_request  apb_request  "APB request",
                                  output t_apb_response apb_response "APB response",

                                  output bit[32] sram_ctrl "SRAM control for whatever purpose",

                                  output t_sram_access_req  sram_access_req  "SRAM access request",
                                  input  t_sram_access_resp sram_access_resp "SRAM access response"
    )
{
    timing to   rising clock clk apb_request;
    timing from rising clock clk apb_response;
    timing from rising clock clk sram_access_req, sram_ctrl;
    timing to   rising clock clk sram_access_resp;
}

/*m apb_target_dprintf */
extern module apb_target_dprintf( clock clk         "System clock",
                                  input bit reset_n "Active low reset",

                                  input  t_apb_request  apb_request  "APB request",
                                  output t_apb_response apb_response "APB response",

                                  output t_dprintf_req_4 dprintf_req,
                                  input  bit             dprintf_ack
    )
{
    timing to   rising clock clk apb_request;
    timing from rising clock clk apb_response;

    timing from rising clock clk dprintf_req;
    timing to   rising clock clk dprintf_ack;

}

/*m apb_target_led_ws2812 */
extern
module apb_target_led_ws2812( clock clk         "System clock",
                              input bit reset_n "Active low reset",

                              input  t_apb_request  apb_request  "APB request",
                              output t_apb_response apb_response "APB response",

                              input bit[8] divider_400ns_in "Default value for divider_400ns",

                              output bit led_chain
    )
{
    timing to   rising clock clk apb_request;
    timing from rising clock clk apb_response;

    timing from rising clock clk led_chain;
    timing to   rising clock clk divider_400ns_in;
    
}

/*m apb_target_ps2_host */
extern
module apb_target_ps2_host( clock clk         "System clock",
                            input bit reset_n "Active low reset",

                            input  t_apb_request  apb_request  "APB request",
                            output t_apb_response apb_response "APB response",

                            input t_ps2_pins ps2_in   "Pin values from the outside",
                            output t_ps2_pins ps2_out "Pin values to drive - 1 means float high, 0 means pull low"
    )
{
    timing to   rising clock clk apb_request;
    timing from rising clock clk apb_response;

    timing to   rising clock clk ps2_in;
    timing from rising clock clk ps2_out;
}

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/


