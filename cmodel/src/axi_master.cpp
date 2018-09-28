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
 * @file   axi_master.cpp
 * @brief  BBC microcomputer display
 *
 * BBC display C model source code, which uses the BBC shared memory
 * (SHM) to create a SHM frame buffer and keyboard interaction for CDL
 * simulations. The axi_master_vnc program can be used to interact
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

/*a Types for axi_master */
/*t t_axi_master_inputs */
/**
 */
typedef struct t_axi_master_inputs {
    t_sl_uint64 *areset_n;

    t_sl_uint64 *awready;
    t_sl_uint64 *arready;
    t_sl_uint64 *wready;

    t_sl_uint64 *b__valid;
    t_sl_uint64 *b__id;
    t_sl_uint64 *b__resp;
    t_sl_uint64 *b__user;

    t_sl_uint64 *r__valid;
    t_sl_uint64 *r__id;
    t_sl_uint64 *r__data;
    t_sl_uint64 *r__resp;
    t_sl_uint64 *r__last;
    t_sl_uint64 *r__user;
} t_axi_master_inputs;

/*t t_axi_master_outputs */
/**
 */
typedef struct t_axi_master_outputs {
    t_sl_uint64 aw__valid;
    t_sl_uint64 aw__id;
    t_sl_uint64 aw__addr;
    t_sl_uint64 aw__len;
    t_sl_uint64 aw__size;
    t_sl_uint64 aw__burst;
    t_sl_uint64 aw__lock;
    t_sl_uint64 aw__cache;
    t_sl_uint64 aw__prot;
    t_sl_uint64 aw__qos;
    t_sl_uint64 aw__region;
    t_sl_uint64 aw__user;

    t_sl_uint64 ar__valid;
    t_sl_uint64 ar__id;
    t_sl_uint64 ar__addr;
    t_sl_uint64 ar__len;
    t_sl_uint64 ar__size;
    t_sl_uint64 ar__burst;
    t_sl_uint64 ar__lock;
    t_sl_uint64 ar__cache;
    t_sl_uint64 ar__prot;
    t_sl_uint64 ar__qos;
    t_sl_uint64 ar__region;
    t_sl_uint64 ar__user;

    t_sl_uint64 w__valid;
    t_sl_uint64 w__id;
    t_sl_uint64 w__data;
    t_sl_uint64 w__strb;
    t_sl_uint64 w__last;
    t_sl_uint64 w__user;

    t_sl_uint64 bready;
    t_sl_uint64 rready;

} t_axi_master_outputs;

/*t c_axi_master */
/**
 * Class for the 'axi_master' module instance
 */
class c_axi_master
{
public:
    c_axi_master( class c_engine *eng, void *eng_handle );
    ~c_axi_master();
    t_sl_error_level delete_instance( void );
    t_sl_error_level capture_inputs( void );
    t_sl_error_level prepreclock( void );
    t_sl_error_level preclock(void);
    t_sl_error_level clock( void );
    t_sl_error_level reset( int pass );
    t_sl_error_level message( t_se_message *message );
    void add_exec_file_enhancements(void);
    class c_axi_queue<t_axi_request> *wreq_fifo;
    class c_axi_queue<t_axi_request> *rreq_fifo;
    class c_axi_queue<t_axi_write_data> *wdata_fifo;
    class c_axi_queue<t_axi_write_response> *wresp_fifo;
    class c_axi_queue<t_axi_read_response>  *rresp_fifo;
private:
    //void drive_pending_csr_request(void);
    //void add_pending_csr_write_request(int select, int address, unsigned int data);
    c_engine *engine;
    int clocks_to_call;
    void *engine_handle;
    int inputs_captured;
    t_axi_master_outputs outputs;
    t_axi_master_inputs inputs;
    // captured inputs...
    int awready;
    int arready;
    int wready;
    t_axi_write_response write_response;
    t_axi_read_response read_response;
    t_sl_exec_file_data *exec_file_data;
    int verbose;
    int address_width;
    int data_width;
    int len_width;
    int id_width;
    int has_reset;
};

