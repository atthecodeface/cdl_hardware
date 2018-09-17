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
include "apb.h"
include "axi.h"
include "dprintf.h"
include "srams.h"

/*a Modules */
/*a Modules - see also csr_target_apb, csr_master_apb in csr_interface.h */
/*m apb_master_mux
 *
 * Multiplex two APB masters on to a single APB master bus
 *
 */
extern
module apb_master_mux( clock clk         "System clock",
                       input bit reset_n "Active low reset",

                       input  t_apb_request  apb_request_0  "APB request to master 0",
                       output t_apb_response apb_response_0 "APB response to master 0",

                       input  t_apb_request  apb_request_1  "APB request to master 1",
                       output t_apb_response apb_response_1 "APB response to master 1",

                       output  t_apb_request  apb_request  "APB request to targets",
                       input   t_apb_response apb_response "APB response from targets"
    )
{
    timing to   rising clock clk apb_request_0, apb_request_1;
    timing from rising clock clk apb_response_0, apb_response_1;
    timing from rising clock clk apb_request;
    timing to   rising clock clk apb_response;
}

/*m apb_master_axi
 *
 * APB master driven by an AXI target (32-bit address, 64-bit data)
 *
 * Supports aligned 32-bit single length transactions only
 *
 */
extern
module apb_master_axi( clock aclk,
                       input bit areset_n,
                       input t_axi_request ar,
                       output bit awready,
                       input t_axi_request aw,
                       output bit arready,
                       output bit wready,
                       input t_axi_write_data w,
                       input bit bready,
                       output t_axi_write_response b,
                       input bit rready,
                       output t_axi_read_response r,

                       output t_apb_request     apb_request,
                       input t_apb_response     apb_response
    )
{
    timing to   rising clock aclk ar, aw, w, bready, rready;
    timing from rising clock aclk awready, arready, wready, b, r;
    timing from rising clock aclk apb_request;
    timing to   rising clock aclk apb_response;
}

/*m apb_processor */
extern
module apb_processor( clock                    clk        "Clock for the CSR interface; a superset of all targets clock",
                      input bit                reset_n,
                      input t_apb_processor_request    apb_processor_request,
                      output t_apb_processor_response  apb_processor_response,
                      output t_apb_request     apb_request   "Pipelined csr request interface output",
                      input t_apb_response     apb_response  "Pipelined csr request interface response",
                      output t_apb_rom_request rom_request,
                      input bit[40]            rom_data
    )
{
    timing to   rising clock clk apb_processor_request;
    timing from rising clock clk apb_processor_response;
    timing from rising clock clk apb_request, rom_request;
    timing to   rising clock clk apb_response, rom_data;
}

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

    //timing comb input  apb_request;
    //timing comb output apb_response; // since response depends on request address usually
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

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/


