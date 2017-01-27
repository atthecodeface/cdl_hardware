/** Copyright (C) 2016-2017,  Gavin J Stark.  All rights reserved.
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
 * @file   bbc_floppy.cpp
 * @brief  BBC floppy class methods
 *
 * Code for the BBC floppy CDL module, originally used as a C model to
 * bring the floppy disk controller up. No longer used.
 */

/*a Includes */
#include "be_model_includes.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "bbc_shm.h"
#include "bbc_floppy.h"
#include "bbc_floppy_disk.h"

/*a Defines
 */
#define struct_offset( ptr, a ) (((char *)&(ptr->a))-(char *)ptr)
#define struct_resolve( t, ptr, a ) ((t)(((char *)(ptr))+(a)))
#define WHERE_I_AM_VERBOSE_ENGINE {fprintf(stderr,"%s,%s,%s,%p,%d\n",__FILE__,engine->get_instance_name(engine_handle),__func__,this,__LINE__ );}
#define WHERE_I_AM_VERBOSE {fprintf(stderr,"%s:%s:%p:%d\n",__FILE__,__func__,this,__LINE__ );}
#define WHERE_I_AM {}

/*a Types for bbc_floppy
*/
/*t t_bbc_floppy_inputs
*/
typedef struct t_bbc_floppy_inputs {
    t_sl_uint64 *floppy_op__step_out;
    t_sl_uint64 *floppy_op__step_in;
    t_sl_uint64 *floppy_op__next_id;
    t_sl_uint64 *floppy_op__read_data_enable;
    t_sl_uint64 *floppy_op__write_data_enable;
    t_sl_uint64 *floppy_op__write_data;
    t_sl_uint64 *floppy_op__write_sector_id_enable;
    t_sl_uint64 *floppy_op__sector_id__track;
    t_sl_uint64 *floppy_op__sector_id__head;
    t_sl_uint64 *floppy_op__sector_id__sector_number;
    t_sl_uint64 *floppy_op__sector_id__sector_length;
    t_sl_uint64 *floppy_op__sector_id__bad_crc;
    t_sl_uint64 *floppy_op__sector_id__bad_data_crc;
    t_sl_uint64 *floppy_op__sector_id__deleted_data;

} t_bbc_floppy_inputs;

/*t t_bbc_floppy_outputs
*/
typedef struct t_bbc_floppy_outputs {
    t_bbc_floppy_response floppy_response;
} t_bbc_floppy_outputs;

/*t t_bbc_floppy
*/
typedef struct {
    int clock_enable;
} t_bbc_floppy;

/*t t_floppy_state */
typedef struct {
    int selected_drive;
    c_bbc_floppy_disk *disks[4];
} t_floppy_state;

/*t c_bbc_floppy
*/
class c_bbc_floppy
{
public:
    c_bbc_floppy( class c_engine *eng, void *eng_handle );
    ~c_bbc_floppy();
    t_sl_error_level delete_instance( void );
    t_sl_error_level capture_inputs( void );
    t_sl_error_level prepreclock( void );
    t_sl_error_level preclock(void);
    t_sl_error_level clock( void );
    t_sl_error_level message( t_se_message *message );
    c_engine *engine;
    int clocks_to_call;
    void *engine_handle;
    int inputs_captured;
    t_bbc_floppy_outputs outputs;
    t_bbc_floppy_inputs inputs;
    t_bbc_floppy_op input_floppy_op;
    t_floppy_state floppy;
    int cycles;
    int verbose;
    int toggle;
    int last_step_out;
    int last_step_in;
    int last_next_id;
    int last_read_data_enable;
};

/*a Static wrapper functions for bbc_floppy
*/
/*f bbc_floppy_instance_fn
*/
static t_sl_error_level bbc_floppy_instance_fn( c_engine *engine, void *engine_handle )
{
    c_bbc_floppy *mod;
    mod = new c_bbc_floppy( engine, engine_handle );
    if (!mod)
        return error_level_fatal;
    return error_level_okay;
}

