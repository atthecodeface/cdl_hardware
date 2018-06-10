include "apb.h"

typedef struct {
    bit ntrst;
    bit tms;
    bit tdi;
} t_jtag;

typedef enum [2] {
    action_idle,
    action_capture,
    action_shift,
    action_update
} t_jtag_action;

extern module jtag_tap( clock jtag_tck,
                 input bit reset_n,
                 input t_jtag jtag,
                 output bit tdo,

                 output bit[5]ir,
                 output t_jtag_action dr_action,
                 output bit[50]dr,
                 input  bit[50]dr_tdi_mask,
                 input  bit[50]dr_out
    )
{
    timing to rising clock jtag_tck jtag, dr_tdi_mask, dr_out;
    timing from rising clock jtag_tck tdo, ir, dr_action, dr;
}

extern module jtag_apb( clock jtag_tck,
                 input bit reset_n,

                 input bit[5]ir,
                 input t_jtag_action dr_action,
                 input  bit[50]dr_in,
                 output bit[50]dr_tdi_mask,
                 output bit[50]dr_out,

                 clock apb_clock,
                 output t_apb_request apb_request,
                 input t_apb_response apb_response
    )
{
    timing to rising clock jtag_tck ir, dr_action, dr_in;
    timing from rising clock jtag_tck dr_tdi_mask, dr_out;
    timing from rising clock apb_clock apb_request;
    timing to rising clock apb_clock apb_response;
    timing comb input dr_in, dr_action, ir;
    timing comb output dr_out, dr_tdi_mask;
}
