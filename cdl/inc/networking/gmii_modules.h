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
 * @file   gmii_modules.h
 * @brief  Modules for GMII modules
 *
 * Header file for GMII modules
 *
 */

/*a Includes */
include "types/ethernet.h"

/*a Modules */
extern module sgmii_gmii_gasket( clock tx_clk   "Transmit clock domain - must be at least 2/5 of the serial clock speed",
                                 clock tx_clk_312_5 "Four-bit transmit serializing data clock",
                                 clock rx_clk   "Receive clock domain - must be at least 2/5 of the serial clock speed",
                                 clock rx_clk_312_5,
                                 input bit tx_reset_n,
                                 input bit tx_reset_312_5_n,
                                 input bit rx_reset_n,
                                 input bit rx_reset_312_5_n,

                                 input t_gmii_tx gmii_tx,
                                 output bit gmii_tx_enable "With a 2/5 tx_clk to tx_clk_312_5 this will never gap",
                                 output t_tbi_valid tbi_tx "Optional TBI instead of SGMII",
                                 output bit[4] sgmii_txd,
                                 
                                 input bit[4] sgmii_rxd,
                                 input t_tbi_valid tbi_rx "Optional TBI instead of SGMII",
                                 output bit gmii_rx_enable "With a 2/5 rx_clk to rx_clk_312_5 this will never gap",
                                 output t_gmii_rx gmii_rx
    )
{
    timing to   rising clock tx_clk       gmii_tx;
    timing from rising clock tx_clk       gmii_tx_enable, tbi_tx;
    timing from rising clock tx_clk_312_5 sgmii_txd;

    timing to   rising clock rx_clk_312_5 sgmii_rxd;
    timing to   rising clock rx_clk       tbi_rx;
    timing from rising clock rx_clk       gmii_rx_enable;
    timing from rising clock rx_clk       gmii_rx;
}

