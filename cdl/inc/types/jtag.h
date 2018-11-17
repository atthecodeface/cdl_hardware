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
 * @file   jtag.h
 * @brief  Types for JTAG handling
 *
 */

/*a Types */
/*t t_jtag
 */
typedef struct {
    bit ntrst;
    bit tms;
    bit tdi;
} t_jtag;

/* t_jtag_action
 */
typedef enum [2] {
    action_idle,
    action_capture,
    action_shift,
    action_update
} t_jtag_action;
