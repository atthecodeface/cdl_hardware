include "types/dprintf.h"
include "types/video.h"
include "types/memories.h"
include "boards/vcu108.h"
extern
module vcu108_generic( clock clk,
                       clock clk_50,
                       input bit reset_n,

                       input  t_dprintf_req_4 vcu108_dprintf_req,
                       input  t_vcu108_inputs vcu108_inputs,
                       output t_vcu108_outputs vcu108_outputs,

                       clock video_clk,
                       input bit video_reset_n,
                       output t_adv7511 vcu108_video,

                       clock     sgmii_tx_clk     "Four-bit transmit serializing data clock (312.5MHz)",
                       input bit sgmii_tx_reset_n "Reset deasserting sync to sgmii_tx_clk",
                       output bit[4] sgmii_txd    "First bit for wire in txd[0]",

                       clock     sgmii_rx_clk     "Four-bit receive serializing data clock (312.5MHz)",
                       input bit sgmii_rx_reset_n "Reset deasserting sync to sgmii_rx_clk",
                       input bit[4] sgmii_rxd     "Oldest bit in rxd[0]",

                       clock flash_clk,
                       input t_mem_flash_in flash_in,
                       output t_mem_flash_out flash_out

    )
{
    timing to   rising clock clk vcu108_inputs, vcu108_dprintf_req;
    timing from rising clock clk vcu108_outputs;

    timing to   rising clock clk_50 vcu108_inputs; // keep clk_50!
    timing from rising clock clk_50 vcu108_outputs; // keep clk_50!

    timing from rising clock video_clk vcu108_video;

    timing to   rising clock sgmii_tx_clk sgmii_tx_reset_n;
    timing from rising clock sgmii_tx_clk sgmii_txd;
    timing to   rising clock sgmii_rx_clk sgmii_rx_reset_n, sgmii_rxd;

    timing to   rising clock flash_clk flash_in;
    timing from rising clock flash_clk flash_out;
}
