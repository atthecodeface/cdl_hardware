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
 * @file   bbc_submodules.h
 * @brief  BBC micro CDL submodules
 *
 * Header file for the modules required for the BBC micro CDL
 * implementation. It should probably be tidied up to put the SRAMs
 * separately, and to start to pull together a cpu/peripheral CDL
 * module header file of its own. But it will do for now
 *
 */

/*a Includes */
include "csr_interface.h"
include "srams.h"
include "bbc_micro_types.h"
include "framebuffer.h"

/*a Modules */
/*m bbc_vidproc */
extern module bbc_vidproc( clock clk_cpu    "Output on real chip in a sense (2MHz out somewhat)",
                    clock clk_2MHz_video    "Output on real chip, 2MHz video clock",
                    input bit reset_n       "Not present on the chip, but required for the model - power up reset",
                    input bit chip_select_n "Active low chip select",
                    input bit address     "Valid with chip select",
                    input bit[8] cpu_data_in    "Data in (from CPU) - was combined with pixel_data_in in BBC micro to save pins",
                    input bit[8] pixel_data_in  "Data in (from RAM) - was combined with cpu_data_in in BBC micro to save pins",
                    input bit disen        "Asserted by CRTC if black output required (e.g. during sync)",
                    input bit invert_n     "Asserted (low) if the output should be inverted (post-disen probably)",
                    input bit cursor       "Asserted for first character of a cursor",
                    input bit[6] saa5050_red      "3 pixels in at 2MHz, red component, from teletext",
                    input bit[6] saa5050_green    "3 pixels in at 2MHz, green component, from teletext",
                    input bit[6] saa5050_blue     "3 pixels out at 2MHz, blue component, from teletext",
                    output bit crtc_clock_enable "High for 2MHz, toggles for 1MHz - the 'character clock' - used also to determine when the shift register is loaded",
                    output bit[8] red      "8 pixels out at 2MHz, red component",
                    output bit[8] green    "8 pixels out at 2MHz, green component",
                    output bit[8] blue     "8 pixels out at 2MHz, blue component",
                    output t_bbc_pixels_per_clock pixels_valid_per_clock
       )
{
    timing to   rising clock clk_cpu    chip_select_n, address, cpu_data_in;
    timing to   rising clock clk_2MHz_video   saa5050_red, saa5050_green, saa5050_blue, pixel_data_in;
    timing to   rising clock clk_2MHz_video   disen, invert_n, cursor;
    timing from rising clock clk_2MHz_video   crtc_clock_enable;
    timing from rising clock clk_2MHz_video   red, green, blue, pixels_valid_per_clock;

}

/*m crtc6845 */
extern module crtc6845( clock clk_2MHz,
                 clock clk_1MHz       "Clock that rises when the 'enable' of the 6845 completes - but a real clock for this model",
                 input bit reset_n,
                 output bit[14] ma        "Memory address",
                 output bit[5] ra         "Row address",
                 input bit read_not_write "Indicates a read transaction if asserted and chip selected",
                 input bit chip_select_n  "Active low chip select",
                 input bit rs             "Register select - address line really",
                 input bit[8] data_in     "Data in (from CPU)",
                 output bit[8] data_out   "Data out (to CPU)",
                 input bit lpstb_n "Light pen strobe",
                 input bit crtc_clock_enable "Not on the real chip - really CLK - the character clock - but this is an enable for clk_2MHz",
                 output bit de,
                 output bit cursor,
                 output bit hsync,
                 output bit vsync
       )
{
    timing to   rising clock clk_1MHz read_not_write, chip_select_n, rs, data_in;
    timing from rising clock clk_1MHz data_out;

    timing to   rising clock clk_2MHz crtc_clock_enable;
    timing from rising clock clk_2MHz ma, ra, de, cursor, hsync, vsync;
}

