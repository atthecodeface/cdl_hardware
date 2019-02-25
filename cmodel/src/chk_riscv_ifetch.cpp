/** Copyright (C) 2019,  Gavin J Stark.  All rights reserved.
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
 * @file   chk_riscv_ifetch.cpp
 * @brief  BBC floppy class methods
 *
 * Code for the BBC floppy CDL module, originally used as a C model to
 * bring the floppy disk controller up. No longer used.
 */

/*a Includes */
#include "be_model_includes.h"
#include "sl_hier_mem.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*a Defines
 */
#define struct_offset( ptr, a ) (((char *)&(ptr->a))-(char *)ptr)
#define struct_resolve( t, ptr, a ) ((t)(((char *)(ptr))+(a)))
#define WHERE_I_AM_VERBOSE_ENGINE {fprintf(stderr,"%s,%s,%s,%p,%d\n",__FILE__,engine->get_instance_name(engine_handle),__func__,this,__LINE__ );}
#define WHERE_I_AM_VERBOSE {fprintf(stderr,"%s:%s:%p:%d\n",__FILE__,__func__,this,__LINE__ );}
#define WHERE_I_AM {}

/*a Types from the CDL */
/*t t_riscv_mode
 */
typedef enum {
    rv_mode_user       = 0, // matches the encoding in table 1.1 of v1.10 privilege spec
    rv_mode_supervisor = 1, // matches the encoding in table 1.1 of v1.10 privilege spec
    rv_mode_machine    = 3, // matches the encoding in table 1.1 of v1.10 privilege spec
    rv_mode_debug      = 7, // all 1s so that it is a superset of machine mode
} t_riscv_mode;

/*t t_riscv_fetch_req_type
 *
 *
 *
 */
typedef enum {
    rv_fetch_none           = 0, // address is invalid - next non-none request MUST be nonsequential
    rv_fetch_nonsequential  = 1, // address is anything, and will be valid late in the cycle
    rv_fetch_sequential_32  = 2, // address=+4 from last cycle
    rv_fetch_repeat         = 3, // address will be same as last cycle
    rv_fetch_sequential_16  = 6, // address=+2 from last cycle
} t_riscv_fetch_req_type;


/*a Types for chk_riscv_ifetch
*/
/*t t_chk_riscv_ifetch_inputs
*/
typedef struct t_chk_riscv_ifetch_inputs {
    t_sl_uint64 *fetch_req__flush_pipeline;
    t_sl_uint64 *fetch_req__req_type;
    t_sl_uint64 *fetch_req__debug_fetch;
    t_sl_uint64 *fetch_req__address;
    t_sl_uint64 *fetch_req__mode;
    t_sl_uint64 *fetch_req__predicted_branch;
    t_sl_uint64 *fetch_req__pc_if_mispredicted;

    t_sl_uint64 *fetch_resp__valid;
    t_sl_uint64 *fetch_resp__debug;
    t_sl_uint64 *fetch_resp__data;
    t_sl_uint64 *fetch_resp__mode;
    t_sl_uint64 *fetch_resp__error;
    t_sl_uint64 *fetch_resp__tag;
} t_chk_riscv_ifetch_inputs;

/*t t_chk_riscv_ifetch_outputs
*/
typedef struct t_chk_riscv_ifetch_outputs {
    t_sl_uint64 error_detected;
    t_sl_uint64 cycle;
} t_chk_riscv_ifetch_outputs;

/*t t_chk_riscv_ifetch_input_state
*/
typedef struct {
    struct {
        t_sl_uint64 flush_pipeline;
        t_sl_uint64 req_type;
        t_sl_uint64 debug_fetch;
        t_sl_uint64 address;
        t_sl_uint64 mode;
        t_sl_uint64 predicted_branch;
        t_sl_uint64 pc_if_mispredicted;
    } fetch_req;
    struct {
        t_sl_uint64 valid;
        t_sl_uint64 debug;
        t_sl_uint64 data;
        t_sl_uint64 mode;
        t_sl_uint64 error;
        t_sl_uint64 tag;
    } fetch_resp;
} t_chk_riscv_ifetch_input_state;

