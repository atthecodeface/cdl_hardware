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
 * @file   encoders.h
 * @brief  Modules for various encoders (generally for networking)
 *
 * Header file for encoder modules
 *
 */

/*a Includes */
include "types/encoding.h"

/*a Modules */
/*m encode_8b10b */
extern module encode_8b10b( input t_8b10b_enc_data enc_data,
                            output t_8b10b_symbol  symbol
    )
{
    timing comb input enc_data;
    timing comb output symbol;
}

/*m decode_8b10b */
extern module decode_8b10b( input t_8b10b_symbol  symbol,
                            output t_8b10b_dec_data dec_data
    )
{
    timing comb input symbol;
    timing comb output dec_data;
}

