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
 * @file   vcu108.h
 * @brief  Header file for Xilinx VCU108 board
 *
 * Header file for the types and CDL modules
 *
 */

/*a Types */
/*t t_de1_inputs */
typedef struct {
    bit[4]  switches;
    bit[5]  buttons; // N S W E C
} t_vcu108_inputs;

/*t t_de1_leds */
typedef struct {
    bit[8] leds;
} t_vcu108_leds;

