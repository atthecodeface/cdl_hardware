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
 * @file   csr_interface.h
 * @brief  Types and modules for the CSR interface
 *
 * Header file for the types and modules in the pipelined CSR
 * interface, including APB target to CSR master, CSR target to APB
 * master, and CSR target to simple CSR access.
 *
 */

/*a Includes */
include "apb.h"

/*a Types */
/*t t_csr_request */
/**
 * The BBC micro implementation is controlled from outside through
 * control register reads and writes implemented by a request
 * interface with this structure (the CSR bus). The bus can be
 * pipelined as much as is required by timing, in both request and
 * response directions.
 *
 * A valid request has 'valid' asserted; this must remain asserted
 * until 'ack' is seen in response.
 *
 * A valid request has read_not_write (1 for read, 0 for write);
 * select (a 16-bit field) and address (a 16-bit field).
 *
 * For write requests the data is up to 64 bits - although many
 * registers are shorter.
 *
 * For read responses a valid request will return a 'data_valid'
 * signal with valid read data.
 *
 * This structure should terminate in a target in a bbc_csr_interface
 * module, which provides a t_csr_access to a target, which is a
 * much simpler interface.
 */
typedef struct {
    bit valid;
    bit read_not_write;
    bit[16] select;
    bit[16] address;
    bit[32] data;
} t_csr_request;

/*t t_csr_response */
/**
 * This is the response structure returning from a target on the CSR
 * bus system back to the master. The 'ack' signal is asserted by a
 * target from the point that the request is detected as valid and
 * serviceable (i.e. a valid request with matching select) until the
 * access is performed. The valid signal should be held high until an
 * acknowledge is seen; it should then be taken low for at least one
 * clock tick.
 *
 * The CSR response from more than one target may be wire-ored
 * together, and pipeline stages may be added as required for timing.
 */
typedef struct {
    bit ack;
    bit read_data_valid;
    bit[32] read_data;
} t_csr_response;

/*t t_csr_access */
/**
 * To simplify design of CSR targets the 'csr_interface' module
 * converts a t_csr_request/t_csr_response interface into this
 * simple CSR access request interface. Doing this hides the
 * complexity of the shared, pipelined CSR request/response bus from
 * the targets, and ensures consistent operation of targets.
 *
 * This access bus has signals that are valid for a single cycle. The
 * access requested must be performed in that cycle. Read data for the
 * access must be provided in the cycle of the request
 * (combinatorially on 'address').
 */
typedef struct {
    bit valid;
    bit read_not_write;
    bit[16] address;
    bit[32] data;
} t_csr_access;

/*t t_csr_access_data */
/**
 * This type conveys a response (in the same cycle as a valid CSR
 * access request) to the csr_interface for a target using that
 * module.
 */
typedef bit[32] t_csr_access_data;


/*a Modules */
/*m csr_target_apb */
extern module csr_target_apb( clock                       clk           "Clock for the CSR interface, possibly gated version of master CSR clock",
                       input bit                reset_n,
                       input t_csr_request      csr_request   "Pipelined csr request interface input",
                       output t_csr_response    csr_response  "Pipelined csr request interface response",
                       output t_apb_request     apb_request   "APB request to target",
                       input t_apb_response     apb_response  "APB response from target",
                       input bit[16]            csr_select    "Hard-wired select value for the client"
    )
{
    timing to   rising clock clk csr_request, csr_select;
    timing from rising clock clk csr_response;

    timing from rising clock clk apb_request;
    timing to   rising clock clk apb_response;
}

/*m csr_target_csr */
extern
module csr_target_csr( clock                       clk           "Clock for the CSR interface, possibly gated version of master CSR clock",
                       input bit                reset_n,
                       input t_csr_request      csr_request   "Pipelined csr request interface input",
                       output t_csr_response    csr_response  "Pipelined csr request interface response",
                       output t_csr_access      csr_access    "Registered CSR access request to client",
                       input  t_csr_access_data csr_access_data "Read data valid combinatorially based on csr_access",
                       input bit[16]            csr_select    "Hard-wired select value for the client"
    )
{
    timing to   rising clock clk csr_request, csr_select;
    timing from rising clock clk csr_response;

    timing from rising clock clk csr_access;
    timing to   rising clock clk csr_access_data;
}

/*m csr_master_apb */
extern
module csr_master_apb( clock                    clk        "Clock for the CSR interface; a superset of all targets clock",
                       input bit                reset_n,
                       input t_apb_request      apb_request   "APB request from master",
                       output t_apb_response    apb_response  "APB response to master",
                       input t_csr_response     csr_response  "Pipelined csr request interface response",
                       output t_csr_request     csr_request   "Pipelined csr request interface output"
    )
{
    timing to   rising clock clk csr_response;
    timing from rising clock clk csr_request;

    timing to   rising clock clk apb_request;
    timing from rising clock clk apb_response;
}

/*m csr_target_timeout */
extern
module csr_target_timeout( clock                       clk           "Clock for the CSR interface, possibly gated version of master CSR clock",
                           input bit                reset_n       "Active low reset",
                           input t_csr_request      csr_request   "Pipelined csr request interface input",
                           output t_csr_response    csr_response  "Pipelined csr request interface response",
                           input bit[16]            csr_timeout   "Number of cycles to wait for until auto-acknowledging a request"
    )
{
    timing to   rising clock clk csr_request, csr_timeout;
    timing from rising clock clk csr_response;
}
