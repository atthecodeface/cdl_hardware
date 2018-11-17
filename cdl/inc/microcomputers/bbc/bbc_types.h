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
 * @file   bbc_micro_types.h
 * @brief  BBC micro types header file for CDL
 *
 * Header file for the types shared by more than one CDL module for
 * the BBC micro implementation
 *
 */

/*a Types */
/*t t_bbc_keyboard */
/**
 * The BBC keyboard consists of a keyboard matrix with ten columns of
 * eight rows of keys. The columns can be individually powered, and
 * then the eight rows can be read as a byte to see which of the
 * column's keys is pressed. There is an additional 'Break' key that
 * is independent of the keyboard matrix, that provides a reset signal
 * to the motherboard.
 *
 * This structure is used to pass the keyboard state in to the BBC
 * micro implementation - since an ASIC of FPGA does not contain a
 * physical keyboard, the key pressed information needs to be conveyed
 * over a bus from outside. This structure permits this.
 */
typedef struct {
    bit reset_pressed;        
    bit[64] keys_down_cols_0_to_7;
    bit[16] keys_down_cols_8_to_9;
} t_bbc_keyboard;

/*t t_bbc_pixels_per_clock */
/**
 * The BBC micro operates with a variable speed pixel clock - it can
 * be 12MHz or 16MHz. Furthermore, for some graphics 'modes' the
 * number of real pixels per clock tick drops as pixels are
 * replicated, to enable pixel information to be used for color
 * selection. Hence 8 pixel per clock at 2MHz is 2 colors for 16Mpps,
 * whereas 2 pixels per clock at 2MHz indicates 16Mpps where each
 * pixel is replicated 4 times over, and can be of 2^4=16 different
 * colors. Mode 2 uses bbc_ppc_2; modes 1 and 5 use bbc_ppc_4; modes
 * 0, 3, 4 and 6 use bbc_ppc_8. Note that modes 0-3 run with 640 base
 * pixels at 16MHz, hence 40us of pixel data per row.
 *
 * For teletext mode the pixel rate is officially 12Mpps, as the
 * teletext characters are 12 pixels wide and there are 40 characters
 * per screen (hence roughly 480 pixels wide, and at 12Mpps that is
 * 40us).
 */
typedef enum[3] {
    bbc_ppc_1,
    bbc_ppc_2,
    bbc_ppc_4,
    bbc_ppc_6,
    bbc_ppc_8,
} t_bbc_pixels_per_clock;

/*t t_bbc_display */
/**
 * The BBC micro output from its video ULA is separate red, green and
 * blue pixel data, and sync signals. This structure conveys this
 * information out of the BBC implementation, plus the number of
 * pixels per clock, so that the display interface may be clocked at
 * 2MHz. For modes where there are fewer than 8 pixels per clock, the
 * red, green and blue data is replicated throughout the bus - so the
 * only real need for pixels_per_clock is to indicate if the pixel
 * clock rate is 12MHz or 16MHz (it is 12MHz if bbc_ppc_6)
 */
typedef struct {
    bit clock_enable;
    bit hsync;
    bit vsync;
    t_bbc_pixels_per_clock pixels_per_clock;
    bit[8] red;
    bit[8] green;
    bit[8] blue;
} t_bbc_display;

/*t t_bbc_display_sram_write */
/**
 * To ease implementation of display framebuffers in target hardware
 * there is a CDL module supplied called 'bbc_display_sram'. This
 * module converts from a t_bbc_display structure to a 3bpp frame
 * buffer (RGB per pixel). The output from this module is therefore a
 * stream of SRAM write transactions, each of 16 pixels.
 *
 * The module itself is configured through a CSR request interface to
 * set the base address of the frame buffer (amongst other things).
 *
 * This bus does not have an equivalent 'response' bus; there is no
 * way to back-pressure the BBC video subsystem, hence no way to
 * back-pressure the display SRAM writes.
 */
typedef struct {
    bit enable;
    bit[48] data;
    bit[16] address;
} t_bbc_display_sram_write;

/*t t_bbc_floppy_sector_id */
/**
 * This structure is used in the request and response to a floppy
 * drive from the FDC (floppy disc controller), for the ID
 * read/written to a sector.
 *
 * Each sector on a floppy has a descriptor that includes byte fields
 * for the head, logical sector number, and the head/sector length
 * and, and a CRC - and the sector data has its own CRC.
 *
 * This structure fits into 32 bits, so a 32-bit wide SRAM can store
 * this data.
 */
