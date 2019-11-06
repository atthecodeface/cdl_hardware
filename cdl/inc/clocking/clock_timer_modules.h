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

/*a Modules */
/*m clock_timer */
extern module clock_timer( clock clk             "Timer clock",
              input bit reset_n     "Active low reset",
              input t_timer_control timer_control "Control of the timer", 
              output t_timer_value  timer_value
    )
{
    timing to   rising clock clk timer_control;
    timing from rising clock clk timer_value;
}

/*m clock_timer_async */
extern module clock_timer_async( clock master_clk             "Master clock",
                          input bit master_reset_n     "Active low reset",
                          clock slave_clk              "Slave clock, asynchronous to master",
                          input bit slave_reset_n     " Active low reset",
                          input t_timer_control  master_timer_control     "Timer control in the master domain - synchronize, reset, enable and lock_to_master are used",
                          input t_timer_value    master_timer_value       "Timer value in the master domain - only 'value' is used",
                          input t_timer_control   slave_timer_control_in  "Timer control in the slave domain - only adder values are used",
                          output t_timer_control  slave_timer_control_out "Timer control in the slave domain for other synchronous clock_timers - all valid",
                          output t_timer_value    slave_timer_value       "Timer value in the slave domain"
    )
{
    timing to   rising clock master_clk master_timer_control, master_timer_value;
    timing to   rising clock slave_clk slave_timer_control_in;
    timing from rising clock slave_clk slave_timer_control_out, slave_timer_value;
}
/*a Module */
extern module clock_timer_as_sec_nsec( clock clk             "Timer clock",
                                input bit reset_n     "Active low reset",
                                input t_timer_control timer_control "Control of the timer",
                                input t_timer_value  timer_value,
                                output t_timer_sec_nsec timer_sec_nsec
    )
{
    timing to   rising clock clk timer_control, timer_value;
    timing from rising clock clk timer_sec_nsec;
}
