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
 * @file   de1_cl.h
 * @brief  Input file for DE1 cl inputs and boards
 *
 * Header file for the types and CDL modules for input devices
 *
 * From Martin Hinner's collection of data:
 *
 * Timing values (display + (right border / front porch) + sync pulse + (back porch / left border))
 *
 *  640x480  @ 60Hz:  25.175MHz clk 640+16+ 96+48 = 800  480+10+2+33 = 525 -syncs
 *  800x600  @ 60Hz:  40MHz clk     800+40+128+88 =1076  600+ 1+4+23 = 628 +syncs
 * 1024x768  @ 60Hz:  65MHz clk    1024+24+136+160=1344  768+ 3+6+29 = 806 -syncs
 * 1280x1024 @ 60Hz: 108MHz clk    1280+48+112+248=1688 1024+ 1+3+38 =1066 +syncs
 * 1600x1200 @ 60Hz: 162MHz clk    1600+64+192+304=2160 1200+ 1+3+46 =1250 +syncs
 *
 */

/*a Types */
/*t t_video_timing
 *
 * Timing controls from a framebuffer_timing module, to control a
 * framebuffer video driver
 */
typedef struct {
    bit v_sync              "Asserted for the whole of the first scanline or a frame";
    bit h_sync              "Asserted for a single clock at the start of every scanline";
    bit will_h_sync         "Asserted if the next clock will be an @a h_sync";
    bit v_displaying        "Asserted for a scanline if the scanline will display data";
    bit display_required    "Asserted for scanlines being displayed, up to the end of the horizontal displayed area - permits prefetching of pixel data";
    bit will_display_enable "Asserted if the next clock will have @a display_enable asserted";
    bit display_enable      "Asserted if pixels should be presented to the output (i.e. outside the front and back porches both horizontally and vertically)";
    bit v_frame_last_line   "Asserted if ";
    bit vs                  "Asserted high/low N scanlines starting at start of frame";
    bit hs                  "Asserted for a single clock at the start of every scanline";
} t_video_timing;

/*t t_video_bus */
typedef struct {
    bit    vsync          "Asserted for one whole line at start of back porch of frame, simultaneous with hsync";
    bit    hsync          "Asserted for one cycle at start of back porch";
    bit    vs             "Asserted high/low N scanlines starting at start of frame";
    bit    hs             "Asserted for a single clock at the start of every scanline";
    bit    display_enable "Asserted after end of back porch for display pixels/lines";
    bit[8] red;
    bit[8] green;
    bit[8] blue;
} t_video_bus;

/*t t_adv7123
 *
 */
typedef struct {
    bit vs       "Vsync asserted for n horizontal lines";
    bit hs       "Hsync asserted for n cycles to start retrace and the end of a line";
    bit blank_n  "Drive high for RGB out to come from red/green/blue; low for RGB to be blanking level";
    bit sync_n   "Composite sync, drive low if sync-on-green is not required, should only be driven low in blanking";
    bit[10] red   "Red data, latched on rising clock";
    bit[10] green "Green data, latched on rising clock";
    bit[10] blue  "Blue data, latched on rising clock";
} t_adv7123;



/*t t_adv7511 */
typedef struct {
    bit    vsync          "Asserted for one whole line at start of back porch of frame, simultaneous with hsync";
    bit    hsync          "Asserted for one cycle at start of back porch";
    bit    de             "Asserted after end of back porch for display pixels/lines";
    bit[16] data;
    bit     spdif;
} t_adv7511;

