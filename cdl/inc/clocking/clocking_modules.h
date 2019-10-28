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
 * @file   clocking_modules.h
 * @brief  Modules for various clocking things
 *
 * Header file for the clocking modules 
 *
 */

/*a Includes */
include "types/clocking.h"

/*a Modules - see also csr_target_apb, csr_master_apb in csr_interface.h */
extern module clocking_phase_measure( clock clk,
                                      input bit reset_n,
                                      output t_bit_delay_config   delay_config,
                                      input  t_bit_delay_response delay_response,
                                      input   t_phase_measure_request measure_request,
                                      output  t_phase_measure_response measure_response
    )
{
    timing from rising clock clk delay_config, measure_response;
    timing to   rising clock clk delay_response, measure_request;
}

extern module clocking_eye_tracking( clock clk,
                              clock data_clk "Clock generating data_p_in and data_n_in (tracking data)",
                              input bit reset_n,

                              input   bit[4] data_p_in,
                              input   bit[4] data_n_in,
                              output  t_bit_delay_config   delay_config,
                              input   t_bit_delay_response delay_response,
                              input   t_eye_track_request  eye_track_request,
                              output  t_eye_track_response eye_track_response
    )
{
    timing to   rising clock data_clk data_p_in, data_n_in;
    timing from rising clock clk delay_config, eye_track_response;
    timing to   rising clock clk delay_response, eye_track_request;
}
