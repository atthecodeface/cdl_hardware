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
 * @file   chk_riscv_trace.cpp
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


/*a Types for chk_riscv_trace
*/
/*t t_chk_riscv_trace_inputs
*/
typedef struct t_chk_riscv_trace_inputs {
    t_sl_uint64 *trace__instr_valid;
    t_sl_uint64 *trace__mode;
    t_sl_uint64 *trace__instr_pc;
    t_sl_uint64 *trace__instruction;
    t_sl_uint64 *trace__branch_taken;
    t_sl_uint64 *trace__branch_target;
    t_sl_uint64 *trace__trap;
    t_sl_uint64 *trace__ret;
    t_sl_uint64 *trace__jalr;
    t_sl_uint64 *trace__rfw_retire;
    t_sl_uint64 *trace__rfw_data_valid;
    t_sl_uint64 *trace__rfw_rd;
    t_sl_uint64 *trace__rfw_data;
    t_sl_uint64 *trace__bkpt_valid;
    t_sl_uint64 *trace__bkpt_reason;
} t_chk_riscv_trace_inputs;

/*t t_chk_riscv_trace_outputs
*/
typedef struct t_chk_riscv_trace_outputs {
    t_sl_uint64 error_detected;
    t_sl_uint64 cycle;
} t_chk_riscv_trace_outputs;

/*t t_chk_riscv_trace_input_state
*/
typedef struct {
    struct {
        t_sl_uint64 instr_valid;
        t_sl_uint64 mode;
        t_sl_uint64 instr_pc;
        t_sl_uint64 instruction;
        t_sl_uint64 branch_taken;
        t_sl_uint64 branch_target;
        t_sl_uint64 trap;
        t_sl_uint64 ret;
        t_sl_uint64 jalr;
        t_sl_uint64 rfw_retire;
        t_sl_uint64 rfw_data_valid;
        t_sl_uint64 rfw_rd;
        t_sl_uint64 rfw_data;
        t_sl_uint64 bkpt_valid;
        t_sl_uint64 bkpt_reason;
    } trace;
} t_chk_riscv_trace_input_state;

/*t t_match_trace_entry
*/
typedef struct t_match_trace_entry {
    struct t_match_trace_entry *next;
    struct t_match_trace_entry *prev;
    int time;
    int mode;
    t_sl_uint64 pc;
    t_sl_uint64 instruction;
} t_match_trace_entry;

/*t t_match_trace
*/
typedef struct {
    t_match_trace_entry *first;
    t_match_trace_entry *last;
    t_match_trace_entry *next_to_match;
} t_match_trace;

/*t c_chk_riscv_trace
*/
class c_chk_riscv_trace
{
public:
    c_chk_riscv_trace( class c_engine *eng, void *eng_handle );
    ~c_chk_riscv_trace();
    t_sl_error_level delete_instance( void );
    t_sl_error_level capture_inputs( void );
    t_sl_error_level prepreclock( void );
    t_sl_error_level preclock(void);
    t_sl_error_level clock( void );
    t_sl_error_level message( t_se_message *message );
    void match_trace_add(int time, int mode, t_sl_uint64 pc, t_sl_uint64 instruction);
    int match_trace_match(int time, int mode, t_sl_uint64 pc, t_sl_uint64 instruction);
    void verify_reset(void);
    void verify_error(const char *format,...);
    void verify_trace_capture(void);
    void verify_trace_match(void);
    c_engine *engine;
    int clocks_to_call;
    void *engine_handle;
    int inputs_captured;
    int connected_okay;
    FILE *capture_trace;
    t_match_trace match_trace;
    t_chk_riscv_trace_outputs outputs;
    t_chk_riscv_trace_inputs inputs;
    t_chk_riscv_trace_input_state input;
    int match_ignore_start_pc;
    int match_ignore_end_pc;
    int match_ignore_mode_mask;
    int match_search_distance;
    int match_ignore_beyond_trace;
    int cycles;
    int verbose;
};

