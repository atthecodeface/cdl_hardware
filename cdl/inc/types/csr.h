/** @copyright (C) 2016-2017,  Gavin J Stark.  All rights reserved.
 *
 * @copyright
 *    Licensed under the Apache License, Version 2.0 (the "License");
 *    you may not use this file except in compliance with the License.
 *    You may obtain a copy of the License at
 *     http://www.apache.org/licenses/LICENSE-2.0.
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 *
 * @file   csr_interface.h
 * @brief  Types and modules for the CSR interface
 *
 * Header file for the types and modules in the pipelined CSR
 * interface, including APB target to CSR master, CSR target to APB
 * master, and CSR target to simple CSR access.
 *
 */

/*a Types */
/*t t_csr_request */
/**
 * This is the request structure for the pipelined CSR interface.
 *
 * A valid request has @a valid asserted; this must remain asserted
 * until @a acknowledge is seen in response; another request must not
 * be driven until @a acknowledge is seen to be low.
 *
 * A valid request has read_not_write (1 for read, 0 for write);
 * select (a 16-bit field) and address (a 16-bit field).
 *
 * For write requests the data is up to 64 bits - although many
 * registers are shorter.
 *
 * For read responses a valid request will return a @a read_data_valid
 * signal with valid @a read_data.
 *
 * This structure should be driven by:
 *
 *   csr_master_apb
 *     In response to an APB, this masters the CSR pipelined interface
 *  
 * This structure should terminate (as leaves) in one or more of:
 *
 *   csr_target_csr
 *     Provides a t_csr_access to a target
 *
 *   csr_target_apb
 *     Provides an APB interface to a target
 *
 *   csr_target_timeout
 *     Automatically times out transactions if the bus hangs for a while
 *
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
    bit acknowledge;
    bit read_data_valid;
    bit read_data_error;
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


