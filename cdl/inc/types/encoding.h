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
 * @file   encoding.h
 * @brief  Types for encodings of bits (generally for networking)
 *
 * Header file for the types for encodings of bits in symbols
 *
 */

/*a Types */
/*t t_8b10b_dec_data */
typedef struct {
    bit    valid                           "Asserted if a valid 8B10B symbol";
    bit[8] data                            "Data decoded from symbol";
    bit    is_control                      "Asserted if a control symbol";
    bit    is_data                         "Asserted if a data symbol";
    bit    disparity_positive              "Asserted if disparoirty after the symbol is positive";
} t_8b10b_dec_data;

/*t t_8b10b_symbol
 */
typedef struct {
    bit     disparity_positive;
    bit[10] symbol;
} t_8b10b_symbol;

/*t t_8b10b_enc_data */
typedef struct {
    bit[8] data                    "Data to be encoded in symbol";
    bit    is_control              "Asserted if a control symbol";
    bit    disparity               "Asserted high if positive disparity in";
} t_8b10b_enc_data;