/*a Match trace methods */
/*f match_trace_add */
void c_chk_riscv_trace::match_trace_add(int time, int mode, t_sl_uint64 pc, t_sl_uint64 instruction)
{
    t_match_trace_entry *ptr;
    if ((pc>=match_ignore_start_pc) && (pc<match_ignore_end_pc)) return;
    if ((1<<mode) & (match_ignore_mode_mask)) return;
    ptr = (t_match_trace_entry *)calloc(1, sizeof(t_match_trace_entry));
    ptr->time = time;
    ptr->mode = mode;
    ptr->pc = pc;
    ptr->instruction = instruction;
    ptr->next = NULL;
    ptr->prev = match_trace.last;
    if (match_trace.last) {
        match_trace.last->next = ptr;
        match_trace.last = ptr;
    } else {
        match_trace.first = ptr;
        match_trace.last = ptr;
        match_trace.next_to_match = ptr;
    }
}

/*f match_trace_match */
int c_chk_riscv_trace::match_trace_match(int time, int mode, t_sl_uint64 pc, t_sl_uint64 instruction)
{
    int mismatch=0;
    if ((pc>=match_ignore_start_pc) && (pc<match_ignore_end_pc)) return 0;
    if ((1<<mode) & (match_ignore_mode_mask)) return 0;
    if (!match_trace.next_to_match) {
        if (match_ignore_beyond_trace) {
            return 0;
        }
        mismatch=1;
        verify_error("No instruction to match at time %d", time );
    } else {
        if (match_trace.next_to_match->mode != mode) {
            mismatch=1;
            verify_error("Execution mode mismatched %d/%d", match_trace.next_to_match->mode, mode);
        }
        if (match_trace.next_to_match->pc != pc) {
            mismatch=1;
            verify_error("Execution pc mismatched %08llx/%08llx", match_trace.next_to_match->pc, pc);
        }
        if (match_trace.next_to_match->instruction != instruction) {
            mismatch=1;
            verify_error("Execution instruction mismatched %08llx/%08llx", match_trace.next_to_match->instruction, instruction);
        }
    }
    if (!mismatch) {
        match_trace.next_to_match = match_trace.next_to_match->next;
        return 0;
    }
    t_match_trace_entry *ptr;
    ptr = match_trace.next_to_match;
    if (!ptr) { ptr=match_trace.last; } else {ptr=ptr->prev;}
    for (int i=0; ptr && (i<match_search_distance); i++) {
        if ((ptr->mode==mode) && (ptr->pc==pc) && (ptr->instruction==instruction)) {
            verify_error("Did match by going back %d instructions", i+1);
            match_trace.next_to_match = ptr->next;
            return mismatch;
        }
        ptr = ptr->prev;
    }
    ptr = match_trace.next_to_match;
    if (ptr) { ptr=ptr->next;}
    for (int i=0; ptr && (i<match_search_distance); i++) {
        if ((ptr->mode==mode) && (ptr->pc==pc) && (ptr->instruction==instruction)) {
            verify_error("Did match by skipping forward back %d instructions", i+1);
            match_trace.next_to_match = ptr->next;
            return mismatch;
        }
        ptr = ptr->next;
    }
    return mismatch;
}

/*a Static wrapper functions for chk_riscv_trace
*/
/*f chk_riscv_trace_instance_fn
*/
static t_sl_error_level chk_riscv_trace_instance_fn( c_engine *engine, void *engine_handle )
{
    c_chk_riscv_trace *mod;
    mod = new c_chk_riscv_trace( engine, engine_handle );
    if (!mod)
        return error_level_fatal;
    return error_level_okay;
}

/*f chk_riscv_trace_delete_fn - simple callback wrapper for the main method
*/
static t_sl_error_level chk_riscv_trace_delete_fn( void *handle )
{
    c_chk_riscv_trace *mod;
    t_sl_error_level result;
    mod = (c_chk_riscv_trace *)handle;
    result = mod->delete_instance();
    delete( mod );
    return result;
}

