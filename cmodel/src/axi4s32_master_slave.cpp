/** Copyright (C) 2018,  Gavin J Stark.  All rights reserved.
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
 * @file   axi4s32_master_slave.cpp
 * @brief  BBC microcomputer display
 *
 * BBC display C model source code, which uses the BBC shared memory
 * (SHM) to create a SHM frame buffer and keyboard interaction for CDL
 * simulations. The axi4s32_master_slave_vnc program can be used to interact
 * with this SHM, allowing a simulation to be viewed, and to have
 * keyboard and reset interactions.
 *
 * The initial cut of this source code is from CDL C model output.
 *
 */
/*a Includes */
#include "be_model_includes.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "sl_exec_file.h"
#include "axi_types.h"
#include "axi.h"

/*a Defines
 */
#if 1   
#define WHERE_I_AM {}
#else
#define WHERE_I_AM {fprintf(stderr,"%s:%d\n",__func__,__LINE__ );}
#endif

/*a Types for axi4s32_master_slave */
/*t t_axi4s32_master_slave_input_ptrs */
/**
 */
typedef struct t_axi4s32_master_slave_input_ptrs {
    t_sl_uint64 *areset_n;

    t_sl_uint64 *master_axi4s_tready;

    t_sl_uint64 *slave_axi4s__valid;
    t_sl_uint64 *slave_axi4s__t__keep;
    t_sl_uint64 *slave_axi4s__t__strb;
    t_sl_uint64 *slave_axi4s__t__data;
    t_sl_uint64 *slave_axi4s__t__last;
    t_sl_uint64 *slave_axi4s__t__user;
    t_sl_uint64 *slave_axi4s__t__id;
    t_sl_uint64 *slave_axi4s__t__dest;
} t_axi4s32_master_slave_input_ptrs;

/*t t_axi4s32_master_slave_input_values */
/**
 */
typedef struct t_axi4s32_master_slave_input_values {
    t_sl_uint64 areset_n;

    t_sl_uint64 master_axi4s_tready;

    t_sl_uint64 slave_axi4s__valid;
    t_sl_uint64 slave_axi4s__t__keep;
    t_sl_uint64 slave_axi4s__t__strb;
    t_sl_uint64 slave_axi4s__t__data;
    t_sl_uint64 slave_axi4s__t__last;
    t_sl_uint64 slave_axi4s__t__user;
    t_sl_uint64 slave_axi4s__t__id;
    t_sl_uint64 slave_axi4s__t__dest;
} t_axi4s32_master_slave_input_values;

/*t t_axi4s32_master_slave_outputs */
/**
 */
typedef struct t_axi4s32_master_slave_outputs {
    t_sl_uint64 slave_axi4s_tready;

    t_sl_uint64 master_axi4s__valid;
    t_sl_uint64 master_axi4s__t__keep;
    t_sl_uint64 master_axi4s__t__strb;
    t_sl_uint64 master_axi4s__t__data;
    t_sl_uint64 master_axi4s__t__last;
    t_sl_uint64 master_axi4s__t__user;
    t_sl_uint64 master_axi4s__t__id;
    t_sl_uint64 master_axi4s__t__dest;
} t_axi4s32_master_slave_outputs;

/*t c_axi4s32_master_slave */
/**
 * Class for the 'axi4s32_master_slave' module instance
 */
class c_axi4s32_master_slave
{
public:
    c_axi4s32_master_slave( class c_engine *eng, void *eng_handle );
    ~c_axi4s32_master_slave();
    t_sl_error_level delete_instance( void );
    t_sl_error_level capture_inputs( void );
    t_sl_error_level prepreclock( void );
    t_sl_error_level preclock(void);
    t_sl_error_level clock( void );
    t_sl_error_level reset( int pass );
    t_sl_error_level message( t_se_message *message );
    void add_exec_file_enhancements(void);
    class c_axi_queue<t_axi4s> *master_fifo;
    class c_axi_queue<t_axi4s> *slave_fifo;
private:
    //void drive_pending_csr_request(void);
    //void add_pending_csr_write_request(int select, int address, unsigned int data);
    c_engine *engine;
    int clocks_to_call;
    void *engine_handle;
    int inputs_captured;
    t_axi4s32_master_slave_outputs outputs;
    t_axi4s32_master_slave_input_ptrs   inputs;
    t_axi4s32_master_slave_input_values input_values;
    t_sl_exec_file_data *exec_file_data;
    int verbose;
    int data_width;
    int keep_width;
    int strb_width;
    int user_width;
    int dest_width;
    int id_width;
    int master_fifo_size;
    int slave_fifo_size;
    int has_reset;
};

