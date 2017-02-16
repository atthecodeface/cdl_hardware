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
 * @file   leds.h
 * @brief  Constants, types and modules for various LED drivers
 *
 * Header file for the types and modules controlling LEDs, including
 * Neopixel chains.
 *
 */

/*a Constants */
constant bit[16] led_seven_seg_hex_a = 16b_1101011111101101;
constant bit[16] led_seven_seg_hex_b = 16b_0010011110011111;
constant bit[16] led_seven_seg_hex_c = 16b_0010111111111011;
constant bit[16] led_seven_seg_hex_d = 16b_0111101101101101;
constant bit[16] led_seven_seg_hex_e = 16b_1111110101000101;
constant bit[16] led_seven_seg_hex_f = 16b_1101111101110001;
constant bit[16] led_seven_seg_hex_g = 16b_1110111101111100;

/*a Types */
/*t t_led_ws2812_data*/
typedef struct {
    bit valid;
    bit last;
    bit[8] red;
    bit[8] green;
    bit[8] blue;
} t_led_ws2812_data;

/*t t_led_ws2812_request*/
typedef struct {
    bit ready          "Active high signal indicating if LED data is required; ignore if the data is currently valid";
    bit first          "If requesting LED data, then the first LED of the stream should be provided; indicates led_number is 0";
    bit[8] led_number  "Number of LED data required, in case an array is used by the client";
} t_led_ws2812_request;

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
