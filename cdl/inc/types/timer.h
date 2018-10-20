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
 * @file   timer.h
 * @brief  Timer types header file for CDL modules
 *
 * Header file for the types for timers
 *
 */

/*a Types */
/*t t_timer_control
 */
typedef struct {
    bit    reset_counter               "Assert to reset the timer counter to 0; this takes precedence over enable_counter";
    bit    enable_counter              "Assert to enable the timer counter; otherwise it holds its value";
    bit    block_writes                "Assert to block writes to the timer counter";
    bit[8] bonus_subfraction_numer     "(n-1) in fractional n/16d increment per cycle";
    bit[8] bonus_subfraction_denom     "(d-1) in fractional n/16d increment per cycle; If zero then no subfractional add";
    bit[4] fractional_adder            "f in fraction f/16 to add per cycle";
    bit[8] integer_adder               "integer amount to add to timer counter per cycle";
} t_timer_control;

/*t t_timer_value
 */
typedef struct {
    bit     irq   "Asserted if comparator >= timer value";
    bit[64] value "64-bit timer value, reflecting the value in the timer counter";
} t_timer_value;
