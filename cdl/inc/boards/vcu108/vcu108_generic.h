include "types/video.h"
include "boards/vcu108.h"
extern
module vcu108_generic( clock clk,
                        input bit reset_n,


                     input t_vcu108_inputs vcu108_inputs,
                     output t_vcu108_leds  vcu108_leds,

                     clock video_clk,
                     input bit video_reset_n,
                     output t_adv7511 vcu108_video,

                     input bit uart_rxd,
                     output bit uart_txd
    )
{
    timing to   rising clock clk vcu108_inputs;
    timing from rising clock clk vcu108_leds;

    timing from rising clock video_clk vcu108_video;

    timing to   rising clock clk uart_rxd;
    timing from rising clock clk uart_txd;
}
