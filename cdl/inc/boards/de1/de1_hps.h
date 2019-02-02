include "types/axi.h"
include "types/ps2.h"
include "types/video.h"
include "boards/de1.h"
extern
module de1_hps_generic( clock clk,
                        input bit reset_n,

                        clock lw_axi_clock_clk,
                        input t_axi_request    lw_axi_ar,
                        output bit             lw_axi_arready,
                        input t_axi_request    lw_axi_aw,
                        output bit             lw_axi_awready,
                        output bit             lw_axi_wready,
                        input t_axi_write_data lw_axi_w,
                        input bit              lw_axi_bready,
                        output t_axi_write_response lw_axi_b,
                        input bit lw_axi_rready,
                        output t_axi_read_response lw_axi_r,

                        clock de1_audio_bclk,
                        input  t_de1_audio de1_audio_adc,
                        output t_de1_audio de1_audio_dac,

                        input t_de1_inputs de1_inputs,
                        output t_de1_leds de1_leds,

                        input t_ps2_pins   de1_ps2_in,
                        output t_ps2_pins  de1_ps2_out,
                        input t_ps2_pins   de1_ps2b_in,
                        output t_ps2_pins  de1_ps2b_out,

                        clock de1_vga_clock,
                        input bit de1_vga_reset_n,
                        output t_adv7123 de1_vga
    )
{
    timing to   rising clock lw_axi_clock_clk lw_axi_ar, lw_axi_aw, lw_axi_w, lw_axi_bready, lw_axi_rready;
    timing from rising clock lw_axi_clock_clk lw_axi_awready, lw_axi_arready, lw_axi_wready, lw_axi_b, lw_axi_r;

    timing to   rising clock de1_audio_bclk de1_audio_adc;
    timing from rising clock de1_audio_bclk de1_audio_dac;

    timing from rising clock de1_vga_clock de1_vga;
}
