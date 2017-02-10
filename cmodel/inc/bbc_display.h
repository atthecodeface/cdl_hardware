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
 * @file   bbc_display.h
 * @brief  BBC display header file
 *
 * Header file for BBC display C model
 *
 */
/*a Wrapper */
#ifndef __INC_BBC_DISPLAY
#define __INC_BBC_DISPLAY

/*a Includes */
#include "sl_general.h"

/*a Types */
/*t t_bbc_pixels_per_clock */
/**
 * Pixels per clock is used to describe the number of pixels that are
 * valid per 2MHz video clock out of the BBC microcomputer.
 */
typedef enum {
    bbc_ppc_1,
    bbc_ppc_2,
    bbc_ppc_4,
    bbc_ppc_6,
    bbc_ppc_8,
} t_bbc_pixels_per_clock;

/*t t_keys_down */
/**
 * The BBC micro keyboard has a matrix of 10 columns of 8 rows of
 * keys. This structure supports a single bit per key indicating that
 * it is down. Column 0 data is held in the bottom eight bits of
 * cols_0_to_7, with row 0 at bit 0 of that. Column 1 is then at the
 * next eight bits up, and so on.
 */
typedef struct t_keys_down {
    t_sl_uint64 cols_0_to_7;
    t_sl_uint64 cols_8_to_9;
} t_keys_down;

/*t t_framebuffer_and_keys */
/** 
 * This structure is used to contain the data for a BBC microcomputer
 * simulation that is shared between more than one process, using
 * shared memory. The structure is placed at the start of the shared
 * memory and it provides for key infomation, reset being pressed (the
 * BBC 'Break' key) and the display framebuffer contents (as 32-bit
 * ARGB) and metrics.
 */
typedef struct t_framebuffer_and_keys {
    t_keys_down keys_down;
    int width;
    int height;
    int data_size;
    int interlaced;
    int field;
    int h_front_porch;
    int v_front_porch;
    int reset_pressed;
    struct t_framebuffer_and_keys *fbk; // only in the local memory instance, points to shm
    int fb_data[1]; // real data pointer is local fbk.fbk->fb_data
} t_framebuffer_and_keys;

/*t t_bbc_csr_request */
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
 */
typedef struct t_bbc_csr_request {
    /** Asserted to indicate a valid request; remains asserted until
     * an 'ack' is seen in response **/
    int valid;
    /** Asserted for reads, deasserted for writes, and held constant
     * while valid is asserted **/
    int read_not_write;
    /** Select bus with a t_bbc_csr_select enumeration value, held
     * constant while valid is asserted **/
    int select;
    /** Address bus indicating which register is to be accessed, held
     * constant while valid is asserted **/
    int address;
    /** Data to be written on a write access, held constant while valid
     * is asserted **/
    t_sl_uint64 data;
} t_bbc_csr_request;

/*t t_bbc_csr_response */
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
typedef struct t_bbc_csr_response {
    /** Asserted to indicate that a CSR request has been taken - held
     * high until valid is deasserted **/
    int ack;
    /** Asserted when the read data from a CSR request is valid **/
    int read_data_valid;
    /** Read data from a CSR request, valid with read_data_valid, zero
     * in all other cycles **/
    t_sl_uint64 read_data;
} t_bbc_csr_response;

/*t t_bbc_sram_response */
/**
 * The response from the BBC micro SRAM request system
 */
typedef struct t_bbc_sram_response {
    /** Asserted to indicate that a SRAM request has been taken - held
     * high until valid is deasserted **/
    int ack;
    /** Asserted when the read data from an SRAM request is valid **/
    int read_data_valid;
    /** Read data from an SRAM request, valid with read_data_valid, zero
     * in all other cycles **/
    t_sl_uint64 read_data;
} t_bbc_sram_response;

/*t t_bbc_csr_select */
/**
 * This enumeration matches the CDL, and it is used to select the CSR
 * target (the 'select' field of csr_request's).
 */
typedef enum {
    bbc_csr_select_clocks = 0,
    bbc_csr_select_display = 1,
    bbc_csr_select_floppy = 2,
    bbc_csr_select_keyboard = 3,
    bbc_csr_select_framebuffer = 4,
} t_bbc_csr_select;

/*t t_bbc_sram_select */
/**
 * This enumeration matches the CDL, and it is used to select the SRAM
 * target for host SRAM transactions
 */
typedef enum {
    bbc_sram_select_micro = 0,
    bbc_sram_select_display = 1,
    bbc_sram_select_floppy = 2,
    bbc_sram_select_cpu       = 16,
    bbc_sram_select_cpu_ram_0 = 16,
    bbc_sram_select_cpu_ram_1 = 17,
    bbc_sram_select_cpu_os    = 18,
    bbc_sram_select_cpu_teletext = 20,
    bbc_sram_select_cpu_rom_0 = 24,
    bbc_sram_select_cpu_rom_1 = 25,
    bbc_sram_select_cpu_rom_2 = 26,
    bbc_sram_select_cpu_rom_3 = 27,
} t_bbc_sram_select;

/*a Wrapper */
#endif

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
