include "types/video.h"
include "types/memories.h"
include "boards/vcu108.h"
extern
module vcu108_generic( clock clk,
                       clock clk_50,
                       input bit reset_n,

                       input  bit[64] vcu108_data,
                       input  t_vcu108_inputs vcu108_inputs,
                       output t_vcu108_outputs vcu108_outputs,

                       clock video_clk,
                       input bit video_reset_n,
                       output t_adv7511 vcu108_video,

                       clock flash_clk,
                       input t_mem_flash_in flash_in,
                       output t_mem_flash_out flash_out
    )
{
    timing to   rising clock clk vcu108_inputs, vcu108_data;
    timing from rising clock clk vcu108_outputs;

    timing to   rising clock clk_50 vcu108_inputs; // keep clk_50!
    timing from rising clock clk_50 vcu108_outputs; // keep clk_50!

    timing from rising clock video_clk vcu108_video;

    timing to   rising clock flash_clk flash_in;
    timing from rising clock flash_clk flash_out;
}
