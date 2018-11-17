/** Copyright (C) 2018,  Gavin J Stark.  All rights reserved.
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
 * @file   axi.h
 * @brief  Types for the AXI bus
 *
 * Header file for the types for an AXI bus, but no modules
 *
 */

/*a Includes */
include "types/axi.h"

/*a Modules - see also apb_master_axi in apb.h*/
/*m axi_master */
extern
module axi_master(clock aclk,
                  input bit areset_n,
                  output t_axi_request ar,
                  input bit awready,
                  output t_axi_request aw,
                  input bit arready,
                  input bit wready,
                  output t_axi_write_data w,
                  output bit bready,
                  input t_axi_write_response b,
                  output bit rready,
                  input t_axi_read_response r
    )
{
    timing from rising clock aclk ar, aw, w, bready, rready;
    timing to rising clock aclk awready, arready, wready, b, r;
}
