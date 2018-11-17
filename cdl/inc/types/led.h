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

/*a Constants */
constant bit[16] led_seven_seg_hex_a = 16b_1101011111101101 "Which hex values require lighting of LED segment A";
constant bit[16] led_seven_seg_hex_b = 16b_0010011110011111 "Which hex values require lighting of LED segment B";
constant bit[16] led_seven_seg_hex_c = 16b_0010111111111011 "Which hex values require lighting of LED segment C";
constant bit[16] led_seven_seg_hex_d = 16b_0111101101101101 "Which hex values require lighting of LED segment D";
constant bit[16] led_seven_seg_hex_e = 16b_1111110101000101 "Which hex values require lighting of LED segment E";
constant bit[16] led_seven_seg_hex_f = 16b_1101111101110001 "Which hex values require lighting of LED segment F";
constant bit[16] led_seven_seg_hex_g = 16b_1110111101111100 "Which hex values require lighting of LED segment G";

/*a Types */
/*t t_led_ws2812_data
 *
 * LED data response to the led_ws2812_chain module, indicating the
 * 24-bit RGB value for the @a led_number'th LED in the chain
 *
 */
typedef struct {
    bit valid     "Assert if the LED data supplied in this structure is valid";
    bit last      "Assert if the LED data is for the last LED in the chain";
    bit[8] red    "The 8 bit red component for the LED to display";
    bit[8] green  "The 8 bit green component for the LED to display";
    bit[8] blue   "The 8 bit blue component for the LED to display";
} t_led_ws2812_data;

/*t t_led_ws2812_request
 *
 * Request from the led_ws2812_chain module to ask for the color data
 * for a particular LED in the LED chain
 */
typedef struct {
    bit ready          "Active high signal indicating if LED data is required; ignore @a ready if the response has @a valid asserted";
    bit first          "If requesting LED data, then the first LED of the stream should be provided; indicates @a led_number is 0";
    bit[8] led_number  "Number of LED data required, so that a client can use a switch statement or register file or array, for example";
} t_led_ws2812_request;

