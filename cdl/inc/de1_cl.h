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
    bit updated_switches;
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
