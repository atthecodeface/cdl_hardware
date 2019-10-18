/** Copyright (C) 2019,  Gavin J Stark.  All rights reserved.
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
 * @file   MDIO.h
 * @brief  MDIO signals
 *
 * Header file for the types for MDIO signals
 *
 */

/*a Types */
/*t t_mdio_out - return is just mdio pin */
typedef struct {
    bit mdc; // max of 2.5MHz (min 400ns period)
    bit mdio;
    bit mdio_enable "if asserted (high) drive mdio";
} t_mdio_out;