/*a Static wrapper functions for axi_master - standard off-the-shelf */
/*f axi_master_instance_fn */
static t_sl_error_level
axi_master_instance_fn( c_engine *engine, void *engine_handle )
{
    c_axi_master *mod;
    mod = new c_axi_master( engine, engine_handle );
    if (!mod)
        return error_level_fatal;
    return error_level_okay;
}

/*f axi_master_delete_fn - simple callback wrapper for the main method */
static t_sl_error_level
axi_master_delete_fn( void *handle )
{
    c_axi_master *mod;
    t_sl_error_level result;
    mod = (c_axi_master *)handle;
    result = mod->delete_instance();
    delete( mod );
    return result;
}

/*f axi_master_reset_fn
*/
static t_sl_error_level axi_master_reset_fn( void *handle, int pass )
{
    c_axi_master *mod;
    mod = (c_axi_master *)handle;
    return mod->reset( pass );
}

/*f axi_master_prepreclock_fn */
static t_sl_error_level
axi_master_prepreclock_fn( void *handle )
{
    c_axi_master *mod;
    mod = (c_axi_master *)handle;
    return mod->prepreclock();
}

/*f axi_master_clock_fn */
static t_sl_error_level
axi_master_clock_fn( void *handle )
{
    c_axi_master *mod;
    mod = (c_axi_master *)handle;
    return mod->clock();
}

/*f axi_master_message  */
static t_sl_error_level
axi_master_message( void *handle, void *arg )
{
    c_axi_master *mod;
    mod = (c_axi_master *)handle;
    return mod->message((t_se_message *)arg );
}

/*f axi_master_preclock_posedge_clk_fn */
static t_sl_error_level
axi_master_preclock_posedge_clk_fn( void *handle )
{
    c_axi_master *mod;
    mod = (c_axi_master *)handle;
    mod->preclock();
    return error_level_okay;
}

/*a Constructors and destructors for axi_master */
/*f exec_file_instantiate_callback
 */
static void exec_file_instantiate_callback( void *handle, struct t_sl_exec_file_data *file_data )
{
    c_axi_master *axim = (c_axi_master *)handle;
    axim->add_exec_file_enhancements();
}

/*f c_axi_master::c_axi_master */
/**
 * Constructor for module 'axi_master' class
 *
 * Registers simulation engine functions
 *
 * Allocates shared memory (if possible)
 *
 * Registers inputs and outputs
 * 
 * Clears inputs
 */
