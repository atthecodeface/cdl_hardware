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
 * @file   framebuffer.h
 * @brief  Framebuffer CDL submodules
 *
 * Header file for framebuffer modules for VGA, LCD panel, both
 * bitmapped and teletext.
 *
 */

/*a Includes */
include "csr_interface.h"
include "teletext.h"
include "bbc_micro_types.h"

/*a Modules */
/*m framebuffer_teletext */
extern module framebuffer_teletext( clock csr_clk "Clock for CSR reads/writes",
                                    clock sram_clk  "SRAM write clock, with frame buffer data",
                                    clock video_clk "Video clock, used to generate vsync, hsync, data out, etc",
                                    input bit reset_n,
                                    input t_bbc_display_sram_write display_sram_write,
                                    output t_video_bus video_bus,
                                    input t_csr_request csr_request,
                                    output t_csr_response csr_response
    )
{
    timing to   rising clock sram_clk   display_sram_write;
    timing to   rising clock csr_clk    csr_request;
    timing from rising clock csr_clk    csr_response;
    timing from rising clock video_clk  video_bus;
}

/*m framebuffer */
extern module framebuffer( clock csr_clk "Clock for CSR reads/writes",
                    clock sram_clk  "SRAM write clock, with frame buffer data",
                    clock video_clk "Video clock, used to generate vsync, hsync, data out, etc",
                    input bit reset_n,
                    input t_bbc_display_sram_write display_sram_write,
                    output t_video_bus video_bus,
                    input t_csr_request csr_request,
                    output t_csr_response csr_response
    )
{
    timing to   rising clock sram_clk   display_sram_write;
    timing to   rising clock csr_clk    csr_request;
    timing from rising clock csr_clk    csr_response;
    timing from rising clock video_clk  video_bus;
}