/*a Static wrapper functions for axi4s32_master_slave - standard off-the-shelf */
/*f axi4s32_master_slave_instance_fn */
static t_sl_error_level
axi4s32_master_slave_instance_fn( c_engine *engine, void *engine_handle )
{
    c_axi4s32_master_slave *mod;
    mod = new c_axi4s32_master_slave( engine, engine_handle );
    if (!mod)
        return error_level_fatal;
    return error_level_okay;
}

/*f axi4s32_master_slave_delete_fn - simple callback wrapper for the main method */
static t_sl_error_level
axi4s32_master_slave_delete_fn( void *handle )
{
    c_axi4s32_master_slave *mod;
    t_sl_error_level result;
    mod = (c_axi4s32_master_slave *)handle;
    result = mod->delete_instance();
    delete( mod );
    return result;
}

/*f axi4s32_master_slave_reset_fn
*/
static t_sl_error_level axi4s32_master_slave_reset_fn( void *handle, int pass )
{
    c_axi4s32_master_slave *mod;
    mod = (c_axi4s32_master_slave *)handle;
    return mod->reset( pass );
}

/*f axi4s32_master_slave_prepreclock_fn */
static t_sl_error_level
axi4s32_master_slave_prepreclock_fn( void *handle )
{
    c_axi4s32_master_slave *mod;
    mod = (c_axi4s32_master_slave *)handle;
    return mod->prepreclock();
}

/*f axi4s32_master_slave_clock_fn */
static t_sl_error_level
axi4s32_master_slave_clock_fn( void *handle )
{
    c_axi4s32_master_slave *mod;
    mod = (c_axi4s32_master_slave *)handle;
    return mod->clock();
}

/*f axi4s32_master_slave_message  */
static t_sl_error_level
axi4s32_master_slave_message( void *handle, void *arg )
{
    c_axi4s32_master_slave *mod;
    mod = (c_axi4s32_master_slave *)handle;
    return mod->message((t_se_message *)arg );
}

/*f axi4s32_master_slave_preclock_posedge_clk_fn */
static t_sl_error_level
axi4s32_master_slave_preclock_posedge_clk_fn( void *handle )
{
    c_axi4s32_master_slave *mod;
    mod = (c_axi4s32_master_slave *)handle;
    mod->preclock();
    return error_level_okay;
}

/*a Constructors and destructors for axi4s32_master_slave */
/*f exec_file_instantiate_callback
 */
static void exec_file_instantiate_callback( void *handle, struct t_sl_exec_file_data *file_data )
{
    c_axi4s32_master_slave *axim = (c_axi4s32_master_slave *)handle;
    axim->add_exec_file_enhancements();
}

/*f c_axi4s32_master_slave::c_axi4s32_master_slave */
/**
 * Constructor for module 'axi4s32_master_slave' class
 *
 * Registers simulation engine functions
 *
 * Allocates shared memory (if possible)
 *
 * Registers inputs and outputs
 * 
 * Clears inputs
 */
