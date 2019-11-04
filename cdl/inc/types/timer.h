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
 *
 * Need to add a 'synchronize_counter', and 'lock_counter'
 *
 * Need a new module that takes the global (async to this clock)
 * counter and uses the local clock to create a 64-bit nanosecond timer
 * The '2;N'th bits of the global counter toggle slowly with respect to this clock
 * and can be grey coded and synced across. This clock should be able to take the
 * bits above N+1 of the global counter without synchronization during 'synchronize_counter'.
 * The bottom bits can be set to the 'correct' value when the synch is detected.
 *
 * For tracking, the synchronized bits are compared with the local bits
 * The difference in timing of the bits is tracked, and 'advance' and 'retard' bits are
 * generated to remove up to half of the difference. Retarding permits adding of less of the
 * adders.
 *
 */
typedef struct {
    bit     reset_counter               "Assert to reset the timer counter to 0; this takes precedence over enable_counter";
    bit     enable_counter              "Assert to enable the timer counter; otherwise it holds its value";
    bit     advance                     "When enabled, a positive edge moves the clock on by half the amount more";
    bit     retard                      "When enabled, a positive edge moves the clock on by half the amount less than normal";
    bit     lock_to_master              "Used by slaves to enable locking to a master when they are asynchronous";
    bit[2]  synchronize                 "Two bits to indicate whether to write top or bottom halves";
    bit[64] synchronize_value           "Value to synchronize to";
    bit     block_writes                "If the timer has a seperate read/write interface, block writes";
    bit[8]  bonus_subfraction_numer     "(n-1) in fractional n/16d increment per cycle";
    bit[8]  bonus_subfraction_denom     "(d-1) in fractional n/16d increment per cycle; If zero then no subfractional add";
    bit[4]  fractional_adder            "f in fraction f/16 to add per cycle";
    bit[8]  integer_adder               "integer amount to add to timer counter per cycle";
} t_timer_control;

/*t t_timer_value
 */
typedef struct {
    bit[64] value   "64-bit timer value, reflecting the value in the timer counter";
    bit     irq     "Asserted if comparator >= timer value";
    bit     locked  "Asserted if the timer has locked (held low unless in a slave clock domain)";
} t_timer_value;
