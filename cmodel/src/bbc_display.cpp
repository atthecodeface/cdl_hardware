/** Copyright (C) 2015-2017,  Gavin J Stark.  All rights reserved.
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
 * @file   bbc_display.cpp
 * @brief  BBC microcomputer display
 *
 * BBC display C model source code, which uses the BBC shared memory
 * (SHM) to create a SHM frame buffer and keyboard interaction for CDL
 * simulations. The bbc_display_vnc program can be used to interact
 * with this SHM, allowing a simulation to be viewed, and to have
 * keyboard and reset interactions.
 *
 * The initial cut of this source code is from CDL C model output.
 *
 */
/*a Includes */
#include "sl_mif.h"
#include "be_model_includes.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "image_io.h"
#include "bbc_shm.h"
#include "bbc_display.h"

/*a Types for bbc_display */
/*t t_bbc_display_sram_write_inputs */
/**
 * The inputs are three buses: display_sram_write, csr_response and
 * host_sram_response. This structure permits wiring of these.
 */
typedef struct t_bbc_display_sram_write_inputs {
    t_sl_uint64 *display_sram_write__enable;
    t_sl_uint64 *display_sram_write__data;
    t_sl_uint64 *display_sram_write__address;
    t_sl_uint64 *csr_response__ack;
    t_sl_uint64 *csr_response__read_data_valid;
    t_sl_uint64 *csr_response__read_data;
    t_sl_uint64 *host_sram_response__ack;
    t_sl_uint64 *host_sram_response__read_data_valid;
    t_sl_uint64 *host_sram_response__read_data;
} t_bbc_display_sram_write_inputs;

/*t t_bbc_display_outputs */
/**
 * The outputs are two buses: csr_request and host_sram_request.
 * This structure contains the data for the outputs.
 */
typedef struct t_bbc_display_outputs {
    t_sl_uint64 reset_n;
    t_sl_uint64 csr_request__valid;
    t_sl_uint64 csr_request__read_not_write;
    t_sl_uint64 csr_request__select;
    t_sl_uint64 csr_request__address;
    t_sl_uint64 csr_request__data;
    t_sl_uint64 host_sram_request__valid;
    t_sl_uint64 host_sram_request__read_enable;
    t_sl_uint64 host_sram_request__write_enable;
    t_sl_uint64 host_sram_request__select;
    t_sl_uint64 host_sram_request__address;
    t_sl_uint64 host_sram_request__write_data;
} t_bbc_display_outputs;

/*t t_bbc_display_sram_write */
/*t t_bbc_display_outputs */
/**
 * This structure is used to capture the values on the
 * display_sram_write input bus, so that those inputs may be used on a
 * relevant clock edge.
 */
typedef struct {
    int enable;
    int address;
    t_sl_uint64 data;
} t_bbc_display_sram_write;

/*t c_bbc_display*/
/**
 * Class for the 'bbc_display' module instance
 */
typedef struct {
    int read_not_write;
    int select;
    int address;
    unsigned int data;
} t_csr_request;
class c_bbc_display
{
public:
    c_bbc_display( class c_engine *eng, void *eng_handle );
    ~c_bbc_display();
    t_sl_error_level delete_instance( void );
    t_sl_error_level capture_inputs( void );
    t_sl_error_level prepreclock( void );
    t_sl_error_level preclock(void);
    t_sl_error_level clock( void );
    t_sl_error_level message( t_se_message *message );
private:
    void drive_pending_csr_request(void);
    void add_pending_csr_write_request(int select, int address, unsigned int data);
    c_engine *engine;
    int clocks_to_call;
    void *engine_handle;
    int inputs_captured;
    t_bbc_display_outputs outputs;
    t_bbc_display_sram_write_inputs inputs;
    t_bbc_display_sram_write input_display;
    t_bbc_csr_response csr_response;
    t_bbc_sram_response host_sram_response;
    t_keys_down req_keys_down;
    t_keys_down csr_keys_down;
    c_bbc_shm *shm;
    t_framebuffer_and_keys fbk;
    int verbose;
    int reset_cycle;
    int num_pending_csr_requests;
    int max_pending_csr_requests;
    t_csr_request pending_csr_requests[32];
};

/*a Static wrapper functions for bbc_display - standard off-the-shelf */
/*f bbc_display_instance_fn */
static t_sl_error_level
bbc_display_instance_fn( c_engine *engine, void *engine_handle )
{
    c_bbc_display *mod;
    mod = new c_bbc_display( engine, engine_handle );
    if (!mod)
        return error_level_fatal;
    return error_level_okay;
}

/*f bbc_display_delete_fn - simple callback wrapper for the main method */
static t_sl_error_level
bbc_display_delete_fn( void *handle )
{
    c_bbc_display *mod;
    t_sl_error_level result;
    mod = (c_bbc_display *)handle;
    result = mod->delete_instance();
    delete( mod );
    return result;
}