/*m acia6850 */
extern module acia6850( clock clk                "Clock that rises when the 'enable' of the 6850 completes - but a real clock for this model",
                 input bit reset_n,
                 input bit read_not_write "Indicates a read transaction if asserted and chip selected",
                 input bit[2] chip_select "Active high chip select",
                 input bit chip_select_n  "Active low chip select",
                 input bit address        "Changes during phase 1 (phi[0] high) with address to read or write",
                 input bit[8] data_in     "Data in (from CPU)",
                 output bit[8] data_out   "Read data out (to CPU)",
                 output bit irq_n         "Active low interrupt",
                 input bit tx_clk         "Clock used for transmit data - must be really about at most quarter the speed of clk",
                 input bit rx_clk         "Clock used for receive data - must be really about at most quarter the speed of clk",
                 output bit txd,
                 input bit cts,
                 input bit rxd,
                 output bit rts,
                 input bit dcd
       )
{
    timing to   rising clock clk   read_not_write, chip_select, chip_select_n, address, data_in;
    timing from rising clock clk   data_out, irq_n;
    timing to   rising clock clk   tx_clk, rx_clk, cts, rxd, dcd;
    timing from rising clock clk   txd, rts;
    timing comb input read_not_write, chip_select, chip_select_n, address;
    timing comb output data_out;
}

/*m bbc_micro_keyboard */
extern module bbc_micro_keyboard( clock clk,
                                  input bit reset_n,
                                  output bit reset_out_n "From the Break key",
                                  input bit keyboard_enable_n "Asserted to make keyboard detection operate",
                                  input bit[4] column_select "Wired to pa[4;0], and indicates which column of the keyboard matrix to access",
                                  input bit[3] row_select    "Wired to pa[3;4], and indicates which row of the keyboard matrix to access",
                                  output bit key_in_column_pressed "Wired to CA2, asserted if keyboard_enable_n and a key is pressed in the specified column (other than row 0)",
                                  output bit selected_key_pressed "Asserted if keyboard_enable_n is asserted and the selected key is pressed",
                                  input t_bbc_keyboard bbc_keyboard
       )
{
    timing to   rising clock clk   keyboard_enable_n, column_select;
    timing from rising clock clk   reset_out_n, key_in_column_pressed, selected_key_pressed;
    timing comb input row_select, column_select, keyboard_enable_n;
    timing comb output selected_key_pressed, key_in_column_pressed;
    timing to   rising clock clk   bbc_keyboard;
}

/*m via6522 */
extern module via6522( clock clk                "1MHz clock rising when bus cycle finishes",
                clock clk_io             "1MHz clock rising when I/O should be captured - can be antiphase to clk",
                input bit reset_n,
                input bit read_not_write "Indicates a read transaction if asserted and chip selected",
                input bit chip_select    "Active high chip select",
                input bit chip_select_n  "Active low chip select",
                input bit[4] address     "Changes during phase 1 (phi[0] high) with address to read or write",
                input bit[8] data_in     "Data in (from CPU)",
                output bit[8] data_out   "Read data out (to CPU)",
                output bit irq_n         "Active low interrupt",
                input  bit ca1            "Port a control 1 in",
                input  bit ca2_in         "Port a control 2 in",
                output bit ca2_out       "Port a control 2 out",
                output bit[8] pa_out     "Port a data out",
                input  bit[8] pa_in      "Port a data in",
                input  bit cb1            "Port b control 1 in",
                input  bit cb2_in         "Port b control 2 in",
                output bit cb2_out       "Port b control 2 out",
                output bit[8] pb_out     "Port b data out",
                input  bit[8] pb_in      "Port b data in"
       )
{
    timing to   rising clock clk   read_not_write, chip_select, chip_select_n, address, data_in;
    timing from rising clock clk   data_out, irq_n;
    timing to   rising clock clk   ca1, ca2_in, pa_in, cb1, cb2_in, pb_in;
    timing from rising clock clk   ca2_out, pa_out, cb2_out, pb_out;
    timing to   rising clock clk_io   ca1, ca2_in, pa_in, cb1, cb2_in, pb_in;
    timing from rising clock clk_io   ca2_out, pa_out, cb2_out, pb_out;
    timing comb input chip_select, chip_select_n, read_not_write, address;
    timing comb output data_out;
}

/*m cpu6502 */
extern module cpu6502( clock clk "Clock, rising edge is start of phi1, end of phi2 - the phi1/phi2 boundary is not required",
                       input bit reset_n,
                       input bit ready "Stops processor during current instruction. Does not stop a write phase. Address bus reflects current address being read. Stops the phase 2 from happening.",
                       input bit irq_n "Active low interrupt in",
                       input bit nmi_n "Active low non-maskable interrupt in",
                       output bit ba "Goes high during phase 2 if ready was low in phase 1 if read_not_write is 1, to permit someone else to use the memory bus",
                       output bit[16] address    "In real 6502, changes during phi 1 with address to read or write",
                       output bit read_not_write "In real 6502, changes during phi 1 with whether to read or write",
                       output bit[8] data_out    "In real 6502, valid at end of phi2 with data to write",
                       input bit[8] data_in      "Captured at the end of phi2 (rising clock in here)"
    )
{
    timing to   rising clock clk   ready, irq_n, nmi_n, data_in;
    timing from rising clock clk   ba, address, read_not_write, data_out;
}