/*f bbc_floppy_delete_fn - simple callback wrapper for the main method
*/
static t_sl_error_level bbc_floppy_delete_fn( void *handle )
{
    c_bbc_floppy *mod;
    t_sl_error_level result;
    mod = (c_bbc_floppy *)handle;
    result = mod->delete_instance();
    delete( mod );
    return result;
}

/*f bbc_floppy_prepreclock_fn
*/
static t_sl_error_level bbc_floppy_prepreclock_fn( void *handle )
{
    c_bbc_floppy *mod;
    mod = (c_bbc_floppy *)handle;
    return mod->prepreclock();
}

/*f bbc_floppy_clock_fn
*/
static t_sl_error_level bbc_floppy_clock_fn( void *handle )
{
    c_bbc_floppy *mod;
    mod = (c_bbc_floppy *)handle;
    return mod->clock();
}

/*f bbc_floppy_message
 */
static t_sl_error_level bbc_floppy_message( void *handle, void *arg )
{
    c_bbc_floppy *mod;
    mod = (c_bbc_floppy *)handle;
    return mod->message((t_se_message *)arg );
}

/*f bbc_floppy_preclock_posedge_clk_fn
*/
static t_sl_error_level bbc_floppy_preclock_posedge_clk_fn( void *handle )
{
    c_bbc_floppy *mod;
    mod = (c_bbc_floppy *)handle;
    mod->preclock();
    return error_level_okay;
}

