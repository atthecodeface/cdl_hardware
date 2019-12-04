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
include "types/axi.h"
include "types/timer.h"

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