/*m saa5050 */
extern module saa5050( clock clk_2MHz     "Supposedly 6MHz pixel clock (TR6), except we use 2MHz and deliver 3 pixels per tick; rising edge should be coincident with clk_1MHz edges",
                       input bit clk_1MHz_enable "Clock enable high for clk_2MHz when the SAA's 1MHz would normally tick",
                       input bit reset_n,
                       input bit superimpose_n "Not implemented",
                       input bit data_n "Serial data in, not implemented",
                       input bit[7] data_in "Parallel data in",
                       input bit dlim "clocks serial data in somehow (datasheet is dreadful...)",
                       input bit glr "General line reset - can be tied to hsync - assert once per line before data comes in",
                       input bit dew "Data entry window - used to determine flashing rate and resets the ROM decoders - can be tied to vsync",
                       input bit crs "Character rounding select - drive high on even interlace fields to enable use of rounded character data (kinda indicates 'half line')",
                       input bit bcs_n "Assert (low) to enable double-height characters (?) ",
                       output bit tlc_n "Asserted (low) when double-height characters occur (?) ",
                       input bit lose "Load output shift register enable - must be low before start of character data in a scanline, rising with (or one tick earlier?) the data; changes off falling F1, rising clk_1MHz",
                       input bit de "Display enable",
                       input bit po "Picture on",
                       output bit[6] red,
                       output bit[6] green,
                       output bit[6] blue,
                       output bit blan,
                       input t_bbc_micro_sram_request host_sram_request "Write only, writes on clk_2MHz rising, acknowledge must be handled by supermodule"    )
{
    timing to   rising clock clk_2MHz clk_1MHz_enable, data_in, lose;
    timing to   rising clock clk_2MHz host_sram_request;
    timing from rising clock clk_2MHz red, green, blue;
}

/*m fdc8271 */
extern module fdc8271( clock clk                "",
                       input bit reset_n        "8271 has an active high reset, but...",
                       input bit chip_select_n  "Active low chip select",
                       input bit read_n         "Indicates a read transaction if asserted and chip selected",
                       input bit write_n        "Indicates a write transaction if asserted and chip selected",
                       input bit[2] address     "Address of register being accessed",
                       input bit[8] data_in     "Data in (from CPU)",
                       output bit[8] data_out   "Read data out (to CPU)",
                       output bit irq_n         "Was INT on the 8271, but that means something else now; active low interrupt",
                       output bit data_req      "",
                       input  bit data_ack_n    "",
                       output bit[2] select     "drive select",
                       input bit[2] ready       "drive ready",
                       output bit fault_reset   "",
                       output bit write_enable  "High if the drive should write data",
                       output bit seek_step     "High if the drive should step",
                       output bit direction     "Direction of step",
                       output bit load_head     "Enable drive head",
                       output bit low_current   "Asserted for track>=43",
                       input bit track_0_n        "Asserted low if the selected drive is on track 0",
                       input bit write_protect_n  "Asserted low if the selected drive is write-protected",
                       input bit index_n          "Asserted low if the selected drive photodiode indicates start of track",
                       output t_bbc_floppy_op bbc_floppy_op              "Model drive operation, including write data",
                       input t_bbc_floppy_response bbc_floppy_response  "Parallel data read, specific to the model"
                // fault_n, count_n, plo, write_data, unseparated_data_n, data_window, insync
       )
{
    timing to    rising clock clk chip_select_n, read_n, write_n, address, data_in;
    timing from  rising clock clk data_out, irq_n;

    timing to    rising clock clk data_ack_n;
    timing from  rising clock clk data_req;

    timing to    rising clock clk bbc_floppy_response;
    timing from  rising clock clk bbc_floppy_op;

    timing comb input data_ack_n, address, read_n, chip_select_n;
    timing comb output data_out;
}

/*m bbc_micro_clocking */
extern module bbc_micro_clocking( clock clk "4MHz clock in as a minimum",
                                  input bit reset_n,
                                  input t_bbc_clock_status clock_status,
                                  output t_bbc_clock_control clock_control,
                                  input t_csr_request csr_request,
                                  output t_csr_response csr_response )
{
    timing to   rising clock clk   clock_status;
    timing from rising clock clk   clock_control;
    timing to   rising clock clk   csr_request;
    timing from rising clock clk   csr_response;
}

