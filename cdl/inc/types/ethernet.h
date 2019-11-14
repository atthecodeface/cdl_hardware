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
 * @file   ethernet.h
 * @brief  Types for various ethernet standards
 *
 */

/*a Includes */
include "types/clocking.h"

/*a Types */
/*t t_gmii_tx */
typedef struct {
    bit tx_en;
    bit tx_er;
    bit [8] txd;
} t_gmii_tx;

/*t t_gmii_rx */
typedef struct {
    bit rx_dv;
    bit rx_er;
    bit rx_crs "Generally unused for GbE";
    bit [8] rxd;
} t_gmii_rx;

/*t t_gmii_op */
typedef enum[3] {
    gmii_op_idle,
    gmii_op_data,
    gmii_op_transmit_error,
    gmii_op_carrier_extend,
    gmii_op_carrier_extend_error,
    gmii_op_low_power_idle,
    gmii_op_unknown
} t_gmii_op;

/*t t_tbi_valid */
typedef struct {
    bit valid;
    bit[10] data;
} t_tbi_valid;
/*t t_sgmii_gasket_status */
typedef struct {
    bit rx_sync;
    bit rx_sync_toggle;
    bit[32] rx_symbols_since_sync;
    bit[16] an_config "Autonegotiation configuration";
    bit[32] an_state;
} t_sgmii_gasket_status;

/*t t_sgmii_gasket_control */
typedef struct {
    bit     write_config;
    bit[4]  write_address;
    bit[32] write_data;
} t_sgmii_gasket_control;

/*t t_sgmii_transceiver_status */
typedef struct {
    t_phase_measure_response measure_response;
    t_eye_track_response     eye_track_response;
} t_sgmii_transceiver_status;

/*t t_sgmii_transceiver_control */
typedef struct {
    bit     valid;
} t_sgmii_transceiver_control;
