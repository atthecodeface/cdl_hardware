/** Copyright (C) 2016-2018,  Gavin J Stark.  All rights reserved.
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
 * @file   input_devices.h
 * @brief  Input device header file for CDL modules
 *
 * Header file for the types and CDL modules for input devices
 *
 */

/*a Includes */

/*a Modules */
/*m async_reduce_4_28_r */
extern
module async_reduce_4_28_r( clock          clk_in "Clock associated with data_in",
                            clock          clk_out "Clock associated with data_out",
                            input bit      reset_n,
                            input bit      valid_in,
                            input bit[4]   data_in,
                            output bit     valid_out,
                            output bit[28] data_out )
{
    timing to   rising clock clk_in  data_in, valid_in;
    timing from rising clock clk_out data_out, valid_out;
}

/*m async_reduce_4_28_l */
extern
module async_reduce_4_28_l( clock          clk_in "Clock associated with data_in",
                            clock          clk_out "Clock associated with data_out",
                            input bit      reset_n,
                            input bit      valid_in,
                            input bit[4]   data_in,
                            output bit     valid_out,
                            output bit[28] data_out )
{
    timing to   rising clock clk_in  data_in, valid_in;
    timing from rising clock clk_out data_out, valid_out;
}

/*m async_reduce_4_60_r */
extern
module async_reduce_4_60_r( clock          clk_in "Clock associated with data_in",
                            clock          clk_out "Clock associated with data_out",
                            input bit      reset_n,
                            input bit      valid_in,
                            input bit[4]   data_in,
                            output bit     valid_out,
                            output bit[60] data_out )
{
    timing to   rising clock clk_in  data_in, valid_in;
    timing from rising clock clk_out data_out, valid_out;
}

/*m async_reduce_4_60_l */
extern
module async_reduce_4_60_l( clock          clk_in "Clock associated with data_in",
                            clock          clk_out "Clock associated with data_out",
                            input bit      reset_n,
                            input bit      valid_in,
                            input bit[4]   data_in,
                            output bit     valid_out,
                            output bit[60] data_out )
{
    timing to   rising clock clk_in  data_in, valid_in;
    timing from rising clock clk_out data_out, valid_out;
}

