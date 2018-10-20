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
 * @file   de1_cl.h
 * @brief  Input file for DE1 cl inputs and boards
 *
 * Header file for the types and CDL modules for input devices
 *
 */

/*a Includes */
include "boards/de1.h"
include "types/csr.h"
include "types/ps2.h"
include "microcomputers/bbc/bbc_types.h"
include "types/video.h"

/*a Types */
/*t t_de1_cl_inputs_control */
typedef struct {
    bit sr_clock """Not really a clock in the FPGA, but a signal toggled by the design""";
    bit sr_shift """Asserted high for rising sr_clock to shift the shift register; if low, the shift register is loaded from the pins""";
} t_de1_cl_inputs_control;

/*t t_rotary_motion_inputs */
typedef struct {
    bit direction_pin;
    bit transition_pin;
} t_rotary_motion_inputs;

/*t t_de1_cl_inputs_status */
typedef struct {
    bit sr_data  """Shift register output data""";
    t_rotary_motion_inputs left_rotary;
    t_rotary_motion_inputs right_rotary;
} t_de1_cl_inputs_status;

/*t t_de1_cl_diamond */
typedef struct {
    bit a; // bottom of diamond
    bit b; // right of diamond
    bit x; // left of diamond
    bit y; // top of diamond
} t_de1_cl_diamond;

/*t t_de1_cl_joystick */
typedef struct {
    bit u;
    bit d;
    bit l;
    bit r;
    bit c;
} t_de1_cl_joystick;

/*t t_de1_cl_shift_register */
typedef struct {
	t_de1_cl_diamond diamond;
	bit    touchpanel_irq;
    t_de1_cl_joystick joystick;
	bit    dialr_click;
	bit    diall_click;
	bit    temperature_alarm;
} t_de1_cl_shift_register;

/*t t_de1_cl_rotary */
typedef struct {
    bit pressed;
    bit direction;
    bit direction_pulse;
} t_de1_cl_rotary;

/*t t_de1_cl_user_inputs */
typedef struct {
    bit updated_switches "Asserted if diamond, joystick, touchpanel_irq, temperature_alarm, and dial pressed bits have been updated";
    t_de1_cl_diamond  diamond;
    t_de1_cl_joystick joystick;
    t_de1_cl_rotary   left_dial;
    t_de1_cl_rotary   right_dial;
    bit               touchpanel_irq;
    bit               temperature_alarm;
} t_de1_cl_user_inputs;

/*t t_de1_cl_lcd */
typedef struct {
    bit vsync_n;
    bit hsync_n;
    bit display_enable;
    bit[6] red;
    bit[7] green;
    bit[6] blue;
    bit backlight;
} t_de1_cl_lcd;

/*t t_de1_cl_shift_register_control */
typedef struct {
    bit sr_clock;
    bit sr_shift;
} t_de1_cl_shift_register_control;

extern module de1_cl_controls( clock clk          "system clock - not the shift register pin, something faster",
                               input bit    reset_n  "async reset",
                               output t_de1_cl_inputs_control inputs_control "Signals to the shift register etc on the DE1 CL daughterboard",
                               input  t_de1_cl_inputs_status  inputs_status  "Signals from the shift register, rotary encoders, etc on the DE1 CL daughterboard",
                               output t_de1_cl_user_inputs    user_inputs    "",
                               input bit[8] sr_divider  "clock divider to control speed of shift register"
    )
{
    timing to    rising clock clk inputs_status, sr_divider;
    timing from  rising clock clk inputs_control, user_inputs;
}

/*a Modules */
/*m bbc_micro_de1_cl_bbc */
extern
module bbc_micro_de1_cl_bbc( clock clk          "50MHz clock from DE1 clock generator",
                             clock video_clk    "9MHz clock from PLL, derived from 50MHz",
                             input bit reset_n  "hard reset from a pin - a key on DE1",
                             input bit bbc_reset_n,
                             input bit framebuffer_reset_n,
                             output t_bbc_clock_control clock_control,
                             input t_bbc_keyboard bbc_keyboard,
                             output t_video_bus video_bus,
                             input t_csr_request csr_request,
                             output t_csr_response csr_response
    )
{
    timing from rising clock clk clock_control;
    timing to   rising clock clk bbc_keyboard, csr_request;
    timing from rising clock clk csr_response;
    timing from rising clock video_clk video_bus;
}

/*m bbc_micro_de1_cl_io */
extern
module bbc_micro_de1_cl_io( clock clk          "50MHz clock from DE1 clock generator",
                            clock video_clk    "9MHz clock from PLL, derived from 50MHz",
                            input bit reset_n  "hard reset from a pin - a key on DE1",
                            input bit bbc_reset_n,
                            input bit framebuffer_reset_n,
                            input t_de1_inputs de1_inputs,
                            input t_bbc_clock_control clock_control,
                            output t_bbc_keyboard bbc_keyboard,
                            output t_video_bus video_bus,
                            output t_csr_request csr_request,
                            input t_csr_response csr_response,
                            input t_ps2_pins ps2_in   "PS2 input pins",
                            output t_ps2_pins ps2_out "PS2 output pin driver open collector",
                            input  t_de1_cl_inputs_status   inputs_status  "DE1 CL daughterboard shifter register etc status",
                            output t_de1_cl_inputs_control  inputs_control "DE1 CL daughterboard shifter register control",
                            output t_de1_leds de1_leds,
                            output bit lcd_source,
                            output bit led_chain
    )
{
    timing to   rising clock clk clock_control;
    timing to   rising clock clk de1_inputs;
    timing from rising clock clk lcd_source, de1_leds;
    timing from rising clock clk bbc_keyboard, csr_request;
    timing to   rising clock clk csr_response;
    timing from rising clock video_clk video_bus;
    timing to   rising clock clk ps2_in, inputs_status;
    timing from rising clock clk ps2_out, inputs_control, led_chain;
}
