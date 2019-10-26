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
 * @file   sync_modules.h
 * @brief  Header files for technology dependent synchronization modules
 *
 */
/*a Includes */

/*a Modules */
/*m tech_sync_flop */
extern module tech_sync_flop( clock clk           "Clock to synchronize to",
                              input bit reset_n   "Active low reset",
                              input bit d         "Data in",
                              output bit q         "Data out" )
{
    timing to   rising clock clk d;
    timing from rising clock clk q;
}

/*m tech_sync_bit */
extern module tech_sync_bit( clock clk           "Clock to synchronize to",
                              input bit reset_n   "Active low reset",
                              input bit d         "Data in",
                              output bit q         "Data out from at least a pair of sync flops" )
{
    timing to   rising clock clk d;
    timing from rising clock clk q;
}
