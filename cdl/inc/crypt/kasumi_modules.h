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
 * @file   kasumi_modules.h
 * @brief  Header files for Kasumi modules
 *
 */

/*a Module */
/*m kasumi_cipher_3 */
extern module kasumi_cipher_3(  clock clk,
                         input bit reset_n,
                         input t_kasumi_input    kasumi_input,
                         output bit              kasumi_input_ack,
                         output t_kasumi_output  kasumi_output,
                         input bit               kasumi_output_ack
    )
{
    timing to   rising clock clk kasumi_input, kasumi_output_ack;
    timing from rising clock clk kasumi_output, kasumi_input_ack;
}

/*m Generic kasumi_cipher */
extern module kasumi_cipher(  clock clk,
                         input bit reset_n,
                         input t_kasumi_input    kasumi_input,
                         output bit              kasumi_input_ack,
                         output t_kasumi_output  kasumi_output,
                         input bit               kasumi_output_ack
    )
{
    timing to   rising clock clk kasumi_input, kasumi_output_ack;
    timing from rising clock clk kasumi_output, kasumi_input_ack;
}

