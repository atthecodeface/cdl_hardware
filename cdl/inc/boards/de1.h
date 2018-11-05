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
 * @file   de2.h
 * @brief  Header file for Altera DE2 board
 *
 * Header file for the types and CDL modules
 *
 */

/*a Types */
/*t t_de1_inputs */
typedef struct {
    bit irda_rxd;
    bit[4]  keys;
    bit[10] switches;
} t_de1_inputs;

/*t t_de1_audio */
typedef struct {
    bit data;
    bit lrc;
} t_de1_audio;

/*t t_de1_leds */
typedef struct {
    bit[10] leds;
    bit[7] h0;
    bit[7] h1;
    bit[7] h2;
    bit[7] h3;
    bit[7] h4;
    bit[7] h5;
} t_de1_leds;

