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
/*t t_timer_lock_window_lsb
 *
 * Enumeration for the lock window for a master/slave clock synchronizer
 *
 * This is used by the clock_timer_async module
 *
 */
typedef enum [2] {
    timer_lock_window_lsb_4 = 2b00,
    timer_lock_window_lsb_6 = 2b01,
    timer_lock_window_lsb_8 = 2b10,
    timer_lock_window_lsb_10 = 2b11
} t_timer_lock_window_lsb;

/*t t_timer_control
 *
 * Timer control structure used by a number of clock_timer modules
 *
 * The basic elements required for a timer are @a reset_counter, @a enable_counter,
 * @a fractional_adder and @a integer_adder
 *
 */
typedef struct {
    bit     reset_counter                       "Assert to reset the timer counter to 0; this takes precedence over enable_counter";
    bit     enable_counter                      "Assert to enable the timer counter; otherwise it holds its value";
    bit     advance                             "When enabled, a positive edge moves the clock on by half the amount more";
    bit     retard                              "When enabled, a positive edge moves the clock on by half the amount less than normal";
    bit     lock_to_master                      "Used by slaves to enable locking to a master when they are asynchronous";
    t_timer_lock_window_lsb lock_window_lsb     "Used by slaves to control the synchronization loop bandwidth";
    bit[2]  synchronize                         "Two bits to indicate whether to write top or bottom halves";
    bit[64] synchronize_value                   "Value to synchronize to";
    bit     block_writes                        "If the timer has a seperate read/write interface, block writes";
    bit[8]  bonus_subfraction_add               "A fractional 1/16 is added to the timer every @a (add+1) / (@a add + @a sub + 2) cycles; if zero and @a sub is zero then no fractional add is performed";
    bit[8]  bonus_subfraction_sub               "Used with @a add for fractional addition; (@sub + 1) is subtracted from the dda accumulator if that is +ve";
    bit[4]  fractional_adder                    "f in fraction f/16 to add per cycle";
    bit[8]  integer_adder                       "integer amount to add to timer counter per cycle";
} t_timer_control;

/*t t_timer_value
 */
typedef struct {
    bit[64] value   "64-bit timer value, reflecting the value in the timer counter";
    bit     irq     "Asserted if comparator >= timer value";
    bit     locked  "Asserted if the timer has locked (held low unless in a slave clock domain)";
} t_timer_value;

/*t t_timer_sec_nsec */
typedef struct {
    bit valid        "If deasserted, the data is not currently valid";
    bit[35] sec      "Qualified by 'valid', seconds since epoch of timer_value";
    bit[30] nsec     "Qualified by 'valid', nanoseconds since epoch of timer_value";
} t_timer_sec_nsec;

