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
 * @file   I2C.h
 * @brief  I2C signals
 *
 * Header file for the types for I2C signals
 *
 */

/*a Types */
/*t t_i2c_action_type - from i2c_interface
 *
 * Transactions are Start -> Ready -> [Bit Start -> Bit End]* -> [Start -> Ready -> [Bit Start -> Bit End]*]* -> Stop
 */
typedef enum [3] {
    i2c_action_none        "No event",
    i2c_action_start       "Start of transaction - bit_num and is_ack are invalid",
    i2c_action_stop        "Stop transaction",
    i2c_action_ready       "SCL low after start ready for start bit - bit_num and is_ack are invalid",
    i2c_action_bit_start   "Start bit - capture the bit value here - bit_num and is_ack are valid",
    i2c_action_bit_end     "End of bit - this is the time to use the bit data - bit_num and is_ack are same as for bit_start",
    i2c_action_timeout     "Timeout occurred",
} t_i2c_action_type;

/*t t_i2c_action - from i2c_interface
 *
 * I2C action
 */
typedef struct {
    bit               is_busy "Asserted if the I2C interface is busy";
    t_i2c_action_type action;
    bit               bit_value;
    bit[3]            bit_num;
    bit               is_ack;
    bit               period_enable "Use as an enable for periods for hold";
} t_i2c_action;

/*t t_i2c_slave_request */
typedef struct {
    bit valid;
    bit read_not_write;
    bit    first;
    bit[7] device;
    bit[8] data;
} t_i2c_slave_request;

/*t t_i2c_slave_response */
typedef struct {
    bit    ack   "Asserted for writes when they are taken, and for reads when data is valid";
    bit[8] data  "Result of last read - must be held steady until next request";
} t_i2c_slave_response;

/*t t_i2c_master_request */
typedef struct {
    // Need a way to force reset of state machine and master
    bit valid;
    bit cont "If asserted then do not issue a stop at the end but prepare for repeated start";
    bit[3]  num_out "From 1 to 4";
    bit[3]  num_in  "From 0 to 4";
    bit[32] data;
} t_i2c_master_request;

/*t t_i2c_master_response_type */
typedef enum[3] {
    i2c_master_response_okay = 0,
    i2c_master_response_arbitration_fail = 1,
    i2c_master_response_no_acknowledge   = 2,
    i2c_master_response_timeout          = 3,
    i2c_master_response_protocol_error   = 4
} t_i2c_master_response_type;
        
/*t t_i2c_master_response */
typedef struct {
    bit    ack   "Asserted for writes when they are taken, and for reads when data is valid";
    bit    in_progress "A transaction is in progress";
    bit    response_valid "Asserted for one cycle as in_progress goes low";
    t_i2c_master_response_type response_type "Response for last transaction - invalid if in_progress";
    bit[32] data  "Result of last read - must be held steady until next request";
} t_i2c_master_response;

/*t t_i2c_master_conf */
typedef struct {
    bit[4] data_hold_delay  "Delay in periods for data change after falling clock";
    bit[4] data_setup_delay "Delay in periods betwween data change and rising clock";
    bit[4] period_delay     "Delay in periods for other timings";
} t_i2c_master_conf;

/*t t_i2c_slave_select */
typedef struct {
    bit[7] value;
    bit[7] mask;
} t_i2c_slave_select;

/*t t_i2c_conf */
typedef struct {
    bit[8] divider "Clock divider to generate internal clock for capturing edges etc (e.g. 100ns or 10MHz)";
    bit[8] period  "Divide value to divide internal clock to a period of (e.g.) 500ns for standard I2C";
} t_i2c_conf;

/*t t_i2c - open drain on output, so no enables */
typedef struct {
    bit scl;
    bit sda;
} t_i2c;
