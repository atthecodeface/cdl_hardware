include "types/axi.h"
include "boards/de1_cl/de1_cl_types.h"
extern
module de1_cl_hps_generic( clock clk,
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

                         input  t_de1_cl_inputs_status  de1_cl_inputs_status,
                         output t_de1_cl_inputs_control de1_cl_inputs_control,

                         output bit de1_cl_led_data_pin,

                         clock de1_cl_lcd_clock,
                         input bit de1_cl_lcd_reset_n,
                         output t_de1_cl_lcd de1_cl_lcd,
                         output t_de1_leds de1_leds,

                         input t_ps2_pins   de1_ps2_in,
                         output t_ps2_pins  de1_ps2_out,
                         input t_ps2_pins   de1_ps2b_in,
                         output t_ps2_pins  de1_ps2b_out,

                         clock de1_vga_clock,
                         input bit de1_vga_reset_n,
                         output t_adv7123 de1_vga,
                         input bit[4] de1_keys,
                         input bit[10] de1_switches,
                         input bit de1_irda_rxd,
                         output bit de1_irda_txd
    )
{
    timing to   rising clock lw_axi_clock_clk lw_axi_ar, lw_axi_aw, lw_axi_w, lw_axi_bready, lw_axi_rready;
    timing from rising clock lw_axi_clock_clk lw_axi_awready, lw_axi_arready, lw_axi_wready, lw_axi_b, lw_axi_r;
}