/*f bbc_display_prepreclock_fn */
static t_sl_error_level
bbc_display_prepreclock_fn( void *handle )
{
    c_bbc_display *mod;
    mod = (c_bbc_display *)handle;
    return mod->prepreclock();
}

/*f bbc_display_clock_fn */
static t_sl_error_level
bbc_display_clock_fn( void *handle )
{
    c_bbc_display *mod;
    mod = (c_bbc_display *)handle;
    return mod->clock();
}

/*f bbc_display_message  */
static t_sl_error_level
bbc_display_message( void *handle, void *arg )
{
    c_bbc_display *mod;
    mod = (c_bbc_display *)handle;
    return mod->message((t_se_message *)arg );
}

/*f bbc_display_preclock_posedge_clk_fn */
static t_sl_error_level
bbc_display_preclock_posedge_clk_fn( void *handle )
{
    c_bbc_display *mod;
    mod = (c_bbc_display *)handle;
    mod->preclock();
    return error_level_okay;
}

/*a Constructors and destructors for bbc_display */
/*f c_bbc_display::c_bbc_display */
/**
 * Constructor for module 'bbc_display' class
 *
 * Registers simulation engine functions
 *
 * Allocates shared memory (if possible)
 *
 * Registers inputs and outputs
 * 
 * Clears inputs
 */
