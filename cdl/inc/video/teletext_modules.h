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
 * @file  teletext.h
 * @brief Teletext types header file
 *
 *
 */
/*a Includes */
include "types/teletext.h"

/*a Modules */
/*m teletext */
extern module teletext( clock clk     "Character clock",
                        input bit reset_n,
                        input t_teletext_character    character  "Parallel character data in, with valid signal",
                        input t_teletext_timings      timings    "Timings for the scanline, row, etc",
                        output t_teletext_rom_access  rom_access "Teletext ROM access",
                        input bit[45]                 rom_data   "Teletext ROM data, valid in cycle after rom_access",
                        output t_teletext_pixels pixels       "Output pixels, two clock ticks delayed from clk in"
    )
{
    timing to   rising clock clk character, timings;
    timing from rising clock clk rom_access;
    timing to   rising clock clk rom_data;
    timing from rising clock clk pixels;
}
