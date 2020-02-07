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
 * @file   encoders.h
 * @brief  Modules for various encoders (generally for networking)
 *
 * Header file for encoder modules
 *
 */

/*a Includes */
include "types/ethernet.h"
include "types/apb.h"
include "types/axi.h"
include "types/timer.h"
include "types/networking.h"

/*a Modules */
/*m gbe_axi4s32 */
extern module gbe_axi4s32( clock tx_aclk   "Transmit clock domain - AXI-4-S and GMII TX clock",
                           input bit tx_areset_n,
                           input t_axi4s32 tx_axi4s,
                           output bit      tx_axi4s_tready,
                           input   bit gmii_tx_enable "Clock enable for tx_aclk for GMII",
                           output  t_gmii_tx gmii_tx,
                           output t_packet_stat tx_packet_stat "Packet statistic when packet completes tx",
                           input  bit           tx_packet_stat_ack "Ack for packet statistic",

                           clock rx_aclk    "Receive clock domain - AXI-4-S and GMII RX clock",
                           input bit rx_areset_n,
                           output t_axi4s32 rx_axi4s,
                           input bit        rx_axi4s_tready,
                           input   bit gmii_rx_enable "Clock enable for rx_aclk for GMII",
                           input   t_gmii_rx gmii_rx,
                           output t_packet_stat rx_packet_stat "Packet statistic when packet completes rx",
                           input  bit           rx_packet_stat_ack "Ack for packet statistic",
                           
                           input t_timer_control rx_timer_control "Timer control in TX clock domain"
    )
{
    timing to   rising clock tx_aclk tx_axi4s, gmii_tx_enable;
    timing from rising clock tx_aclk tx_axi4s_tready, gmii_tx;
    timing from rising clock tx_aclk tx_packet_stat;
    timing to   rising clock tx_aclk tx_packet_stat_ack;

    timing to   rising clock rx_aclk rx_axi4s_tready, gmii_rx, gmii_rx_enable;
    timing from rising clock rx_aclk rx_axi4s;
    timing from rising clock rx_aclk rx_packet_stat;
    timing to   rising clock rx_aclk rx_packet_stat_ack;
    timing to   rising clock rx_aclk rx_timer_control;
}

/*m gbe_single - Single GbE with SGMII and APB target to control them */
extern module gbe_single( clock clk,
                   input bit reset_n,

                   input  t_axi4s32    tx_axi4s        "AXI-4-S bus for transmit data",
                   output bit          tx_axi4s_tready "Tready signal to ack transmit AXI-4-S bus",
                   input  bit          gmii_tx_enable  "Clock enable for clk for GMII if NOT using SGMII/TBI",
                   output t_gmii_tx    gmii_tx         "GMII Tx bus (on clk valid with gmii_tx_enable, not needed if using SGMII/TBI)",
                   output t_tbi_valid  tbi_tx          "TBI Tx bus (on clk, not needed if using SGMII)",

                   output t_axi4s32    rx_axi4s,
                   input  bit          rx_axi4s_tready,
                   input  bit          gmii_rx_enable    "Clock enable for clk for GMII if NOT using SGMII/TBI",
                   input  t_gmii_rx    gmii_rx           "GMII Rx bus (on clk valid with gmii_rx_enable, tie low if using GMII or TBI",
                   input  t_tbi_valid  tbi_rx            "TBI Rx bus (on clk, tie low if using GMII or SGMII)",
                    
                   input t_timer_control timer_control "Timer control - tie all low if no timestamp required - sync to clk",

                   input  t_apb_request  apb_request  "APB request",
                   output t_apb_response apb_response "APB response",

                   clock     sgmii_tx_clk       "Four-bit transmit serializing data clock (312.5MHz) - required for SGMII and TBI",
                   input bit sgmii_tx_reset_n   "Reset deasserting sync to sgmii_tx_clk - tie low if SGMII not being used",
                   output bit[4] sgmii_txd      "First bit for wire in txd[0]",

                   clock     sgmii_rx_clk       "Four-bit receive serializing data clock (312.5MHz) - required for SGMII and TBI",
                   input bit sgmii_rx_reset_n   "Reset deasserting sync to sgmii_rx_clk - tie low if SGMII not being used",
                   input bit[4] sgmii_rxd       "Oldest bit in rxd[0] - tie low if SGMII not being used",

                   input t_sgmii_transceiver_status    sgmii_transceiver_status   "Status from transceiver, on sgmii_rx_clk; wire low if SGMII not being used",
                   output  t_sgmii_transceiver_control sgmii_transceiver_control  "Control of transceiver, on sgmii_rx_clk"
    )
{
    timing to   rising clock clk tx_axi4s;
    timing from rising clock clk tx_axi4s_tready, gmii_tx;
    timing to   rising clock clk rx_axi4s_tready;
    timing from rising clock clk rx_axi4s;

    timing to   rising clock clk gmii_tx_enable;    
    timing from rising clock clk gmii_tx, tbi_tx;
    timing to   rising clock clk gmii_rx, tbi_rx, gmii_rx_enable;

    timing to   rising clock clk timer_control;
    timing to   rising clock clk apb_request;
    timing from rising clock clk apb_response;

    timing from rising clock sgmii_tx_clk sgmii_txd;
    timing to   rising clock sgmii_rx_clk sgmii_rxd;

    timing to   rising clock sgmii_rx_clk sgmii_transceiver_status;
    timing from rising clock sgmii_rx_clk sgmii_transceiver_control;
}

