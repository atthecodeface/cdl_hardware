/** @copyright (C) 2016-2017,  Gavin J Stark.  All rights reserved.
 *
 * @copyright
 *    Licensed under the Apache License, Version 2.0 (the "License");
 *    you may not use this file except in compliance with the License.
 *    You may obtain a copy of the License at
 *     http://www.apache.org/licenses/LICENSE-2.0.
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 *
 * @file   leds.h
 * @brief  Constants, types and modules for various LED drivers
 *
 * Header file for the types and modules controlling LEDs, including
 * Neopixel chains.
 *
 */

/*a Includes */
include "types/led.h"

/*a Modules */
/*m led_seven_segment*/
extern module led_seven_segment( input bit[4] hex   "Hexadecimal to display on 7-segment LED",
                                 output bit[7] leds "1 for LED on, 0 for LED off, for segments a-g in bits 0-7"
    )
{
    timing comb input hex;
    timing comb output leds;
}

/*m led_ws2812_chain*/
extern module led_ws2812_chain( clock clk                   "system clock - not the pin clock",
                                input bit    reset_n  "async reset",
                                input bit[8] divider_400ns  "clock divider value to provide for generating a pulse every 400ns based on clk",
                                output t_led_ws2812_request led_request  "LED data request",
                                input t_led_ws2812_data     led_data     "LED data, for the requested led",
                                output bit led_chain                     "Data in pin for LED chain"
    )
{
    timing to   rising clock clk  divider_400ns, led_data;
    timing from rising clock clk  led_request, led_chain;
}
