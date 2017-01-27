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
 * @file   bbc_floppy.h
 * @brief  BBC floppy drive model header file
 *
 * Header file for BBC floppy drive
 *
 */

/*a Wrapper */
#ifndef __INC_BBC_FLOPPY
#define __INC_BBC_FLOPPY

/*a Includes */
#include "sl_general.h"

/*a Types */
/*t t_bbc_floppy_sector_id */
/**
 * This structure is used in the request and response to a floppy
 * drive from the FDC (floppy disk controller), for the ID
 * read/written to a sector.
 *
 * Each sector on a floppy has a descriptor that includes byte fields
 * for the head, logical sector number, and the head/sector length
 * and, and a CRC - and the sector data has its own CRC.
 */
typedef struct t_bbc_floppy_sector_id {
    t_sl_uint64 track;
    t_sl_uint64 head;
    t_sl_uint64 sector_number;
    t_sl_uint64 sector_length;
    t_sl_uint64 bad_crc;
    t_sl_uint64 bad_data_crc;
    t_sl_uint64 deleted_data;
} t_bbc_floppy_sector_id;

/*t t_bbc_floppy_op */
/**
 * The floppy op structure is used to convey a floppy operation from
 * the FDC to the floppy drive; it is effectively an internal set of
 * signals that are driven inside the FDC to the floppy controller,
 * which converts them to analog data or other control signals to the
 * floppy drive interface.
 *
 * The structure has no 'valid' signal - it is valid on every clock
 * tick. However, control signals are required to toggle on and toggle
 * off - it is the 'rising edge' of step_out, step_in, next_id,
 * read_data_enable, etc that cause those to occur.
 *
 * step_out and step_in are mutually exclusive; step_out moves the
 * head out towards the outer rim of the disk, which is where track 0
 * is.
 *
 * next_id is asserted if the drive should read the next sector ID (in
 * reality waiting for the disk to spin round until a sector id
 * descriptors is decoded from the surface) from the disk. In response
 * to this, some time later, a floppy response with a valid sector_id
 * should be presented.
 *
 * read_data_enable is asserted if the next word (32 bits) of sector
 * data should be read from the disk surface. This should only be
 * asserted after a 'next_id', or after a previous
 * 'read_data_enable'. After a 'next_id' it causes the first data word
 * of the sector for which the sector id was returned; otherwise it
 * continues data from that sector.
 *
 * write_data_enable and write_data are not currently used. They
 * should be used to write the data after a 'next_id' has been
 * asserted, at 32 bits per write.
 *
 * write_sector_id_enable and sector_id are not currently used. They
 * should be used to write the sector id data for a sector. This is
 * generally done on a floppy disk controller only when formatting a
 * track, and so in fact may never be implemented (if formatting is
 * assumed to be hard as opposed to soft).
 *
 */
typedef struct {
    t_sl_uint64 step_out; // towards track 0
    t_sl_uint64 step_in;
    t_sl_uint64 next_id;
    t_sl_uint64 read_data_enable;
    t_sl_uint64 write_data_enable;
    t_sl_uint64 write_data;
    t_sl_uint64 write_sector_id_enable;
    t_bbc_floppy_sector_id sector_id;
} t_bbc_floppy_op;

/*t t_bbc_floppy_response */
/**
 * The floppy response structure conveys data back from the floppy
 * drive interface to the FDC in response to the floppy operation.
 *
 * sector_id_valid is asserted for a single clock tick in conjunction
 * with valid sector_id data in response to a 'next_id' rising edge in
 * the floppy operation; this may occur any number of clock ticks
 * after the request, and in the intervening period no other requests
 * are permitted.
 *
 * read_data_valid is asserted for a single clock tick in conjunction
 * with valid read_data in response to a 'read_data_enable' floppy
 * operation; this may occur any number of clock ticks after the
 * request, and in the intervening period no other requests are
 * permitted.
 *
 * index is asserted if the latest sector_id is the first physical
 * sector of the track - i.e. if the 'index hole' on the floppy disk
 * is at that point. On a real floppy disk the index hole need not be
 * anywhere near an actual valid sector data field, but for the
 * emulation the index value is valid for the whole of the period from
 * one sector_id_valid to the next.
 * 
 * track_zero is asserted if the current track is track zero. This
 * becomes asserted when the drive is 'stepped out' to the outermost
 * track (i.e. the physical track number is decremented to 0).
 *
 * disk_ready is asserted if there is a floppy in the drive.
 * 
 * write_protect is asserted if the floppy in the drive has a write
 * protect tab on it.
 * 
 */
typedef struct {
    t_sl_uint64 sector_id_valid;
    t_bbc_floppy_sector_id sector_id;
    t_sl_uint64 index; // assert if sector_id is the first sector of the track
    t_sl_uint64 read_data_valid;
    t_sl_uint64 read_data;
    t_sl_uint64 track_zero;    // assert if the current track is track 0
    t_sl_uint64 write_protect; // assert if the disk is write protected (independent of valid)
    t_sl_uint64 disk_ready;    // assert if the disk is loaded (independent of valid)
} t_bbc_floppy_response;

/*t t_bbc_floppy_sram_request */
/**
 * To implement the floppy drive there is a CDL implementation which
 * takes floppy operations and converts them to SRAM reads (and
 * writes); this is a standard SRAM access request interface.
 */
typedef struct {
    t_sl_uint64 enable;
    t_sl_uint64 read_not_write;
    t_sl_uint64 address;
    t_sl_uint64 data;
} t_bbc_floppy_sram_request;

/*t t_bbc_floppy_sram_response */
/**
 * The CDL implementation for the floppy drive uses this as a response
 * - ack asserts to acknowledge a read or write request, and valid
 * read data is returned with data_valid.
 */
typedef struct {
    t_sl_uint64 ack;
    t_sl_uint64 data_valid;
    t_sl_uint64 data;
} t_bbc_floppy_sram_response;

/*a Wrapper */
#endif

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
