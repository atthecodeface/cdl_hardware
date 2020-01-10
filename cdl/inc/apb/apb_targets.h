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
include "types/uart.h"
include "types/axi.h"
include "types/dprintf.h"
include "types/sram.h"
include "types/ps2.h"
include "types/i2c.h"
include "types/jtag.h"

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

                            output t_timer_value  timer_value,
                            output t_timer_control timer_control_out "Control from the timer, if configured"
    )
{
    timing to   rising clock clk apb_request, timer_control;
    timing from rising clock clk apb_response, timer_value, timer_control_out;
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

/*m apb_target_jtag */
extern module apb_target_jtag( clock clk         "System clock",
                               input bit reset_n "Active low reset",

                               input  t_apb_request  apb_request  "APB request",
                               output t_apb_response apb_response "APB response",

                               output bit             jtag_tck_enable,
                               output t_jtag          jtag,
                               input  bit             jtag_tdo

    )
{
    timing to   rising clock clk apb_request;
    timing from rising clock clk apb_response;
    timing from rising clock clk jtag_tck_enable, jtag;
    timing to   rising clock clk jtag_tdo;
}

/*m apb_target_uart_minimal */
extern module apb_target_uart_minimal( clock clk,
                                input bit reset_n,

                                input  t_apb_request  apb_request  "APB request",
                                output t_apb_response apb_response "APB response",

                                input    t_uart_rx_data uart_rx,
                                output   t_uart_tx_data uart_tx,
                                output   t_uart_status  status
    )
{
    timing to   rising clock clk apb_request;
    timing from rising clock clk apb_response;
    timing from rising clock clk uart_tx, status;
    timing to   rising clock clk uart_rx;
}

/*m apb_target_dprintf_uart */
extern module apb_target_dprintf_uart( clock clk,
                                input bit reset_n,

                                input  t_apb_request  apb_request  "APB request",
                                output t_apb_response apb_response "APB response",

                                input t_dprintf_req_4   dprintf_req  "Debug printf request",
                                output bit              dprintf_ack  "Debug printf acknowledge",
                                
                                output bit              uart_txd
    )
{
    timing to   rising clock clk apb_request;
    timing from rising clock clk apb_response;
    timing to   rising clock clk dprintf_req;
    timing from rising clock clk dprintf_ack;
    timing from rising clock clk uart_txd;

}

/*m apb_target_i2c_master */
extern module apb_target_i2c_master( clock clk         "System clock",
                              input bit reset_n "Active low reset",

                              input  t_apb_request  apb_request  "APB request",
                              output t_apb_response apb_response "APB response",

                              input  t_i2c       i2c_in "Pin values in",
                              output t_i2c       i2c_out "Pin values to drive - 1 means float high, 0 means pull low"
    )
{
    timing to   rising clock clk apb_request;
    timing from rising clock clk apb_response;
    timing to   rising clock clk i2c_in;
    timing from rising clock clk i2c_out;
}

/*m apb_target_axi4s */
extern module apb_target_axi4s( clock clk         "System clock",
                         input bit reset_n "Active low reset",

                         input  t_apb_request  apb_request  "APB request",
                         output t_apb_response apb_response "APB response",

                         output t_sram_access_req  tx_sram_access_req  "SRAM access request",
                         input  t_sram_access_resp tx_sram_access_resp "SRAM access response",

                         output t_sram_access_req  rx_sram_access_req  "SRAM access request",
                         input  t_sram_access_resp rx_sram_access_resp "SRAM access response",

                         input bit        tx_axi4s_tready,
                         output t_axi4s32 tx_axi4s,
                         input t_axi4s32  rx_axi4s,
                         output bit       rx_axi4s_tready
    )
{
    timing to   rising clock clk tx_axi4s_tready;
    timing from rising clock clk tx_axi4s;
    timing from rising clock clk rx_axi4s_tready;
    timing to   rising clock clk rx_axi4s;
    timing from rising clock clk apb_response;
    timing to   rising clock clk apb_request;
    timing from rising clock clk rx_sram_access_req, tx_sram_access_req;
    timing to   rising clock clk rx_sram_access_resp, tx_sram_access_resp;
}

/*m apb_target_axi4s */
extern module apb_target_analyzer( clock analyzer_clock,
                            clock async_trace_read_clock,
                            clock apb_clock,

                            input bit reset_n,

                            input  t_apb_request  apb_request  "APB request",
                            output t_apb_response apb_response "APB response",

                            output bit trace_ready,
                            output bit trace_done,

                            output bit[32]analyzer_mux_control,
                            input bit[32]internal_signal_in,

                            input bit ext_trigger_reset,
                            input bit ext_trigger_enable,

                            input bit async_trace_read_enable,
                            output bit async_trace_valid_out,
                            output bit[32] async_trace_out )
{
    timing to   rising clock apb_clock apb_request;
    timing from rising clock apb_clock apb_response, analyzer_mux_control;

    timing from rising clock analyzer_clock trace_ready, trace_done;
    timing to   rising clock analyzer_clock internal_signal_in;
    timing to   rising clock analyzer_clock ext_trigger_reset, ext_trigger_enable;

    timing to   rising clock async_trace_read_clock async_trace_read_enable;
    timing from rising clock async_trace_read_clock async_trace_valid_out, async_trace_out;
}

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/


