include "types/clock_divider.h"
extern module clock_divider( clock clk                    "Clock for the module",
                      input bit reset_n            "Active low reset",
                      input t_clock_divider_control divider_control "Controls for any clock divider",
                      output t_clock_divider_output divider_output  "Clock divider output state, all clocked"
    )
{
    timing to   rising clock clk divider_control;
    timing from rising clock clk divider_output;
}
