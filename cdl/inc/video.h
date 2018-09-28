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
 */

/*a Includes */

/*a Types */
/*t t_video_bus */
typedef struct {
    bit    vsync "Asserted for one whole line at start of back porch of frame, simultaneous with hsync";
    bit    hsync "Asserted for one cycle at start of back porch";
    bit    display_enable "Asserted after end of back porch for display pixels/lines";
    bit[8] red;
    bit[8] green;
    bit[8] blue;
} t_video_bus;

/*t t_adv7123
 *
 * Timing values (display + (right border / front porch) + sync pulse + (back porch / left border))
 *
 *  640x480 @ 60Hz: 25.175MHz clk 640+16+ 96+48 = 800  480+10+2+33 = 525 -syncs
 *  800x600 @ 60Hz: 40MHz clk     800+40+128+88 =1076  600+ 1+4+23 = 628 +syncs
 * 1024x768 @ 60Hz: 65MHz clk    1024+24+136+160=1344  768+ 3+6+29 = 806 -syncs
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