/*a Constructors and destructors for bbc_floppy
*/
/*f c_bbc_floppy::c_bbc_floppy
*/
c_bbc_floppy::c_bbc_floppy( class c_engine *eng, void *eng_handle )
{
    engine = eng;
    engine_handle = eng_handle;

    engine->register_delete_function( engine_handle, (void *)this, bbc_floppy_delete_fn );
    engine->register_message_function( engine_handle, (void *)this, bbc_floppy_message );

    //const char *shm_lock_filename="/tmp/bbc_shm.lock";
    //const int shm_key = 0xbbc;
    //shm = new c_bbc_shm(shm_lock_filename, shm_key, fbk.data_size);
    static const char *initial_disk_filename = "disks/ELITEBBC.SDD";
    //static const char *initial_disk_filename = "disks/Hubert.ssd";
    //static const char *initial_disk_filename = "disks/munchyman.ssd";
    floppy.selected_drive = 0;
    floppy.disks[0] = new c_bbc_floppy_disk();
    floppy.disks[1] = NULL;
    floppy.disks[2] = NULL;
    floppy.disks[3] = NULL;
    floppy.disks[0]->load_disk(initial_disk_filename, -1, 1);
    
    memset(&inputs, 0, sizeof(inputs));
    memset(&input_floppy_op, 0, sizeof(input_floppy_op));

    engine->register_prepreclock_fn( engine_handle, (void *)this, bbc_floppy_prepreclock_fn );
    engine->register_preclock_fns( engine_handle, (void *)this, "clk", bbc_floppy_preclock_posedge_clk_fn, (t_engine_callback_fn) NULL );
    engine->register_clock_fn( engine_handle, (void *)this, "clk", engine_sim_function_type_posedge_clock, bbc_floppy_clock_fn );

#define REGISTER_OUTPUT(s,w) \
    engine->register_output_signal(engine_handle, #s, w, &outputs.s); \
    engine->register_output_generated_on_clock(engine_handle, #s, "clk", 1 );
#define REGISTER_OUTPUT2(s1,s2,w)                                    \
    engine->register_output_signal(engine_handle, #s1 "__" #s2, w, &outputs.s1.s2); \
    engine->register_output_generated_on_clock(engine_handle, #s1 "__" #s2, "clk", 1 );
#define REGISTER_OUTPUT3(s1,s2,s3,w)                                    \
    engine->register_output_signal(engine_handle, #s1 "__" #s2 "__" #s3, w, &outputs.s1.s2.s3); \
    engine->register_output_generated_on_clock(engine_handle, #s1 "__" #s2 "__" #s3, "clk", 1 );
#define REGISTER_INPUT(s,w) \
    engine->register_input_signal(engine_handle, #s, w, &inputs.s); \
    engine->register_input_used_on_clock(engine_handle, #s, "clk", 1 );

    REGISTER_INPUT(floppy_op__step_out,1);
    REGISTER_INPUT(floppy_op__step_in,1);
    REGISTER_INPUT(floppy_op__next_id,1);
    REGISTER_INPUT(floppy_op__read_data_enable,1);
    REGISTER_INPUT(floppy_op__write_data_enable,1);
    REGISTER_INPUT(floppy_op__write_data,32);
    REGISTER_INPUT(floppy_op__write_sector_id_enable,1);
    REGISTER_INPUT(floppy_op__sector_id__track,7);
    REGISTER_INPUT(floppy_op__sector_id__head,1);
    REGISTER_INPUT(floppy_op__sector_id__sector_number,6);
    REGISTER_INPUT(floppy_op__sector_id__sector_length,2);
    REGISTER_INPUT(floppy_op__sector_id__bad_crc,1);
    REGISTER_INPUT(floppy_op__sector_id__bad_data_crc,1);
    REGISTER_INPUT(floppy_op__sector_id__deleted_data,1);

    REGISTER_OUTPUT2(floppy_response,disk_ready,1);
    REGISTER_OUTPUT2(floppy_response,track_zero,1);
    REGISTER_OUTPUT2(floppy_response,index,1);
    REGISTER_OUTPUT2(floppy_response,write_protect,1);
    REGISTER_OUTPUT2(floppy_response,read_data_valid,1);
    REGISTER_OUTPUT2(floppy_response,sector_id_valid,1);
    REGISTER_OUTPUT2(floppy_response,read_data,32);
    REGISTER_OUTPUT3(floppy_response,sector_id,track,7);
    REGISTER_OUTPUT3(floppy_response,sector_id,head,1);
    REGISTER_OUTPUT3(floppy_response,sector_id,sector_number,6);
    REGISTER_OUTPUT3(floppy_response,sector_id,sector_length,2);
    REGISTER_OUTPUT3(floppy_response,sector_id,bad_crc,1);
    REGISTER_OUTPUT3(floppy_response,sector_id,bad_data_crc,1);
    REGISTER_OUTPUT3(floppy_response,sector_id,deleted_data,1);

    outputs.floppy_response.sector_id_valid = 0;
    outputs.floppy_response.sector_id.track  =0;
    outputs.floppy_response.sector_id.head = 0;
    outputs.floppy_response.sector_id.sector_number = 0;
    outputs.floppy_response.sector_id.sector_length = 0;
    outputs.floppy_response.sector_id.bad_crc = 0;
    outputs.floppy_response.sector_id.bad_data_crc = 0;
    outputs.floppy_response.sector_id.deleted_data = 0;
    outputs.floppy_response.index = 0;
    outputs.floppy_response.read_data_valid = 0;
    outputs.floppy_response.read_data = 0;
    outputs.floppy_response.track_zero = 0;
    outputs.floppy_response.write_protect = 0;
    outputs.floppy_response.disk_ready = 0;
}

/*f c_bbc_floppy::~c_bbc_floppy
*/
c_bbc_floppy::~c_bbc_floppy()
{
    delete_instance();
}

/*f c_bbc_floppy::delete_instance
*/
t_sl_error_level c_bbc_floppy::delete_instance( void )
{
    return error_level_okay;
}

/*f c_bbc_floppy::message
*/
t_sl_error_level c_bbc_floppy::message( t_se_message *message )
{
    fprintf(stderr,"Got message %d\n",message->reason);
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

/*a Class preclock/clock methods for bbc_floppy
*/
/*f c_bbc_floppy::capture_inputs
*/
t_sl_error_level c_bbc_floppy::capture_inputs( void )
{
    input_floppy_op.step_out = inputs.floppy_op__step_out[0];
    input_floppy_op.step_in  = inputs.floppy_op__step_in[0];
    input_floppy_op.next_id  = inputs.floppy_op__next_id[0];
    input_floppy_op.read_data_enable  = inputs.floppy_op__read_data_enable[0];
    input_floppy_op.write_data_enable  = inputs.floppy_op__write_data_enable[0];
    input_floppy_op.write_data  = inputs.floppy_op__write_data[0];
    input_floppy_op.write_sector_id_enable  = inputs.floppy_op__write_sector_id_enable[0];
    input_floppy_op.sector_id.track  = inputs.floppy_op__sector_id__track[0];
    input_floppy_op.sector_id.head   = inputs.floppy_op__sector_id__head[0];
    input_floppy_op.sector_id.sector_number   = inputs.floppy_op__sector_id__sector_number[0];
    input_floppy_op.sector_id.sector_length   = inputs.floppy_op__sector_id__sector_length[0];
    input_floppy_op.sector_id.bad_crc   = inputs.floppy_op__sector_id__bad_crc[0];
    input_floppy_op.sector_id.bad_data_crc   = inputs.floppy_op__sector_id__bad_data_crc[0];
    input_floppy_op.sector_id.deleted_data   = inputs.floppy_op__sector_id__deleted_data[0];

    return error_level_okay;
}

/*f c_bbc_floppy::prepreclock
*/
t_sl_error_level c_bbc_floppy::prepreclock( void )
{
    WHERE_I_AM;
    inputs_captured=0;
    clocks_to_call=0;
    return error_level_okay;
}

/*f c_bbc_floppy::preclock
*/
t_sl_error_level c_bbc_floppy::preclock(void)
{
    WHERE_I_AM;
    if (!inputs_captured) { capture_inputs(); inputs_captured++; }
    clocks_to_call++;
    return error_level_okay;
}

/*f c_bbc_floppy::clock
*/
t_sl_error_level c_bbc_floppy::clock( void )
{
    c_bbc_floppy_disk *selected_disk = floppy.disks[0];
    WHERE_I_AM;
    if (clocks_to_call>0) {
        clocks_to_call=0;
        toggle = !toggle;
        if (!toggle) return error_level_okay;
        if (!selected_disk) {
            outputs.floppy_response.disk_ready = 0;
            return error_level_okay;
        }
        outputs.floppy_response.disk_ready = 1;
        outputs.floppy_response.write_protect = selected_disk->write_protected;

        if (input_floppy_op.step_out && !last_step_out) {
            selected_disk->step_track(-1);
        }
        if (input_floppy_op.step_in && !last_step_in) { // dont step out if invalid
            selected_disk->step_track(+1);
        }
        outputs.floppy_response.sector_id_valid = 0;
        if (input_floppy_op.next_id && !last_next_id) {
            selected_disk->next_sector();
            selected_disk->get_sector_id(-1,-1,&outputs.floppy_response.sector_id);
            outputs.floppy_response.sector_id_valid = 1;
        }
        outputs.floppy_response.read_data_valid = 0;
        if (input_floppy_op.read_data_enable && !last_read_data_enable) {
            selected_disk->read_data(-1, -1, (unsigned char *)(&outputs.floppy_response.read_data), -1, 4);
            outputs.floppy_response.read_data_valid = 1;
        }
        last_step_in  = input_floppy_op.step_in;
        last_step_out = input_floppy_op.step_out;
        last_next_id  = input_floppy_op.next_id;
        last_read_data_enable  = input_floppy_op.read_data_enable;
        outputs.floppy_response.index      = (selected_disk->current_sector==0);
        outputs.floppy_response.track_zero = (selected_disk->current_track==0);
    }
    return error_level_okay;
}

/*a Initialization functions
*/
/*f bbc_floppy__init
*/
extern void bbc_floppy__init( void )
{
    se_external_module_register( 1, "bbc_floppy", bbc_floppy_instance_fn, "cdl_model" );
}

/*a Scripting support code
*/
/*f initbbc_floppy
*/
extern "C" void initbbc_floppy( void )
{
    bbc_floppy__init( );
    scripting_init_module( "bbc_floppy" );
}
/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
