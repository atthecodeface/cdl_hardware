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
 * @file   kasumi_fi.cdl
 * @brief  FI function for Kasumi
 *
 */

/*a Module */
/*m kasumi_fi */
extern module kasumi_fi( input bit[16] data_in,
                         input bit[16] key_in,
                         output bit[16] data_out
    )
{
    timing comb input  data_in, key_in;
    timing comb output data_out;
}

/*m kasumi_sbox7 */
extern module kasumi_sbox7( input bit[7] sbox_in,
                            output bit[7] sbox_out
    )
{
    timing comb input  sbox_in;
    timing comb output sbox_out;
}

/*m kasumi_sbox9 */
extern module kasumi_sbox9( input bit[9] sbox_in,
                            output bit[9] sbox_out
    )
{
    timing comb input  sbox_in;
    timing comb output sbox_out;
}

/*m kasumi_fo_cycles_3 */
extern module kasumi_fo_cycles_3( clock clk,
                           input bit reset_n,
                           input bit start,
                           input bit[32] data_in,
                           input bit[32] keys_ki_ko_1,
                           input bit[32] keys_ki_ko_2,
                           input bit[32] keys_ki_ko_3,
                           output bit data_valid,
                           output bit[32] data_out
    )
{
    timing to   rising clock clk start, data_in, keys_ki_ko_1, keys_ki_ko_2, keys_ki_ko_3;
    timing from rising clock clk data_out, data_valid;

    timing comb input data_in, keys_ki_ko_1, keys_ki_ko_2, keys_ki_ko_3;
    timing comb output data_out;
}