typedef struct {
    bit[7] track;
    bit    head;
    bit[6] sector_number;
    bit[2] sector_length;
    bit    bad_crc;
    bit    bad_data_crc;
    bit    deleted_data;
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
 * head out towards the outer rim of the disc, which is where track 0
 * is.
 *
 * next_id is asserted if the drive should read the next sector ID (in
 * reality waiting for the disc to spin round until a sector id
 * descriptors is decoded from the surface) from the disc. In response
 * to this, some time later, a floppy response with a valid sector_id
 * should be presented.
 *
 * read_data_enable is asserted if the next word (32 bits) of sector
 * data should be read from the disc surface. This should only be
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
 * generally done on a floppy disc controller only when formatting a
 * track, and so in fact may never be implemented (if formatting is
 * assumed to be hard as opposed to soft).
 *
 */
typedef struct {
    bit    step_out; // towards track 0
    bit    step_in;
    bit    next_id;
    bit    read_data_enable;
    bit    write_data_enable;
    bit[32] write_data;
    bit    write_sector_id_enable;
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
 * sector of the track - i.e. if the 'index hole' on the floppy disc
 * is at that point. On a real floppy disc the index hole need not be
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
    bit sector_id_valid;
    t_bbc_floppy_sector_id sector_id;
    bit                   index; // assert if sector_id is the first sector of the track
    bit     read_data_valid;
    bit[32] read_data;
    bit    track_zero;    // assert if the current track is track 0
    bit    write_protect; // assert if the disk is write protected (independent of valid)
    bit    disk_ready;    // assert if the disk is loaded (independent of valid)
} t_bbc_floppy_response;

/*t t_bbc_floppy_sram_request */
/**
 * To implement the floppy drive there is a CDL implementation which
 * takes floppy operations and converts them to SRAM reads (and
 * writes); this is a standard SRAM access request interface.
 */
typedef struct {
    bit enable;
    bit read_not_write;
    bit[20] address;
    bit[32] write_data;
} t_bbc_floppy_sram_request;

/*t t_bbc_floppy_sram_response */
/**
 * The CDL implementation for the floppy drive uses this as a response
 * - ack asserts to acknowledge a read or write request, and valid
 * read data is returned with data_valid.
 */
typedef struct {
    bit ack;
    bit read_data_valid;
    bit[32] read_data;
} t_bbc_floppy_sram_response;

/*t t_bbc_clock_control */
/**
 * This structure conveys clock gating and reset information to the
 * BBC micro CDL implementation and various peripherals and other
 * logic. Other modules require it to determine when to clock: for
 * example, the floppy disc controller clocks on the CPU clock, so the
 * interface from this module to its SRAM also clocks at the same
 * edges (i.e. clk gated by enable_cpu).
 */
typedef struct {
    bit enable_cpu               "Asserted if the rising edge of 'clk' should also be a rising CPU clock edge";
    bit will_enable_2MHz_video   "Asserted if 'enable_2MHz_video' will be asserted in the next 'clk' period";
    bit enable_2MHz_video        "Asserted if the rising  edge of 'clk' should also be a rising video '2MHz' clock edge";
    bit enable_1MHz_rising       "Asserted if the rising  edge of 'clk' should also be a rising '1MHz' clock edge";
    bit enable_1MHz_falling      "Asserted if the rising  edge of 'clk' should also be a falling '1MHz' clock edge";
    bit[2] phi                   "Phase of BBC 6502 clock operation - in a real BBC micro this comes from the CPU";
    bit reset_cpu                "Asserted if the CPU should be reset, controlled by a CSR register";
    bit[4] debug;
} t_bbc_clock_control;

/*t t_bbc_clock_status */
/**
 * This structure conveys information in to the clock control module
 * from the BBC micro - the real BBC micro has complex management of
 * the CPU and hence system bus clock based on whether a 1MHz
 * peripheral I/O space is being accessed or not.
 */
typedef struct {
    bit cpu_1MHz_access "Asserted by the BBC micro if a 1MHz peripheral is being accessed - this the CPU clock enables to align with the 1MHz clock enables";
} t_bbc_clock_status;

/*t t_bbc_micro_sram_request */
/**
 * This structure is used to enable writing and reading any SRAM
 * within a CDL implementation; it is a bus that can be pipelined
 * arbitrarily (both in request and response), and it may be split
 * amongst multiple targets (hence it can be set up as a pipelined
 * tree, with the master at the root).
 *
 * The protocol is for the master to assert valid with the required
 * request on the bus. The master must wait for an 'ack' from a target
 * to reach it, when it may then remove the 'valid' (for at least one
 * cycle). If the request has been a read, then the master must also
 * wait for 'read_data_valid' - which may occur in the same cycle as
 * the 'ack'.
 *
 * Before issuing another SRAM transaction the master must wait for
 * 'ack' to go low.
 *
 * A target receiving a valid request should compare the 'select'
 * lines with the SRAMs that it services, and assert 'ack' if it can
 * handle the request. It then performs the transaction, and returns
 * any read data with the 'read_data_valid' signal asserted. In every
 * cycle that it does not have valid read_data the read_data and
 * read_data_valid must be 0.
 *
 * The target may wait for valid to be deasserted before deasserting
 * 'ack' (if it had been the selected target).
 */
typedef struct {
    bit valid            "Asserted to indicate that an SRAM request is valid";
    bit read_enable      "Constant during 'valid', indicates if a read access is required. Exclusive with write_enable";
    bit write_enable     "Constant during 'valid', indicates if a write access is required. Exclusive with read_enable";
    bit[8] select        "Constant during 'valid', indicates which SRAM should be accessed. Usually one of t_bbc_sram_select";
    bit[24] address      "Constant during 'valid', indicates address in SRAM should be accessed.";
    bit[64] write_data   "Constant during 'valid', contains data to be written to SRAM (if write_enable is asserted) - ignored otherwise.";
} t_bbc_micro_sram_request;

/*t t_bbc_micro_sram_response */
/**
 * This structure conveys back towards the host the acknowledgement
 * and any SRAM read data in response to a BBC micro SRAM read/write
 * request.
 */
typedef struct {
    bit ack               "Asserted to indicate that a SRAM request has been taken - held high until valid is deasserted";
    bit read_data_valid   "Asserted when the read data from an SRAM request is valid";
    bit[64] read_data     "Read data from an SRAM request, valid with read_data_valid, zero in all other cycles";
} t_bbc_micro_sram_response;

/*t t_bbc_sram_select */
/**
 * This enumeration matches the C, and it is used to select the SRAM
 * target for host SRAM transactions
 */
typedef enum[8] {
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
/*t t_bbc_csr_select */
/**
 * This enumeration matches the C, and it is used to select the CSR
 * target (the 'select' field of csr_request's).
 */
typedef enum[16] {
    bbc_csr_select_clocks = 0,
    bbc_csr_select_display = 1,
    bbc_csr_select_floppy = 2,
    bbc_csr_select_keyboard = 3,
    bbc_csr_select_framebuffer = 4,
} t_bbc_csr_select;