c_axi_master::c_axi_master( class c_engine *eng, void *eng_handle )
{
    engine = eng;
    engine_handle = eng_handle;

    engine->register_delete_function( engine_handle, (void *)this, axi_master_delete_fn );
    engine->register_reset_function( engine_handle, (void *)this, axi_master_reset_fn );
    engine->register_message_function( engine_handle, (void *)this, axi_master_message );

    verbose       = engine->get_option_int( engine_handle, "verbose", 0 );
    address_width = engine->get_option_int( engine_handle, "address_width", 32 );
    data_width    = engine->get_option_int( engine_handle, "data_width", 32 ); // 32-bit or 64-bit
    id_width      = engine->get_option_int( engine_handle, "id_width", 12 ); // awid, 
    len_width     = engine->get_option_int( engine_handle, "len_width", 4 ); // awlen, arlen

    int max_wreq  = engine->get_option_int( engine_handle, "max_wr_req", 4 );
    int max_rreq  = engine->get_option_int( engine_handle, "max_rreq", 4 );
    int max_wdata = engine->get_option_int( engine_handle, "max_wdata", 4 );
    int max_wresp = engine->get_option_int( engine_handle, "max_wresp", 4 );
    int max_rresp = engine->get_option_int( engine_handle, "max_rresp", 4 );

    has_reset = 0;

    wreq_fifo  = new c_axi_queue<t_axi_request>(max_wreq);
    rreq_fifo  = new c_axi_queue<t_axi_request>(max_rreq);
    wdata_fifo = new c_axi_queue<t_axi_write_data>(max_wdata);
    wresp_fifo = new c_axi_queue<t_axi_write_response>(max_wresp);
    rresp_fifo = new c_axi_queue<t_axi_read_response>(max_rresp);

    memset(&inputs, 0, sizeof(inputs));

    engine->register_prepreclock_fn( engine_handle, (void *)this, axi_master_prepreclock_fn );
    engine->register_preclock_fns( engine_handle, (void *)this, "aclk", axi_master_preclock_posedge_clk_fn, (t_engine_callback_fn) NULL );
    engine->register_clock_fn( engine_handle, (void *)this, "aclk", engine_sim_function_type_posedge_clock, axi_master_clock_fn );

#define REGISTER_OUTPUT(s,w) \
    engine->register_output_signal(engine_handle, #s, w, &outputs.s); \
    engine->register_output_generated_on_clock(engine_handle, #s, "aclk", 1 );
#define REGISTER_INPUT(s,w) \
    engine->register_input_signal(engine_handle, #s, w, &inputs.s); \
    engine->register_input_used_on_clock(engine_handle, #s, "aclk", 1 );

    REGISTER_INPUT(areset_n,1);
    REGISTER_INPUT(awready,1);
    REGISTER_OUTPUT(aw__valid,1);
    REGISTER_OUTPUT(aw__id,id_width);
    REGISTER_OUTPUT(aw__addr,address_width);
    REGISTER_OUTPUT(aw__len,len_width);
    REGISTER_OUTPUT(aw__size,3);
    REGISTER_OUTPUT(aw__burst,2);
    REGISTER_OUTPUT(aw__lock,2);  // 2 in axi3
    REGISTER_OUTPUT(aw__cache,4); // slightly different used between axi3 and axi4
    REGISTER_OUTPUT(aw__prot,3); //
    REGISTER_OUTPUT(aw__qos,4); // axi4 only, optional
    REGISTER_OUTPUT(aw__region,4); // axi4 only, optional
    REGISTER_OUTPUT(aw__user,4); // axi4 only, don't use

    REGISTER_INPUT(wready,1);
    REGISTER_OUTPUT(w__valid,1);
    REGISTER_OUTPUT(w__id,id_width);
    REGISTER_OUTPUT(w__data,data_width);
    REGISTER_OUTPUT(w__strb,data_width/8);
    REGISTER_OUTPUT(w__last,1);
    REGISTER_OUTPUT(w__user,4);

    REGISTER_INPUT(b__valid,1);
    REGISTER_INPUT(b__id,id_width);
    REGISTER_INPUT(b__resp,2);
    REGISTER_INPUT(b__user,4);
    REGISTER_OUTPUT(bready,1);

    REGISTER_INPUT(arready,1);
    REGISTER_OUTPUT(ar__valid,1);
    REGISTER_OUTPUT(ar__id,id_width);
    REGISTER_OUTPUT(ar__addr,address_width);
    REGISTER_OUTPUT(ar__len,len_width);
    REGISTER_OUTPUT(ar__size,3);
    REGISTER_OUTPUT(ar__burst,2);
    REGISTER_OUTPUT(ar__lock,2);  // 2 in axi3
    REGISTER_OUTPUT(ar__cache,4); // slightly different used between axi3 and axi4
    REGISTER_OUTPUT(ar__prot,3); //
    REGISTER_OUTPUT(ar__qos,4); // axi4 only, optional
    REGISTER_OUTPUT(ar__region,4); // axi4 only, optional
    REGISTER_OUTPUT(ar__user,4); // axi4 only, don't use

    REGISTER_INPUT(r__valid,1);
    REGISTER_INPUT(r__id,id_width);
    REGISTER_INPUT(r__data,data_width);
    REGISTER_INPUT(r__resp,2);
    REGISTER_INPUT(r__last,1);
    REGISTER_INPUT(r__user,4);
    REGISTER_OUTPUT(rready,1);

    exec_file_data = NULL;
    PyObject *obj = (PyObject *)(engine->get_option_object( engine_handle, "object" ));

    if (obj)
    {
        sl_exec_file_allocate_from_python_object( engine->error, engine->message, exec_file_instantiate_callback, (void *)this, "exec_file", obj, &exec_file_data, "AXI master", 1 );
    }

}

/*f c_axi_master::~c_axi_master */
/**
 * Standard destructor for axi_master module class
 */
c_axi_master::~c_axi_master()
{
    delete_instance();
}

/*f c_axi_master::delete_instance */
/**
 * Standard destructor for axi_master module class
 */
t_sl_error_level c_axi_master::delete_instance( void )
{
    if (exec_file_data )
    {
        sl_exec_file_free( exec_file_data );
        exec_file_data = NULL;
    }
    return error_level_okay;
}

/*f c_axi_master::message */
/**
 * Handle a message sent to the module in the simulation environment
 *
 * This is currently a hack to just save the frame buffer as a PNG
 * when invoked with any message.
 *
 */
t_sl_error_level c_axi_master::message( t_se_message *message )
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

/*f c_axi_master::add_exec_file_enhancements
 */
static t_sl_exec_file_method_fn ef_req_enqueue_read;
static t_sl_exec_file_method_fn ef_req_enqueue_write;
static t_sl_exec_file_method_fn ef_write_data_enqueue;
static t_sl_exec_file_method_fn ef_write_response_dequeue;
static t_sl_exec_file_method_fn ef_write_response_empty;
static t_sl_exec_file_method_fn ef_read_response_dequeue;
static t_sl_exec_file_method_fn ef_read_response_empty;

/*f ef_set
 */
static t_sl_error_level ef_req_enqueue_write(t_sl_exec_file_cmd_cb *cmd_cb, void *obj, t_sl_exec_file_object_desc *object_desc, t_sl_exec_file_method *method)
{
    WHERE_I_AM;
    c_axi_master *axim = (c_axi_master *)ef_owner_of_objf(object_desc);
    t_axi_request *axi_req = ef_axi_request_of_objf(object_desc);
    t_sl_uint64 delay = sl_exec_file_eval_fn_get_argument_integer( cmd_cb->file_data, cmd_cb->args, 0 );
    return sl_exec_file_eval_fn_set_result(cmd_cb->file_data, (t_sl_uint64)(!!axim->wreq_fifo->enqueue(axi_req, delay)))?error_level_okay:error_level_fatal;
}
static t_sl_error_level ef_req_enqueue_read(t_sl_exec_file_cmd_cb *cmd_cb, void *obj, t_sl_exec_file_object_desc *object_desc, t_sl_exec_file_method *method)
{
    WHERE_I_AM;
    c_axi_master *axim = (c_axi_master *)ef_owner_of_objf(object_desc);
    t_axi_request *axi_req = ef_axi_request_of_objf(object_desc);
    t_sl_uint64 delay = sl_exec_file_eval_fn_get_argument_integer( cmd_cb->file_data, cmd_cb->args, 0 );
    return sl_exec_file_eval_fn_set_result(cmd_cb->file_data, (t_sl_uint64)(!!axim->rreq_fifo->enqueue(axi_req, delay)))?error_level_okay:error_level_fatal;
}
static t_sl_error_level ef_write_data_enqueue(t_sl_exec_file_cmd_cb *cmd_cb, void *obj, t_sl_exec_file_object_desc *object_desc, t_sl_exec_file_method *method)
{
    WHERE_I_AM;
    c_axi_master *axim = (c_axi_master *)ef_owner_of_objf(object_desc);
    t_axi_write_data *axi_wd = ef_axi_write_data_of_objf(object_desc);
    t_sl_uint64 delay = sl_exec_file_eval_fn_get_argument_integer( cmd_cb->file_data, cmd_cb->args, 0 );
    return sl_exec_file_eval_fn_set_result(cmd_cb->file_data, (t_sl_uint64)(!!axim->wdata_fifo->enqueue(axi_wd, delay)))?error_level_okay:error_level_fatal;
}
static t_sl_error_level ef_write_response_dequeue(t_sl_exec_file_cmd_cb *cmd_cb, void *obj, t_sl_exec_file_object_desc *object_desc, t_sl_exec_file_method *method)
{
    WHERE_I_AM;
    c_axi_master *axim = (c_axi_master *)ef_owner_of_objf(object_desc);
    t_axi_write_response *axi_wr = ef_axi_write_response_of_objf(object_desc);
    return sl_exec_file_eval_fn_set_result(cmd_cb->file_data, (t_sl_uint64)(!!axim->wresp_fifo->dequeue(axi_wr, NULL)))?error_level_okay:error_level_fatal;
}
static t_sl_error_level ef_write_response_empty(t_sl_exec_file_cmd_cb *cmd_cb, void *obj, t_sl_exec_file_object_desc *object_desc, t_sl_exec_file_method *method)
{
    WHERE_I_AM;
    c_axi_master *axim = (c_axi_master *)ef_owner_of_objf(object_desc);
    return sl_exec_file_eval_fn_set_result(cmd_cb->file_data, (t_sl_uint64)axim->wresp_fifo->is_empty())?error_level_okay:error_level_fatal;
}
static t_sl_error_level ef_read_response_dequeue(t_sl_exec_file_cmd_cb *cmd_cb, void *obj, t_sl_exec_file_object_desc *object_desc, t_sl_exec_file_method *method)
{
    WHERE_I_AM;
    c_axi_master *axim = (c_axi_master *)ef_owner_of_objf(object_desc);
    t_axi_read_response *axi_rr = ef_axi_read_response_of_objf(object_desc);
    return sl_exec_file_eval_fn_set_result(cmd_cb->file_data, (t_sl_uint64)(!!axim->rresp_fifo->dequeue(axi_rr, NULL)))?error_level_okay:error_level_fatal;
}
static t_sl_error_level ef_read_response_empty(t_sl_exec_file_cmd_cb *cmd_cb, void *obj, t_sl_exec_file_object_desc *object_desc, t_sl_exec_file_method *method)
{
    WHERE_I_AM;
    c_axi_master *axim = (c_axi_master *)ef_owner_of_objf(object_desc);
    return sl_exec_file_eval_fn_set_result(cmd_cb->file_data, (t_sl_uint64)axim->rresp_fifo->is_empty())?error_level_okay:error_level_fatal;
}

static t_sl_exec_file_method axi_req_obj_additional_methods[] =
{
    {"enqueue_read", 'i',  1, "i",  "enqueue_read(<delay>)", ef_req_enqueue_read, NULL },
    {"enqueue_write", 'i',  1, "i",  "enqueue_write(<delay>)", ef_req_enqueue_write, NULL },
    SL_EXEC_FILE_METHOD_NONE
};
// enqueue
static t_sl_exec_file_method axi_write_data_obj_additional_methods[] =
{
    {"enqueue", 'i',  1, "i",  "enqueue(<delay>)", ef_write_data_enqueue, NULL },
    SL_EXEC_FILE_METHOD_NONE
};
// dequeue
static t_sl_exec_file_method axi_write_response_obj_additional_methods[] =
{
    {"empty", 'i',  0, "i",  "empty()", ef_write_response_empty, NULL },
    {"dequeue", 'i',  0, "i",  "dequeue()", ef_write_response_dequeue, NULL },
    SL_EXEC_FILE_METHOD_NONE
};
// dequeue
static t_sl_exec_file_method axi_read_response_obj_additional_methods[] =
{
    {"empty", 'i',  0, "i",  "empty()", ef_read_response_empty, NULL },
    {"dequeue", 'i',  0, "i",  "dequeue()", ef_read_response_dequeue, NULL },
    SL_EXEC_FILE_METHOD_NONE
};
static int ef_fn_axi_request(void *handle, t_sl_exec_file_data *file_data, t_sl_exec_file_value *args)
{
    const char *name = sl_exec_file_eval_fn_get_argument_string(file_data, args, 0);
    t_axi_request *axi_req = (t_axi_request *)malloc(sizeof(t_axi_request));
    void *ef_object = ef_axi_req_create(file_data, name, handle, axi_req, axi_req_obj_additional_methods );
    return (ef_object==NULL) ? error_level_serious : error_level_okay;
}
static int ef_fn_axi_write_data(void *handle, t_sl_exec_file_data *file_data, t_sl_exec_file_value *args)
{
    const char *name = sl_exec_file_eval_fn_get_argument_string(file_data, args, 0);
    t_axi_write_data *axi_req = (t_axi_write_data *)malloc(sizeof(t_axi_write_data));
    void *ef_object = ef_axi_write_data_create(file_data, name, handle, axi_req, axi_write_data_obj_additional_methods );
    return (ef_object==NULL) ? error_level_serious : error_level_okay;
}
static int ef_fn_axi_write_response(void *handle, t_sl_exec_file_data *file_data, t_sl_exec_file_value *args)
{
    const char *name = sl_exec_file_eval_fn_get_argument_string(file_data, args, 0);
    t_axi_write_response *axi_req = (t_axi_write_response *)malloc(sizeof(t_axi_write_response));
    void *ef_object = ef_axi_write_response_create(file_data, name, handle, axi_req, axi_write_response_obj_additional_methods );
    return (ef_object==NULL) ? error_level_serious : error_level_okay;
}
static int ef_fn_axi_read_response(void *handle, t_sl_exec_file_data *file_data, t_sl_exec_file_value *args)
{
    const char *name = sl_exec_file_eval_fn_get_argument_string(file_data, args, 0);
    t_axi_read_response *axi_req = (t_axi_read_response *)malloc(sizeof(t_axi_read_response));
    void *ef_object = ef_axi_read_response_create(file_data, name, handle, axi_req, axi_read_response_obj_additional_methods );
    return (ef_object==NULL) ? error_level_serious : error_level_okay;
}

static t_sl_exec_file_fn ef_fns[] =
{
    {0, "axi_request", 'i', "s", "axi_request(<name>) - create an axi request instance called 'name'", ef_fn_axi_request },
    {0, "axi_write_data", 'i', "s", "axi_write_data(<name>) - create an axi write data instance called 'name'", ef_fn_axi_write_data },
    {0, "axi_write_response", 'i', "s", "axi_write_response(<name>) - create an axi write response instance called 'name'", ef_fn_axi_write_response },
    {0, "axi_read_response", 'i', "s", "axi_read_response(<name>) - create an axi read response instance called 'name'", ef_fn_axi_read_response },
    SL_EXEC_FILE_FN_NONE
};
void c_axi_master::add_exec_file_enhancements(void)
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

/*a Class preclock/clock methods for axi_master
*/
/*f c_axi_master::capture_inputs */
/**
 * Capture inputs - happens prior to relevant clock edges
 *
 */
t_sl_error_level
c_axi_master::capture_inputs( void )
{
    awready = inputs.awready[0];
    arready = inputs.arready[0];
    wready  = inputs.wready[0];
    write_response.valid = inputs.b__valid[0];
    write_response.id    = inputs.b__id[0];
    write_response.resp  = inputs.b__resp[0];
    write_response.user  = 0;
    if (inputs.b__user) {write_response.user  = inputs.b__user[0];}

    read_response.valid = inputs.r__valid[0];
    read_response.id    = inputs.r__id[0];
    read_response.data  = inputs.r__data[0];
    read_response.resp  = inputs.r__resp[0];
    read_response.last  = inputs.r__last[0];
    read_response.user  = 0;
    if (inputs.r__user) {read_response.user  = inputs.r__user[0];}

    return error_level_okay;
}

/*f c_axi_master::prepreclock */
/**
 * Prepreclock call, invoked on every clock edge before any preclock or
 * clock functions, permitting clearing of appropriate guards
 */
t_sl_error_level
c_axi_master::prepreclock( void )
{
    inputs_captured=0;
    clocks_to_call=0;
    return error_level_okay;
}

/*f c_axi_master::preclock */
/**
 * Preclock call, invoked after a prepreclock if the clock is going to
 * fire; inputs must be captured at this point (as they may be invalid
 * at 'clock').
 */
t_sl_error_level
c_axi_master::preclock(void)
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

/*f c_axi_master::clock */
/**
 * Clock call, invoked after all preclock calls. Handle any clock
 * edges indicated required by 'preclock' calls.
 */
t_sl_error_level
c_axi_master::clock( void )
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

    /*b Handle write requests
     */
    if (outputs.aw__valid && awready) {
        outputs.aw__valid = 0;
        outputs.aw__id     = 0;
        outputs.aw__addr   = 0;
        outputs.aw__len    = 0;
        outputs.aw__size   = 0;
        outputs.aw__burst  = 0;
        outputs.aw__lock   = 0;
        outputs.aw__cache  = 0;
        outputs.aw__prot   = 0;
        outputs.aw__qos    = 0;
        outputs.aw__region = 0;
        outputs.aw__user   = 0;
    }
    if (!outputs.aw__valid && !wreq_fifo->is_empty()) {
        t_axi_request axi_req;
        int delay;
        wreq_fifo->dequeue(&axi_req, &delay);
        outputs.aw__valid = 1;
        outputs.aw__id     = axi_req.id;
        outputs.aw__addr   = axi_req.addr;
        outputs.aw__len    = axi_req.len;
        outputs.aw__size   = axi_req.size;
        outputs.aw__burst  = axi_req.burst;
        outputs.aw__lock   = axi_req.lock;
        outputs.aw__cache  = axi_req.cache;
        outputs.aw__prot   = axi_req.prot;
        outputs.aw__qos    = axi_req.qos;
        outputs.aw__region = axi_req.region;
        outputs.aw__user   = axi_req.user;
    }

    /*b Handle read requests
     */
    if (outputs.ar__valid && arready) {
        outputs.ar__valid = 0;
        outputs.ar__id     = 0;
        outputs.ar__addr   = 0;
        outputs.ar__len    = 0;
        outputs.ar__size   = 0;
        outputs.ar__burst  = 0;
        outputs.ar__lock   = 0;
        outputs.ar__cache  = 0;
        outputs.ar__prot   = 0;
        outputs.ar__qos    = 0;
        outputs.ar__region = 0;
        outputs.ar__user   = 0;
    }
    if (!outputs.ar__valid && !rreq_fifo->is_empty()) {
        t_axi_request axi_req;
        int delay;
        rreq_fifo->dequeue(&axi_req, &delay);
        outputs.ar__valid = 1;
        outputs.ar__id     = axi_req.id;
        outputs.ar__addr   = axi_req.addr;
        outputs.ar__len    = axi_req.len;
        outputs.ar__size   = axi_req.size;
        outputs.ar__burst  = axi_req.burst;
        outputs.ar__lock   = axi_req.lock;
        outputs.ar__cache  = axi_req.cache;
        outputs.ar__prot   = axi_req.prot;
        outputs.ar__qos    = axi_req.qos;
        outputs.ar__region = axi_req.region;
        outputs.ar__user   = axi_req.user;
    }

    /*b Handle write data
     */
    if (outputs.w__valid && wready) {
        outputs.w__valid = 0;
        outputs.w__id    = 0;
        outputs.w__data  = 0;
        outputs.w__strb  = 0;
        outputs.w__last  = 0;
        outputs.w__user  = 0;
    }
    if (!outputs.w__valid && !wdata_fifo->is_empty()) {
        t_axi_write_data axi_wdata;
        int delay;
        wdata_fifo->dequeue(&axi_wdata, &delay);
        outputs.w__valid = 1;
        outputs.w__id    = axi_wdata.id;
        outputs.w__data  = axi_wdata.data;
        outputs.w__strb  = axi_wdata.strb;
        outputs.w__last  = axi_wdata.last;
        outputs.w__user  = axi_wdata.user;
    }

    /*b Handle write response
     */
    if (outputs.bready && write_response.valid) {
        wresp_fifo->enqueue(&write_response, 0);
    }
    outputs.bready = !wresp_fifo->is_full();

    /*b Handle read response
     */
    if (outputs.bready && read_response.valid) {
        rresp_fifo->enqueue(&read_response, 0);
    }
    outputs.rready = !rresp_fifo->is_full();

    /*b All done
     */
    return error_level_okay;
}

/*f c_axi_master::reset
*/
t_sl_error_level c_axi_master::reset( int pass )
{
    awready = 0;
    arready = 0;
    wready  = 0;
    memset(&write_response, 0, sizeof(write_response));
    memset(&read_response, 0, sizeof(read_response));
    memset(&outputs, 0, sizeof(outputs));
    return error_level_okay;
}
/*a Initialization functions */
/*f axi_master__init */
/**
 * Initialize the module with the simulation engine
 */
extern void
axi_master__init( void )
{
    se_external_module_register( 1, "axi_master", axi_master_instance_fn, "cdl_model" );
}

/*a Scripting support code
*/
/*f initaxi_master */
/**
 * External function invoked by the simulation engine when the library
 * is loaded, to register the module
 */
extern "C" void
initaxi_master( void )
{
    axi_master__init( );
    scripting_init_module( "axi_master" );
}

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