c_axi4s32_master_slave::c_axi4s32_master_slave( class c_engine *eng, void *eng_handle )
{
    engine = eng;
    engine_handle = eng_handle;

    engine->register_delete_function( engine_handle, (void *)this, axi4s32_master_slave_delete_fn );
    engine->register_reset_function( engine_handle, (void *)this, axi4s32_master_slave_reset_fn );
    engine->register_message_function( engine_handle, (void *)this, axi4s32_master_slave_message );

    verbose       = engine->get_option_int( engine_handle, "verbose", 0 );
    data_width    = engine->get_option_int( engine_handle, "data_width", 32 );
    keep_width    = engine->get_option_int( engine_handle, "keep_width", data_width/8 );
    strb_width    = engine->get_option_int( engine_handle, "strb_width", data_width/8 );
    user_width    = engine->get_option_int( engine_handle, "user_width", 64 );
    id_width      = engine->get_option_int( engine_handle, "id_width", 64 );
    dest_width    = engine->get_option_int( engine_handle, "dest_width", 64 );

    master_fifo_size = engine->get_option_int( engine_handle, "master_fifo_size", 32 );
    slave_fifo_size  = engine->get_option_int( engine_handle, "slave_fifo_size", 32 );
    has_reset = 0;

    master_fifo  = new c_axi_queue<t_axi4s>(master_fifo_size);
    slave_fifo  = new c_axi_queue<t_axi4s>(slave_fifo_size);

    memset(&inputs, 0, sizeof(inputs));

    engine->register_prepreclock_fn( engine_handle, (void *)this, axi4s32_master_slave_prepreclock_fn );
    engine->register_preclock_fns( engine_handle, (void *)this, "aclk", axi4s32_master_slave_preclock_posedge_clk_fn, (t_engine_callback_fn) NULL );
    engine->register_clock_fn( engine_handle, (void *)this, "aclk", engine_sim_function_type_posedge_clock, axi4s32_master_slave_clock_fn );

#define REGISTER_OUTPUT(s,w) \
    engine->register_output_signal(engine_handle, #s, w, &outputs.s); \
    engine->register_output_generated_on_clock(engine_handle, #s, "aclk", 1 );
#define REGISTER_INPUT(s,w) \
    engine->register_input_signal(engine_handle, #s, w, &inputs.s); \
    engine->register_input_used_on_clock(engine_handle, #s, "aclk", 1 );

    REGISTER_INPUT(master_axi4s_tready,1);
    REGISTER_OUTPUT(master_axi4s__valid,1);
    REGISTER_OUTPUT(master_axi4s__t__id,id_width);
    REGISTER_OUTPUT(master_axi4s__t__data,data_width);
    REGISTER_OUTPUT(master_axi4s__t__keep,keep_width);
    REGISTER_OUTPUT(master_axi4s__t__strb,strb_width);
    REGISTER_OUTPUT(master_axi4s__t__user,user_width);
    REGISTER_OUTPUT(master_axi4s__t__id,id_width);
    REGISTER_OUTPUT(master_axi4s__t__dest,dest_width);
    REGISTER_OUTPUT(master_axi4s__t__last,1);

    REGISTER_OUTPUT(slave_axi4s_tready,1);
    REGISTER_INPUT(slave_axi4s__valid,1);
    REGISTER_INPUT(slave_axi4s__t__id,id_width);
    REGISTER_INPUT(slave_axi4s__t__data,data_width);
    REGISTER_INPUT(slave_axi4s__t__keep,keep_width);
    REGISTER_INPUT(slave_axi4s__t__strb,strb_width);
    REGISTER_INPUT(slave_axi4s__t__user,user_width);
    REGISTER_INPUT(slave_axi4s__t__id,id_width);
    REGISTER_INPUT(slave_axi4s__t__dest,dest_width);
    REGISTER_INPUT(slave_axi4s__t__last,1);

    exec_file_data = NULL;
    PyObject *obj = (PyObject *)(engine->get_option_object( engine_handle, "object" ));

    if (obj)
    {
        sl_exec_file_allocate_from_python_object( engine->error, engine->message, exec_file_instantiate_callback, (void *)this, "exec_file", obj, &exec_file_data, "AXI master", 1 );
    }

}

/*f c_axi4s32_master_slave::~c_axi4s32_master_slave */
/**
 * Standard destructor for axi4s32_master_slave module class
 */
c_axi4s32_master_slave::~c_axi4s32_master_slave()
{
    delete_instance();
}

/*f c_axi4s32_master_slave::delete_instance */
/**
 * Standard destructor for axi4s32_master_slave module class
 */
t_sl_error_level c_axi4s32_master_slave::delete_instance( void )
{
    if (exec_file_data )
    {
        sl_exec_file_free( exec_file_data );
        exec_file_data = NULL;
    }
    return error_level_okay;
}

/*f c_axi4s32_master_slave::message */
/**
 * Handle a message sent to the module in the simulation environment
 *
 * This is currently a hack to just save the frame buffer as a PNG
 * when invoked with any message.
 *
 */
t_sl_error_level c_axi4s32_master_slave::message( t_se_message *message )
{
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

/*f c_axi4s32_master_slave::add_exec_file_enhancements
 */

/*f ef_set
 */
static t_sl_error_level ef_master_enqueue(t_sl_exec_file_cmd_cb *cmd_cb, void *obj, t_sl_exec_file_object_desc *object_desc, t_sl_exec_file_method *method)
{
    WHERE_I_AM;
    c_axi4s32_master_slave *axim = (c_axi4s32_master_slave *)ef_owner_of_objf(object_desc);
    t_axi4s *axi4s = ef_axi4s_of_objf(object_desc);
    t_sl_uint64 delay = sl_exec_file_eval_fn_get_argument_integer( cmd_cb->file_data, cmd_cb->args, 0 );
    return sl_exec_file_eval_fn_set_result(cmd_cb->file_data, (t_sl_uint64)(!!axim->master_fifo->enqueue(axi4s, delay)))?error_level_okay:error_level_fatal;
}
static t_sl_error_level ef_slave_dequeue(t_sl_exec_file_cmd_cb *cmd_cb, void *obj, t_sl_exec_file_object_desc *object_desc, t_sl_exec_file_method *method)
{
    WHERE_I_AM;
    c_axi4s32_master_slave *axim = (c_axi4s32_master_slave *)ef_owner_of_objf(object_desc);
    t_axi4s *axi4s = ef_axi4s_of_objf(object_desc);
    return sl_exec_file_eval_fn_set_result(cmd_cb->file_data, (t_sl_uint64)(!!axim->slave_fifo->dequeue(axi4s, NULL)))?error_level_okay:error_level_fatal;
}
static t_sl_error_level ef_slave_empty(t_sl_exec_file_cmd_cb *cmd_cb, void *obj, t_sl_exec_file_object_desc *object_desc, t_sl_exec_file_method *method)
{
    WHERE_I_AM;
    c_axi4s32_master_slave *axim = (c_axi4s32_master_slave *)ef_owner_of_objf(object_desc);
    return sl_exec_file_eval_fn_set_result(cmd_cb->file_data, (t_sl_uint64)axim->slave_fifo->is_empty())?error_level_okay:error_level_fatal;
}

static t_sl_exec_file_method axi4s_obj_additional_methods[] =
{
    {"master_enqueue", 'i',  1, "i",  "master_enqueue(<delay>)", ef_master_enqueue, NULL },
    {"slave_dequeue",  'i',  0, "i",  "slave_dequeue()",         ef_slave_dequeue, NULL },
    {"slave_empty",    'i',  0, "i",  "slave_empty()",           ef_slave_empty, NULL },
    SL_EXEC_FILE_METHOD_NONE
};
static int ef_fn_axi4s(void *handle, t_sl_exec_file_data *file_data, t_sl_exec_file_value *args)
{
    const char *name = sl_exec_file_eval_fn_get_argument_string(file_data, args, 0);
    t_axi4s *axi4s = (t_axi4s *)malloc(sizeof(t_axi4s));
    void *ef_object = ef_axi4s_create(file_data, name, handle, axi4s, axi4s_obj_additional_methods );
    return (ef_object==NULL) ? error_level_serious : error_level_okay;
}

static t_sl_exec_file_fn ef_fns[] =
{
    {0, "axi4s", 'i', "s", "axi4s(<name>) - create an axi4s data object called 'name'", ef_fn_axi4s },
    SL_EXEC_FILE_FN_NONE
};
void c_axi4s32_master_slave::add_exec_file_enhancements(void)
{
    t_sl_exec_file_lib_desc lib_desc;

    sl_exec_file_set_environment_interrogation( exec_file_data, (t_sl_get_environment_fn)sl_option_get_string, (void *)engine->get_option_list( engine_handle ) );

    lib_desc.version = sl_ef_lib_version_cmdcb;
    lib_desc.library_name = "axi_bfm";
    lib_desc.handle = (void *)this;
    lib_desc.cmd_handler = NULL;//exec_file_cmd_handler_cb;
    lib_desc.file_cmds = NULL;//ef_cmds;
    lib_desc.file_fns  = ef_fns;
    sl_exec_file_add_library( exec_file_data, &lib_desc );

    engine->bfm_add_exec_file_enhancements( exec_file_data, engine_handle, "aclk", 1 );
}

/*a Class preclock/clock methods for axi4s32_master_slave
*/
/*f c_axi4s32_master_slave::capture_inputs */
/**
 * Capture inputs - happens prior to relevant clock edges
 *
 */
t_sl_error_level
c_axi4s32_master_slave::capture_inputs( void )
{
    input_values.master_axi4s_tready = inputs.master_axi4s_tready[0];

    input_values.slave_axi4s__valid = inputs.slave_axi4s__valid[0];
    input_values.slave_axi4s__t__keep = inputs.slave_axi4s__t__keep[0];
    input_values.slave_axi4s__t__strb = inputs.slave_axi4s__t__strb[0];
    input_values.slave_axi4s__t__data = inputs.slave_axi4s__t__data[0];
    input_values.slave_axi4s__t__last = inputs.slave_axi4s__t__last[0];
    input_values.slave_axi4s__t__user = inputs.slave_axi4s__t__user[0];
    input_values.slave_axi4s__t__id = inputs.slave_axi4s__t__id[0];
    input_values.slave_axi4s__t__dest = inputs.slave_axi4s__t__dest[0];

    return error_level_okay;
}

/*f c_axi4s32_master_slave::prepreclock */
/**
 * Prepreclock call, invoked on every clock edge before any preclock or
 * clock functions, permitting clearing of appropriate guards
 */
t_sl_error_level
c_axi4s32_master_slave::prepreclock( void )
{
    inputs_captured=0;
    clocks_to_call=0;
    return error_level_okay;
}

/*f c_axi4s32_master_slave::preclock */
/**
 * Preclock call, invoked after a prepreclock if the clock is going to
 * fire; inputs must be captured at this point (as they may be invalid
 * at 'clock').
 */
t_sl_error_level
c_axi4s32_master_slave::preclock(void)
{
    if (!inputs_captured) {
        capture_inputs();
        inputs_captured++;

        if (!has_reset) {
            if (exec_file_data)
                sl_exec_file_reset( exec_file_data );
            has_reset = 1;
        }

        if (exec_file_data)
            sl_exec_file_send_message_to_object( exec_file_data, "bfm_exec_file_support", "preclock", NULL );
    }
    clocks_to_call++;
    return error_level_okay;
}

/*f c_axi4s32_master_slave::clock */
/**
 * Clock call, invoked after all preclock calls. Handle any clock
 * edges indicated required by 'preclock' calls.
 */
t_sl_error_level
c_axi4s32_master_slave::clock( void )
{
    if (clocks_to_call>0) {
        clocks_to_call=0;
    }
    /*b Run the exec_file
     */
    WHERE_I_AM;
    if (exec_file_data)
    {
        while (sl_exec_file_despatch_next_cmd( exec_file_data ));
    }
    // free any events we are done with - any that fired a few clock ticks ago

    /*b Call BFM clock function
     */
    WHERE_I_AM;
    if (exec_file_data)
        sl_exec_file_send_message_to_object( exec_file_data, "bfm_exec_file_support", "clock", NULL );

    /*b Handle master
     */
    if (outputs.master_axi4s__valid && input_values.master_axi4s_tready) {
        outputs.master_axi4s__valid = 0;
        outputs.master_axi4s__t__data = 0;
        outputs.master_axi4s__t__strb = 0;
        outputs.master_axi4s__t__keep = 0;
        outputs.master_axi4s__t__last = 0;
        outputs.master_axi4s__t__user = 0;
        outputs.master_axi4s__t__id = 0;
        outputs.master_axi4s__t__dest = 0;
    }
    if (!outputs.master_axi4s__valid && !master_fifo->is_empty()) {
        t_axi4s axi4s;
        int delay;
        master_fifo->dequeue(&axi4s, &delay);
        outputs.master_axi4s__valid = 1;
        outputs.master_axi4s__t__data = axi4s.data;
        outputs.master_axi4s__t__strb = axi4s.strb;
        outputs.master_axi4s__t__keep = axi4s.keep;
        outputs.master_axi4s__t__last = axi4s.last;
        outputs.master_axi4s__t__user = axi4s.user;
        outputs.master_axi4s__t__id   = axi4s.id;
        outputs.master_axi4s__t__dest = axi4s.dest;
    }

    /*b Handle slave
     */
    if (input_values.slave_axi4s__valid && outputs.slave_axi4s_tready) {
        t_axi4s axi4s;
        axi4s.data = input_values.slave_axi4s__t__data;
        axi4s.strb = input_values.slave_axi4s__t__strb;
        axi4s.keep = input_values.slave_axi4s__t__keep;
        axi4s.last = input_values.slave_axi4s__t__last;
        axi4s.user = input_values.slave_axi4s__t__user;
        axi4s.id   = input_values.slave_axi4s__t__id  ;
        axi4s.dest = input_values.slave_axi4s__t__dest ;
        slave_fifo->enqueue(&axi4s, 0);
    }
    outputs.slave_axi4s_tready = !slave_fifo->is_full();

    /*b All done
     */
    return error_level_okay;
}

/*f c_axi4s32_master_slave::reset
*/
t_sl_error_level c_axi4s32_master_slave::reset( int pass )
{
    memset(&input_values, 0, sizeof(input_values));
    memset(&outputs, 0, sizeof(outputs));
    return error_level_okay;
}
/*a Initialization functions */
/*f axi4s32_master_slave__init */
/**
 * Initialize the module with the simulation engine
 */
extern void
axi4s32_master_slave__init( void )
{
    se_external_module_register( 1, "axi4s32_master_slave", axi4s32_master_slave_instance_fn, "cdl_model" );
}

/*a Scripting support code
*/
/*f initaxi4s32_master_slave */
/**
 * External function invoked by the simulation engine when the library
 * is loaded, to register the module
 */
extern "C" void
initaxi4s32_master_slave( void )
{
    axi4s32_master_slave__init( );
    scripting_init_module( "axi4s32_master_slave" );
}

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