c_bbc_display::c_bbc_display( class c_engine *eng, void *eng_handle )
{
    engine = eng;
    engine_handle = eng_handle;

    engine->register_delete_function( engine_handle, (void *)this, bbc_display_delete_fn );
    engine->register_message_function( engine_handle, (void *)this, bbc_display_message );

    const char *shm_lock_filename="/tmp/bbc_shm.lock";
    const int shm_key = 0xbbc;
    fbk.width  = 640;
    fbk.height = 600;
    fbk.interlaced = 1;
    fbk.field = 0;
    fbk.h_front_porch = 0;
    fbk.v_front_porch = 0;
    fbk.data_size = sizeof(fbk) + sizeof(t_sl_uint32) * fbk.width * fbk.height;
    shm = new c_bbc_shm(shm_lock_filename, shm_key, fbk.data_size);
    fbk.fbk = (t_framebuffer_and_keys *)shm->data;
    if (!fbk.fbk) {
        delete(shm);
        shm = NULL;
        fprintf(stderr,"Not using shared data as shm failed\n");
        fbk.fbk = (t_framebuffer_and_keys *)malloc(fbk.data_size);
    }
    *(fbk.fbk) = fbk;
    fbk.fbk->keys_down.cols_0_to_7 = 0;
    fbk.fbk->keys_down.cols_8_to_9 = 0;
    fbk.fbk->reset_pressed = 0;
    csr_keys_down.cols_0_to_7 = 0;
    csr_keys_down.cols_8_to_9 = 0;
    num_pending_csr_requests = 0;
    max_pending_csr_requests = sizeof(pending_csr_requests)/sizeof(pending_csr_requests[0]);

    memset(&inputs, 0, sizeof(inputs));
    memset(&input_display, 0, sizeof(input_display));

    engine->register_prepreclock_fn( engine_handle, (void *)this, bbc_display_prepreclock_fn );
    engine->register_preclock_fns( engine_handle, (void *)this, "clk", bbc_display_preclock_posedge_clk_fn, (t_engine_callback_fn) NULL );
    engine->register_clock_fn( engine_handle, (void *)this, "clk", engine_sim_function_type_posedge_clock, bbc_display_clock_fn );

#define REGISTER_OUTPUT(s,w) \
    engine->register_output_signal(engine_handle, #s, w, &outputs.s); \
    engine->register_output_generated_on_clock(engine_handle, #s, "clk", 1 );
#define REGISTER_INPUT(s,w) \
    engine->register_input_signal(engine_handle, #s, w, &inputs.s); \
    engine->register_input_used_on_clock(engine_handle, #s, "clk", 1 );
    REGISTER_INPUT(display_sram_write__enable,1);
    REGISTER_INPUT(display_sram_write__data,48);
    REGISTER_INPUT(display_sram_write__address,16);

    REGISTER_INPUT(csr_response__ack,1);
    REGISTER_INPUT(csr_response__read_data_valid,1);
    REGISTER_INPUT(csr_response__read_data,32);

    REGISTER_INPUT(host_sram_response__ack,1);
    REGISTER_INPUT(host_sram_response__read_data_valid,1);
    REGISTER_INPUT(host_sram_response__read_data,64);

    REGISTER_OUTPUT(reset_n,1);

    REGISTER_OUTPUT(csr_request__valid,1);
    REGISTER_OUTPUT(csr_request__read_not_write,1);
    REGISTER_OUTPUT(csr_request__select,16);
    REGISTER_OUTPUT(csr_request__address,16);
    REGISTER_OUTPUT(csr_request__data,32);

    REGISTER_OUTPUT(host_sram_request__valid,1);
    REGISTER_OUTPUT(host_sram_request__read_enable,1);
    REGISTER_OUTPUT(host_sram_request__write_enable,1);
    REGISTER_OUTPUT(host_sram_request__select,8);
    REGISTER_OUTPUT(host_sram_request__address,24);
    REGISTER_OUTPUT(host_sram_request__write_data,64);

    reset_cycle = 100;
    outputs.reset_n = 0;
    outputs.csr_request__valid = 0;
    outputs.host_sram_request__valid = 0;
}

/*f c_bbc_display::~c_bbc_display */
/**
 * Standard destructor for bbc_display module class
 */
c_bbc_display::~c_bbc_display()
{
    delete_instance();
}

/*f c_bbc_display::delete_instance */
/**
 * Standard destructor for bbc_display module class
 */
t_sl_error_level c_bbc_display::delete_instance( void )
{
    return error_level_okay;
}

/*f c_bbc_display::message */
/**
 * Handle a message sent to the module in the simulation environment
 *
 * This is currently a hack to just save the frame buffer as a PNG
 * when invoked with any message.
 *
 */
t_sl_error_level c_bbc_display::message( t_se_message *message )
{
    fprintf(stderr,"Got message %d\n",message->reason);
    image_write_rgba("fred.png", (const unsigned char *)fbk.fbk->fb_data, fbk.width, fbk.height);
    switch (message->reason)
    {
    case se_message_reason_set_option:
        const char *option_name;
        option_name = (const char *)message->data.ptrs[0];
        message->response_type = se_message_response_type_int;
        message->response = 1;
        if (!strcmp(option_name,"verbose"))
        {
            verbose = (int)(t_sl_uint64)message->data.ptrs[1];
        }
        else
        {
            message->response = -1;
        }
        break;
    }
    return error_level_okay;
}

/*a Class preclock/clock methods for bbc_display
*/
/*f c_bbc_display::capture_inputs */
/**
 * Capture inputs - happens prior to relevant clock edges
 *
 */
t_sl_error_level
c_bbc_display::capture_inputs( void )
{
    input_display.enable  = inputs.display_sram_write__enable[0];
    input_display.data    = inputs.display_sram_write__data[0];
    input_display.address = inputs.display_sram_write__address[0];
    csr_response.ack               = inputs.csr_response__ack[0];
    csr_response.read_data_valid   = inputs.csr_response__read_data_valid[0];
    csr_response.read_data         = inputs.csr_response__read_data[0];
    host_sram_response.ack          = inputs.host_sram_response__ack[0];
    host_sram_response.read_data_valid   = inputs.host_sram_response__read_data_valid[0];
    host_sram_response.read_data         = inputs.host_sram_response__read_data[0];
    return error_level_okay;
}

/*f c_bbc_display::prepreclock */
/**
 * Prepreclock call, invoked on every clock edge before any preclock or
 * clock functions, permitting clearing of appropriate guards
 */
t_sl_error_level
c_bbc_display::prepreclock( void )
{
    inputs_captured=0;
    clocks_to_call=0;
    return error_level_okay;
}

/*f c_bbc_display::preclock */
/**
 * Preclock call, invoked after a prepreclock if the clock is going to
 * fire; inputs must be captured at this point (as they may be invalid
 * at 'clock').
 */
t_sl_error_level
c_bbc_display::preclock(void)
{
    if (!inputs_captured) { capture_inputs(); inputs_captured++; }
    clocks_to_call++;
    return error_level_okay;
}

/*f c_bbc_display::clock */
/**
 * Clock call, invoked after all preclock calls. Handle any clock
 * edges indicated required by 'preclock' calls.
 */
void
c_bbc_display::add_pending_csr_write_request(int select, int address, unsigned int data) {
    t_csr_request *csr_request;
    if (num_pending_csr_requests == max_pending_csr_requests)
        return;
    csr_request = &(pending_csr_requests[num_pending_csr_requests]);
    num_pending_csr_requests++;
    csr_request->read_not_write = 0;
    csr_request->select = select;
    csr_request->address = address;
    csr_request->data = data;
}
void
c_bbc_display::drive_pending_csr_request(void) {
    outputs.csr_request__valid = 0;
    if (num_pending_csr_requests==0) return;
    outputs.csr_request__valid = 1;
    outputs.csr_request__read_not_write = 0;
    outputs.csr_request__select  = pending_csr_requests[0].select;
    outputs.csr_request__address = pending_csr_requests[0].address;
    outputs.csr_request__data    = pending_csr_requests[0].data;
    num_pending_csr_requests--;
    for (int i=0; i<num_pending_csr_requests; i++) {
        pending_csr_requests[i] = pending_csr_requests[i+1];
    }
    fprintf(stderr,"Popped to %d requests\n",num_pending_csr_requests);
}
t_sl_error_level
c_bbc_display::clock( void )
{
    if (clocks_to_call>0) {
        clocks_to_call=0;

        if (input_display.enable) {
            int address;
            address = input_display.address*16;
            if (address<0) {address=0;}
            if (address>fbk.width*fbk.height-16) {address=0;}
            for (int i=0; i<16; i++) {
                int ibr = (15-i);
                int ibg = (31-i);
                int ibb = (47-i);
                t_sl_uint32 color = ( ((input_display.data &(1ULL<<ibr))?0x0000ff:0x000000) |
                                      ((input_display.data &(1ULL<<ibg))?0x00ff00:0x000000) |
                                      ((input_display.data &(1ULL<<ibb))?0xff0000:0x000000));
                fbk.fbk->fb_data[address++] = (color | 0xff000000);
            }
        }
        outputs.reset_n = !(reset_cycle>0);
        if (reset_cycle>0) { reset_cycle--; }
        if (fbk.fbk->reset_pressed) { reset_cycle=10000; }
        if (reset_cycle==1) {
            add_pending_csr_write_request(bbc_csr_select_clocks, 0, (2<<8) | (3<<0) );// clock speedup
            add_pending_csr_write_request(bbc_csr_select_display, 0, (40<<16) | (0<<0) );// SRAM base address
            add_pending_csr_write_request(bbc_csr_select_display, 1, (1<<30) | (500<<20) | (40<<10) | (40<<0) );// SRAM scan lines and writes per scanline
            add_pending_csr_write_request(bbc_csr_select_display, 2, ((65536-70)<<16) | ((65536-140)<<0) );// video porches
        }
        //keyboard__reset_pressed         = fbk.fbk->reset_pressed;
        req_keys_down.cols_0_to_7 = fbk.fbk->keys_down.cols_0_to_7 | 1;
        req_keys_down.cols_8_to_9 = fbk.fbk->keys_down.cols_8_to_9;
        if ((csr_keys_down.cols_0_to_7&0xffffffff) != (req_keys_down.cols_0_to_7&0xffffffff)) {
            add_pending_csr_write_request(bbc_csr_select_keyboard, 8, req_keys_down.cols_0_to_7&0xffffffff);
        }
        if ((csr_keys_down.cols_0_to_7&0xffffffff00000000ULL) != (req_keys_down.cols_0_to_7&0xffffffff00000000ULL)) {
            add_pending_csr_write_request(bbc_csr_select_keyboard, 9, req_keys_down.cols_0_to_7>>32);
        }
        if ((csr_keys_down.cols_8_to_9&0xffff) != (req_keys_down.cols_8_to_9&0xffff)) {
            add_pending_csr_write_request(bbc_csr_select_keyboard, 10, req_keys_down.cols_8_to_9);
        }
        csr_keys_down.cols_0_to_7 = req_keys_down.cols_0_to_7;
        csr_keys_down.cols_8_to_9 = req_keys_down.cols_8_to_9;
        if ((outputs.csr_request__valid==0) && (outputs.reset_n) && !csr_response.ack) {
            drive_pending_csr_request();
        }
        if (csr_response.ack) {
            outputs.csr_request__valid = 0;
        }
        if (outputs.host_sram_request__valid==0) {
            outputs.host_sram_request__valid=1;
            outputs.host_sram_request__select = bbc_sram_select_cpu_ram_1;
            outputs.host_sram_request__read_enable = 1;
            outputs.host_sram_request__write_enable = 0;
            outputs.host_sram_request__address = ((outputs.host_sram_request__address+1) & 0xfff)|0x3c00;
            outputs.host_sram_request__write_data = 0xdeadbeeff00dcafeULL + outputs.host_sram_request__address;
        }
        if (host_sram_response.ack) {
            outputs.host_sram_request__valid = 0;
        }
    }
    return error_level_okay;
}

/*a Initialization functions */
/*f bbc_display__init */
/**
 * Initialize the module with the simulation engine
 */
extern void
bbc_display__init( void )
{
    se_external_module_register( 1, "bbc_display", bbc_display_instance_fn, "cdl_model" );
}

/*a Scripting support code
*/
/*f initbbc_display */
/**
 * External function invoked by the simulation engine when the library
 * is loaded, to register the module
 */
extern "C" void
initbbc_display( void )
{
    bbc_display__init( );
    scripting_init_module( "bbc_display" );
}

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