/*t t_chk_riscv_ifetch_verify_state
*/
typedef struct {
    t_sl_hier_mem *hier_mem;
    t_riscv_fetch_req_type last_req_type;
    t_sl_uint64 address;
} t_chk_riscv_ifetch_verify_state;

/*t c_chk_riscv_ifetch
*/
class c_chk_riscv_ifetch
{
public:
    c_chk_riscv_ifetch( class c_engine *eng, void *eng_handle );
    ~c_chk_riscv_ifetch();
    t_sl_error_level delete_instance( void );
    t_sl_error_level capture_inputs( void );
    t_sl_error_level prepreclock( void );
    t_sl_error_level preclock(void);
    t_sl_error_level clock( void );
    t_sl_error_level message( t_se_message *message );
    void verify_reset(void);
    void verify_error(const char *format,...);
    void verify_fetch_request(void);
    void verify_fetch_response(void);
    int verify_create_memory(void);
    int verify_memory_check_and_set(t_sl_uint64 word_address, t_sl_uint64 data, t_sl_uint64 mask, t_sl_uint64 *old_data);
    c_engine *engine;
    int clocks_to_call;
    void *engine_handle;
    int inputs_captured;
    int connected_okay;
    t_chk_riscv_ifetch_outputs outputs;
    t_chk_riscv_ifetch_inputs inputs;
    t_chk_riscv_ifetch_input_state input;
    t_chk_riscv_ifetch_verify_state verify;
    int cycles;
    int verbose;
};

/*a Static wrapper functions for chk_riscv_ifetch
*/
/*f chk_riscv_ifetch_instance_fn
*/
static t_sl_error_level chk_riscv_ifetch_instance_fn( c_engine *engine, void *engine_handle )
{
    c_chk_riscv_ifetch *mod;
    mod = new c_chk_riscv_ifetch( engine, engine_handle );
    if (!mod)
        return error_level_fatal;
    return error_level_okay;
}

/*f chk_riscv_ifetch_delete_fn - simple callback wrapper for the main method
*/
static t_sl_error_level chk_riscv_ifetch_delete_fn( void *handle )
{
    c_chk_riscv_ifetch *mod;
    t_sl_error_level result;
    mod = (c_chk_riscv_ifetch *)handle;
    result = mod->delete_instance();
    delete( mod );
    return result;
}

/*f chk_riscv_ifetch_prepreclock_fn
*/
static t_sl_error_level chk_riscv_ifetch_prepreclock_fn( void *handle )
{
    c_chk_riscv_ifetch *mod;
    mod = (c_chk_riscv_ifetch *)handle;
    return mod->prepreclock();
}

/*f chk_riscv_ifetch_clock_fn
*/
static t_sl_error_level chk_riscv_ifetch_clock_fn( void *handle )
{
    c_chk_riscv_ifetch *mod;
    mod = (c_chk_riscv_ifetch *)handle;
    return mod->clock();
}

/*f chk_riscv_ifetch_message
 */
static t_sl_error_level chk_riscv_ifetch_message( void *handle, void *arg )
{
    c_chk_riscv_ifetch *mod;
    mod = (c_chk_riscv_ifetch *)handle;
    return mod->message((t_se_message *)arg );
}

/*f chk_riscv_ifetch_preclock_posedge_clk_fn
*/
static t_sl_error_level chk_riscv_ifetch_preclock_posedge_clk_fn( void *handle )
{
    c_chk_riscv_ifetch *mod;
    mod = (c_chk_riscv_ifetch *)handle;
    mod->preclock();
    return error_level_okay;
}