/*f chk_riscv_trace_prepreclock_fn
*/
static t_sl_error_level chk_riscv_trace_prepreclock_fn( void *handle )
{
    c_chk_riscv_trace *mod;
    mod = (c_chk_riscv_trace *)handle;
    return mod->prepreclock();
}

/*f chk_riscv_trace_clock_fn
*/
static t_sl_error_level chk_riscv_trace_clock_fn( void *handle )
{
    c_chk_riscv_trace *mod;
    mod = (c_chk_riscv_trace *)handle;
    return mod->clock();
}

/*f chk_riscv_trace_message
 */
static t_sl_error_level chk_riscv_trace_message( void *handle, void *arg )
{
    c_chk_riscv_trace *mod;
    mod = (c_chk_riscv_trace *)handle;
    return mod->message((t_se_message *)arg );
}

/*f chk_riscv_trace_preclock_posedge_clk_fn
*/
static t_sl_error_level chk_riscv_trace_preclock_posedge_clk_fn( void *handle )
{
    c_chk_riscv_trace *mod;
    mod = (c_chk_riscv_trace *)handle;
    mod->preclock();
    return error_level_okay;
}

/*a Constructors and destructors for chk_riscv_trace
*/
/*f c_chk_riscv_trace::c_chk_riscv_trace
*/
c_chk_riscv_trace::c_chk_riscv_trace( class c_engine *eng, void *eng_handle )
{
    const char *capture_filename;
    const char *match_filename;
    engine = eng;
    engine_handle = eng_handle;

    engine->register_delete_function( engine_handle, (void *)this, chk_riscv_trace_delete_fn );
    engine->register_message_function( engine_handle, (void *)this, chk_riscv_trace_message );
    capture_filename = engine->get_option_string( engine_handle, "capture_filename", "" );
    match_filename = engine->get_option_string( engine_handle, "match_filename", "" );
    match_search_distance = engine->get_option_int( engine_handle, "match_search_distance", 2 );
    match_ignore_beyond_trace = engine->get_option_int( engine_handle, "ignore_beyond_trace", 1 );
    match_ignore_mode_mask = engine->get_option_int( engine_handle, "ignore_mode_mask", 0 );
    match_ignore_start_pc = engine->get_option_int( engine_handle, "ignore_start_pc", 0 );
    match_ignore_end_pc   = engine->get_option_int( engine_handle, "ignore_end_pc", 0 );

    memset(&inputs, 0, sizeof(inputs));
    memset(&input, 0, sizeof(input));
    capture_trace = NULL;
    if (capture_filename[0]) {
        capture_trace = fopen(capture_filename,"w");
    }
    match_trace.last  = NULL;
    match_trace.first = NULL;
    match_trace.next_to_match = NULL;
    if (match_filename[0]) {
        FILE *f;
        int time;
        int mode;
        t_sl_uint64 pc;
        t_sl_uint64 instruction;
        f = fopen(match_filename,"r");
        while (f && (fscanf(f, "%d,%d,%llx,%llx\n",&time,&mode,&pc,&instruction)==4)) {
            match_trace_add(time,mode,pc,instruction);
        }
        fclose(f);
    }
    connected_okay = 0;

    engine->register_prepreclock_fn( engine_handle, (void *)this, chk_riscv_trace_prepreclock_fn );
    engine->register_preclock_fns( engine_handle, (void *)this, "clk", chk_riscv_trace_preclock_posedge_clk_fn, (t_engine_callback_fn) NULL );
    engine->register_clock_fn( engine_handle, (void *)this, "clk", engine_sim_function_type_posedge_clock, chk_riscv_trace_clock_fn );

#define REGISTER_OUTPUT(s,w) \
    engine->register_output_signal(engine_handle, #s, w, &outputs.s); \
    engine->register_output_generated_on_clock(engine_handle, #s, "clk", 1 );
#define REGISTER_INPUT(s,w) \
    engine->register_input_signal(engine_handle, #s, w, &inputs.s); \
    engine->register_input_used_on_clock(engine_handle, #s, "clk", 1 );

    REGISTER_INPUT(trace__instr_valid,  1);
    REGISTER_INPUT(trace__mode,         3);
    REGISTER_INPUT(trace__instr_pc,     32);
    REGISTER_INPUT(trace__instruction,  32);
    REGISTER_INPUT(trace__branch_taken, 1);
    REGISTER_INPUT(trace__branch_target,32);
    REGISTER_INPUT(trace__trap,         1);
    REGISTER_INPUT(trace__ret,          1);
    REGISTER_INPUT(trace__jalr,         1);
    REGISTER_INPUT(trace__rfw_retire,      1);
    REGISTER_INPUT(trace__rfw_data_valid,  1);
    REGISTER_INPUT(trace__rfw_rd,          5);
    REGISTER_INPUT(trace__rfw_data,       32);
    REGISTER_INPUT(trace__bkpt_valid,      1);
    REGISTER_INPUT(trace__bkpt_reason,     4);
    
    REGISTER_OUTPUT(error_detected,1);
    REGISTER_OUTPUT(cycle,32);

    outputs.error_detected = 0;
    outputs.cycle = 0;
}

/*f c_chk_riscv_trace::~c_chk_riscv_trace
*/
c_chk_riscv_trace::~c_chk_riscv_trace()
{
    delete_instance();
}

/*f c_chk_riscv_trace::delete_instance
*/
t_sl_error_level c_chk_riscv_trace::delete_instance( void )
{
    if (capture_trace) {fclose(capture_trace);}
    capture_trace = NULL;
    return error_level_okay;
}

/*f c_chk_riscv_trace::message
*/
t_sl_error_level c_chk_riscv_trace::message( t_se_message *message )
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
void
c_chk_riscv_trace::verify_reset(void)
{
}

/*f verify_error */
void
c_chk_riscv_trace::verify_error(const char *format, ...)
{
    char buf[256];
    va_list ap;
    va_start(ap, format);
    (void) vsnprintf(buf, sizeof(buf), format, ap);
    va_end(ap);
    engine->add_error( (void *)__FILE__,
                       error_level_serious,
                       error_number_general_error_ssd, 0,
                       error_arg_type_const_string, "Risc-V Trace checker",
                       error_arg_type_malloc_string, buf,
                       error_arg_type_integer, engine->cycle(),
                       error_arg_type_const_filename, __FILE__,
                       error_arg_type_line_number, __LINE__,
                       error_arg_type_none );

    outputs.error_detected = 1;
    outputs.cycle = engine->cycle();
}

/*f verify_trace_capture
  Only invoked if capture_trace is a valid FILE *
 */
void
c_chk_riscv_trace::verify_trace_capture(void)
{
    if (input.trace.instr_valid) {
        t_sl_uint64 pc;
        t_sl_uint64 instruction;
        int mode;
        mode        = input.trace.mode;
        pc          = input.trace.instr_pc;
        instruction = input.trace.instruction;
        fprintf(capture_trace, "%d,%d,%08llx,%08llx\n",
                engine->cycle(), mode, pc, instruction);
    }
}

/*f verify_trace_match */
void
c_chk_riscv_trace::verify_trace_match(void)
{
    if (input.trace.instr_valid) {
        t_sl_uint64 pc;
        t_sl_uint64 instruction;
        int mode;
        mode        = input.trace.mode;
        pc          = input.trace.instr_pc;
        instruction = input.trace.instruction;
        if (!match_trace_match(engine->cycle(), mode, pc, instruction)) {
        }
    }
}

/*a Class preclock/clock methods for chk_riscv_trace
*/
/*f c_chk_riscv_trace::capture_inputs
*/
t_sl_error_level c_chk_riscv_trace::capture_inputs( void )
{
    if (connected_okay==0) {
        connected_okay = 1;
        if (inputs.trace__instr_valid==NULL) connected_okay=-1;
        if (inputs.trace__mode==NULL) connected_okay=-1;
        if (inputs.trace__instr_pc==NULL) connected_okay=-1;
        if (inputs.trace__instruction==NULL) connected_okay=-1;
        if (inputs.trace__branch_taken==NULL) connected_okay=-1;
        if (inputs.trace__branch_target==NULL) connected_okay=-1;
        if (inputs.trace__trap==NULL) connected_okay=-1;
        if (inputs.trace__ret==NULL) connected_okay=-1;
        if (inputs.trace__jalr==NULL) connected_okay=-1;
        if (inputs.trace__rfw_retire==NULL) connected_okay=-1;
        if (inputs.trace__rfw_data_valid==NULL) connected_okay=-1;
        if (inputs.trace__rfw_rd==NULL) connected_okay=-1;
        if (inputs.trace__rfw_data==NULL) connected_okay=-1;
        if (inputs.trace__bkpt_valid==NULL) connected_okay=-1;
        if (inputs.trace__bkpt_reason==NULL) connected_okay=-1;
    }
    if (connected_okay<0) { return error_level_okay; }
    input.trace.instr_valid      = inputs.trace__instr_valid[0];
    input.trace.mode             = inputs.trace__mode[0];
    input.trace.instr_pc         = inputs.trace__instr_pc[0];
    input.trace.instruction      = inputs.trace__instruction[0];
    input.trace.branch_taken     = inputs.trace__branch_taken[0];
    input.trace.branch_target    = inputs.trace__branch_target[0];
    input.trace.trap             = inputs.trace__trap[0];
    input.trace.ret              = inputs.trace__ret[0];
    input.trace.jalr             = inputs.trace__jalr[0];
    input.trace.rfw_retire       = inputs.trace__rfw_retire[0];
    input.trace.rfw_data_valid   = inputs.trace__rfw_data_valid[0];
    input.trace.rfw_rd           = inputs.trace__rfw_rd[0];
    input.trace.rfw_data         = inputs.trace__rfw_data[0];
    input.trace.bkpt_valid       = inputs.trace__bkpt_valid[0];
    input.trace.bkpt_reason      = inputs.trace__bkpt_reason[0];

    return error_level_okay;
}

/*f c_chk_riscv_trace::prepreclock
*/
t_sl_error_level c_chk_riscv_trace::prepreclock( void )
{
    WHERE_I_AM;
    inputs_captured=0;
    clocks_to_call=0;
    return error_level_okay;
}

/*f c_chk_riscv_trace::preclock
*/
t_sl_error_level c_chk_riscv_trace::preclock(void)
{
    WHERE_I_AM;
    if (!inputs_captured) { capture_inputs(); inputs_captured++; }
    clocks_to_call++;
    return error_level_okay;
}

/*f c_chk_riscv_trace::clock
*/
t_sl_error_level c_chk_riscv_trace::clock( void )
{
    WHERE_I_AM;
    if (clocks_to_call>0) {
        clocks_to_call=0;
        outputs.error_detected = 0;
        if (capture_trace) verify_trace_capture();
        if (match_trace.first) verify_trace_match();
    }
    return error_level_okay;
}

/*a Initialization functions
*/
/*f chk_riscv_trace__init
*/
extern void chk_riscv_trace__init( void )
{
    se_external_module_register( 1, "chk_riscv_trace", chk_riscv_trace_instance_fn, "cdl_model" );
}

/*a Scripting support code
*/
/*f initchk_riscv_trace
*/
extern "C" void initchk_riscv_trace( void )
{
    chk_riscv_trace__init( );
    scripting_init_module( "chk_riscv_trace" );
}

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