/*m bbc_micro_rams */
extern module bbc_micro_rams( clock clk "4MHz clock in as a minimum",
                       input bit reset_n,
                       input t_bbc_clock_control clock_control,
                       input t_bbc_micro_sram_request host_sram_request,
                       output t_bbc_micro_sram_response host_sram_response,
                       input t_bbc_display_sram_write display_sram_write,
                       input t_bbc_floppy_sram_request floppy_sram_request,
                       output t_bbc_floppy_sram_response floppy_sram_response,
                       output t_bbc_micro_sram_request bbc_micro_host_sram_request,
                       input t_bbc_micro_sram_response bbc_micro_host_sram_response )
{
    timing to   rising clock clk clock_control;
    timing to   rising clock clk host_sram_request, display_sram_write, floppy_sram_request, bbc_micro_host_sram_response;
    timing from rising clock clk host_sram_response, floppy_sram_response, bbc_micro_host_sram_request;
}

/*m bbc_micro */
extern module bbc_micro( clock clk "Clock at least at '4MHz' - CPU runs at least half of this",
                  input t_bbc_clock_control clock_control,
                  output t_bbc_clock_status clock_status,
                  input bit reset_n,
                  input t_bbc_keyboard keyboard,
                  output t_bbc_display display,
                  output bit keyboard_reset_n,
                  output t_bbc_floppy_op floppy_op,
                         input t_bbc_floppy_response floppy_response,
                       input t_bbc_micro_sram_request host_sram_request,
                       output t_bbc_micro_sram_response host_sram_response )
{
    timing to   rising clock clk   clock_control, keyboard, floppy_response;
    timing from rising clock clk   clock_status, display, floppy_op;

    timing to   rising clock clk   host_sram_request;
    timing from rising clock clk   host_sram_response;
}

/*m bbc_display_sram */
extern module bbc_display_sram( clock clk "Clock running at 2MHz",
                         input bit reset_n,
                         input t_bbc_display display,
                         output t_bbc_display_sram_write sram_write,
                         input t_csr_request csr_request,
                         output t_csr_response csr_response
    )
{
    timing to   rising clock clk   display, csr_request;
    timing from rising clock clk   sram_write, csr_response;
}

/*m bbc_keyboard_csr */
extern module bbc_keyboard_csr( clock clk "Clock running at 2MHz",
                         input bit reset_n,
                         output t_bbc_keyboard keyboard,
                         input bit keyboard_reset_n,
                         input t_csr_request csr_request,
                         output t_csr_response csr_response
    )
{
    timing to   rising clock clk   keyboard_reset_n, csr_request;
    timing from rising clock clk   keyboard, csr_response;
}

/*m bbc_keyboard_ps2 */
extern
module bbc_keyboard_ps2( clock clk "Clock of PS2 keyboard",
                         input bit reset_n,
                         input t_ps2_key_state  ps2_key,
                         output t_bbc_keyboard keyboard
    )
{
    timing to   rising clock clk   ps2_key;
    timing from rising clock clk   keyboard;
}

/*m bbc_floppy_sram */
extern module bbc_floppy_sram( clock clk "Clock running at 2MHz",
                        input bit reset_n,
                        input t_bbc_floppy_op floppy_op,
                        output t_bbc_floppy_response floppy_response,
                        output t_bbc_floppy_sram_request sram_request,
                        input t_bbc_floppy_sram_response sram_response,
                        input t_csr_request csr_request,
                        output t_csr_response csr_response
)
{
    timing to   rising clock clk   floppy_op, sram_response, csr_request;
    timing from rising clock clk   floppy_response, sram_request, csr_response;
}

/*m bbc_display */
extern module bbc_display( clock clk "Clock running at 2MHz",
                           //input bit reset_n,
                           input t_bbc_display_sram_write display_sram_write,
                           input t_bbc_floppy_sram_request floppy_sram_request,
                           output t_bbc_keyboard keyboard,
                           output bit reset_n,
                           output t_bbc_floppy_sram_response floppy_sram_response )
{
    timing to   rising clock clk   display_sram_write, floppy_sram_request;
    timing from rising clock clk   keyboard, floppy_sram_response;
}