/*a Constructors and destructors for chk_riscv_ifetch
*/
/*f c_chk_riscv_ifetch::c_chk_riscv_ifetch
*/
c_chk_riscv_ifetch::c_chk_riscv_ifetch( class c_engine *eng, void *eng_handle )
{
    engine = eng;
    engine_handle = eng_handle;

    engine->register_delete_function( engine_handle, (void *)this, chk_riscv_ifetch_delete_fn );
    engine->register_message_function( engine_handle, (void *)this, chk_riscv_ifetch_message );

    memset(&inputs, 0, sizeof(inputs));
    memset(&input, 0, sizeof(input));
    memset(&verify, 0, sizeof(verify));
    connected_okay = 0;

    engine->register_prepreclock_fn( engine_handle, (void *)this, chk_riscv_ifetch_prepreclock_fn );
    engine->register_preclock_fns( engine_handle, (void *)this, "clk", chk_riscv_ifetch_preclock_posedge_clk_fn, (t_engine_callback_fn) NULL );
    engine->register_clock_fn( engine_handle, (void *)this, "clk", engine_sim_function_type_posedge_clock, chk_riscv_ifetch_clock_fn );

#define REGISTER_OUTPUT(s,w) \
    engine->register_output_signal(engine_handle, #s, w, &outputs.s); \
    engine->register_output_generated_on_clock(engine_handle, #s, "clk", 1 );
#define REGISTER_INPUT(s,w) \
    engine->register_input_signal(engine_handle, #s, w, &inputs.s); \
    engine->register_input_used_on_clock(engine_handle, #s, "clk", 1 );

    REGISTER_INPUT(fetch_req__flush_pipeline,1);
    REGISTER_INPUT(fetch_req__req_type,3);
    REGISTER_INPUT(fetch_req__debug_fetch,1);
    REGISTER_INPUT(fetch_req__address,32);
    REGISTER_INPUT(fetch_req__mode,3);
    REGISTER_INPUT(fetch_req__predicted_branch,1);
    REGISTER_INPUT(fetch_req__pc_if_mispredicted,32);
    
    REGISTER_INPUT(fetch_resp__valid,1);
    REGISTER_INPUT(fetch_resp__debug,1);
    REGISTER_INPUT(fetch_resp__data,32);
    REGISTER_INPUT(fetch_resp__mode,3);
    REGISTER_INPUT(fetch_resp__error,1);
    REGISTER_INPUT(fetch_resp__tag,2);
    
    REGISTER_OUTPUT(error_detected,1);
    REGISTER_OUTPUT(cycle,32);

    outputs.error_detected = 0;
    outputs.cycle = 0;
}

/*f c_chk_riscv_ifetch::~c_chk_riscv_ifetch
*/
c_chk_riscv_ifetch::~c_chk_riscv_ifetch()
{
    delete_instance();
}

/*f c_chk_riscv_ifetch::delete_instance
*/
t_sl_error_level c_chk_riscv_ifetch::delete_instance( void )
{
    if (verify.hier_mem) { sl_hier_mem_free(verify.hier_mem); }
    return error_level_okay;
}

/*f c_chk_riscv_ifetch::message
*/
t_sl_error_level c_chk_riscv_ifetch::message( t_se_message *message )
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

/*a Verification methods
*/
/*f verify_reset */
static int page_sizes[] = {14,10,10,10,0};
int
c_chk_riscv_ifetch::verify_create_memory(void)
{
    if (!verify.hier_mem) {
        verify.hier_mem = sl_hier_mem_create(1ULL<<32, page_sizes, sl_hier_mem_unwritten_data_zero, 8);
    }
    return (verify.hier_mem!=NULL);
}

void
c_chk_riscv_ifetch::verify_reset(void)
{
    if (verify.hier_mem) {
        sl_hier_mem_free(verify.hier_mem);
        verify_create_memory();
    }
    verify.last_req_type = rv_fetch_none;
    verify.address = 0;
}

/*f verify_memory_check_and_set
  word_address = 32-bit word address
  data = 32-bits of data expected to be there
  mask = 32-bits of mask of data which must match

  Always set the memory at the address to be | mask and data
  if data matches then return 0
 */
int
c_chk_riscv_ifetch::verify_memory_check_and_set(t_sl_uint64 word_address, t_sl_uint64 data, t_sl_uint64 mask, t_sl_uint64 *old_data)
{
    t_sl_hier_mem_data_ptr b_ptr;
    t_sl_uint64 *ptr;
    t_sl_uint64 mem_mask, mem_data;
    t_sl_uint64 combined_mask;
    int mismatch;
    if (!verify_create_memory()) return 1;
    b_ptr = sl_hier_mem_find(verify.hier_mem, word_address, 1 ); // allocate please!
    ptr = (t_sl_uint64 *)b_ptr;
    mem_data = *ptr;
    mem_mask = mem_data >> 32;
    mem_data = mem_data & 0xffffffffULL;
    mem_mask = mem_mask & 0xffffffffULL;
    combined_mask = mem_mask & mask;
    mismatch = ((mem_data & combined_mask) != (data & combined_mask));
    if (mismatch) *old_data = mem_data;
    mem_mask |= mask;
    mem_data = (mem_data &~ mask) | (data & mask);
    mem_data = mem_data & 0xffffffffULL;
    mem_mask = mem_mask & 0xffffffffULL;
    *ptr = (mem_data<<0) | (mem_mask<<32);
    return mismatch;
}

/*f verify_error */
void
c_chk_riscv_ifetch::verify_error(const char *format, ...)
{
    char buf[256];
    va_list ap;
    va_start(ap, format);
    (void) vsnprintf(buf, sizeof(buf), format, ap);
    va_end(ap);
    engine->add_error( (void *)__FILE__,
                       error_level_serious,
                       error_number_general_error_ssd, 0,
                       error_arg_type_const_string, "Risc-V Ifetch checker",
                       error_arg_type_malloc_string, buf,
                       error_arg_type_integer, engine->cycle(),
                       error_arg_type_const_filename, __FILE__,
                       error_arg_type_line_number, __LINE__,
                       error_arg_type_none );

    outputs.error_detected = 1;
    outputs.cycle = engine->cycle();
}

/*f verify_fetch_request */
void
c_chk_riscv_ifetch::verify_fetch_request(void)
{
    switch (input.fetch_req.req_type) {
    case rv_fetch_none: {
        break;
    }
    case rv_fetch_nonsequential: {
        break;
    }
    case rv_fetch_repeat: {
        if (verify.address != input.fetch_req.address) {
            verify_error("Unexpected address for repeat (%08x/%08x)", verify.address, input.fetch_req.address);
        }
        if (verify.last_req_type == rv_fetch_none) {
            verify_error("Repeat fetch following a none fetch breaks protocol (last was %d)", verify.last_req_type);
        }
        break;
    }
    case rv_fetch_sequential_16: {
        if (verify.address+2 != input.fetch_req.address) {
            verify_error("Unexpected address for sequential_16 (%08x/%08x)", verify.address+2, input.fetch_req.address);
        }
        if (verify.last_req_type == rv_fetch_none) {
            verify_error("Sequential_16 fetch following a none fetch breaks protocol (last was %d)", verify.last_req_type);
        }
        break;
    }
    case rv_fetch_sequential_32: {
        if (verify.address+4 != input.fetch_req.address) {
            verify_error("Unexpected address for sequential_32 (%08x/%08x)", verify.address+4, input.fetch_req.address);
        }
        if (verify.last_req_type == rv_fetch_none) {
            verify_error("Sequential_32 fetch following a none fetch breaks protocol (last was %d)", verify.last_req_type);
        }
        break;
    }
    }
    verify.last_req_type = (t_riscv_fetch_req_type) input.fetch_req.req_type;
    verify.address = input.fetch_req.address;
}

/*f verify_fetch_response */
void
c_chk_riscv_ifetch::verify_fetch_response(void)
{
    if (input.fetch_req.req_type==rv_fetch_none) {
        if (input.fetch_resp.valid) {
            verify_error("Received a 'valid' fetch response when none was requested");
        }
    } else {
        if (input.fetch_resp.valid) {
            t_sl_uint64 address = input.fetch_req.address;
            t_sl_uint64 word_address = address>>2;
            t_sl_uint64 old_data;
            switch (address&3) {
            case 0: {
                if (verify_memory_check_and_set( word_address, input.fetch_resp.data, 0xffffffffULL, &old_data )) {
                    verify_error("Data for instruction fetch at address %08x was not that expected %08x %08x", address, input.fetch_resp.data, old_data);
                }
                break;
            }
            case 2: {
                if (verify_memory_check_and_set( word_address,   input.fetch_resp.data<<16, 0xffff0000ULL, &old_data) ||
                    verify_memory_check_and_set( word_address+1, input.fetch_resp.data>>16, 0xffffULL, &old_data)  ) {
                    verify_error("Data for instruction fetch at address %08x was not that expected %08x %08x", address, input.fetch_resp.data, old_data);
                }
                break;
            }
            default: {
                verify_error("Data for odd address %08x cannot be checked", address);
            }
            }
        }
    }
}

/*a Class preclock/clock methods for chk_riscv_ifetch
*/
/*f c_chk_riscv_ifetch::capture_inputs
*/
t_sl_error_level c_chk_riscv_ifetch::capture_inputs( void )
{
    if (connected_okay==0) {
        connected_okay = 1;
        if (inputs.fetch_req__flush_pipeline==NULL) connected_okay=-1;
        if (inputs.fetch_req__req_type==NULL) connected_okay=-1;
        if (inputs.fetch_req__debug_fetch==NULL) connected_okay=-1;
        if (inputs.fetch_req__address==NULL) connected_okay=-1;
        if (inputs.fetch_req__mode==NULL) connected_okay=-1;
        if (inputs.fetch_req__predicted_branch==NULL) connected_okay=-1;
        if (inputs.fetch_req__pc_if_mispredicted==NULL) connected_okay=-1;
        if (inputs.fetch_resp__valid==NULL) connected_okay=-1;
        if (inputs.fetch_resp__debug==NULL) connected_okay=-1;
        if (inputs.fetch_resp__data==NULL) connected_okay=-1;
        if (inputs.fetch_resp__mode==NULL) connected_okay=-1;
        if (inputs.fetch_resp__error==NULL) connected_okay=-1;
        if (inputs.fetch_resp__tag==NULL) connected_okay=-1;
    }
    if (connected_okay<0) { return error_level_okay; }
    input.fetch_req.flush_pipeline      = inputs.fetch_req__flush_pipeline[0];
    input.fetch_req.req_type            = inputs.fetch_req__req_type[0];
    input.fetch_req.debug_fetch         = inputs.fetch_req__debug_fetch[0];
    input.fetch_req.address             = inputs.fetch_req__address[0];
    input.fetch_req.mode                = inputs.fetch_req__mode[0];
    input.fetch_req.predicted_branch    = inputs.fetch_req__predicted_branch[0];
    input.fetch_req.pc_if_mispredicted  = inputs.fetch_req__pc_if_mispredicted[0];

    input.fetch_resp.valid    = inputs.fetch_resp__valid[0];
    input.fetch_resp.debug    = inputs.fetch_resp__debug[0];
    input.fetch_resp.data     = inputs.fetch_resp__data[0];
    input.fetch_resp.mode     = inputs.fetch_resp__mode[0];
    input.fetch_resp.error    = inputs.fetch_resp__error[0];
    input.fetch_resp.tag      = inputs.fetch_resp__tag[0];

    return error_level_okay;
}

/*f c_chk_riscv_ifetch::prepreclock
*/
t_sl_error_level c_chk_riscv_ifetch::prepreclock( void )
{
    WHERE_I_AM;
    inputs_captured=0;
    clocks_to_call=0;
    return error_level_okay;
}

/*f c_chk_riscv_ifetch::preclock
*/
t_sl_error_level c_chk_riscv_ifetch::preclock(void)
{
    WHERE_I_AM;
    if (!inputs_captured) { capture_inputs(); inputs_captured++; }
    clocks_to_call++;
    return error_level_okay;
}

/*f c_chk_riscv_ifetch::clock
*/
t_sl_error_level c_chk_riscv_ifetch::clock( void )
{
    WHERE_I_AM;
    if (clocks_to_call>0) {
        clocks_to_call=0;
        outputs.error_detected = 0;
        verify_fetch_request();
        verify_fetch_response();
    }
    return error_level_okay;
}

/*a Initialization functions
*/
/*f chk_riscv_ifetch__init
*/
extern void chk_riscv_ifetch__init( void )
{
    se_external_module_register( 1, "chk_riscv_ifetch", chk_riscv_ifetch_instance_fn, "cdl_model" );
}

/*a Scripting support code
*/
/*f initchk_riscv_ifetch
*/
extern "C" void initchk_riscv_ifetch( void )
{
    chk_riscv_ifetch__init( );
    scripting_init_module( "chk_riscv_ifetch" );
}

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
