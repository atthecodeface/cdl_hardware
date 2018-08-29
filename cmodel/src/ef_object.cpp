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
 * @file   ef_object.cpp
 * @brief  Exec-file object with properties
 *
 *
 */
/*a Includes */
#include "be_model_includes.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "sl_debug.h"
#include "sl_exec_file.h"
#include "sl_general.h"
#include "sl_token.h"
#include "ef_object.h"

/*a Defines
 */
#if 1   
#define WHERE_I_AM {}
#else
#define WHERE_I_AM {fprintf(stderr,"%s:%d\n",__func__,__LINE__ );}
#endif

/*a Types
 */
/*t t_ef_object
 */
typedef struct t_ef_object
{
    void *owner;
    void *contents;
    t_ef_property *properties;
    char *name;
    t_sl_exec_file_method methods[1];
} t_ef_object;

/*a Static forward function declarations
 */
static t_sl_exec_file_method_fn ef_set;
static t_sl_exec_file_method_fn ef_get;

/*a Statics
 */
/*v req_obj_methods - Exec file object methods
 */
static t_sl_exec_file_method ef_object_methods[] =
{
    {"set",    'i',  2, "si",  "set", ef_set, NULL },
    {"get",   'i', 1, "s",    "get", ef_get, NULL },
    SL_EXEC_FILE_METHOD_NONE
};

/*a EF request object methods
 */
/*f ef_set
 */
static t_sl_error_level ef_set(t_sl_exec_file_cmd_cb *cmd_cb, void *obj, t_sl_exec_file_object_desc *object_desc, t_sl_exec_file_method *method)
{
    WHERE_I_AM;
    t_ef_object *object = (t_ef_object *)object_desc->handle;
    const char *property  = sl_exec_file_eval_fn_get_argument_string( cmd_cb->file_data, cmd_cb->args, 0 );
    t_sl_uint64 value     = sl_exec_file_eval_fn_get_argument_integer( cmd_cb->file_data, cmd_cb->args, 1 );
    t_ef_property *ef_properties = object->properties;
    for (int i=0; ef_properties[i].name; i++) {
        if (!strcmp(ef_properties[i].name, property)) {
            void *property_element = ((char *)object->contents)+ef_properties[i].offset;
            if (ef_properties[i].ef_type == ef_type_int) {
                ((int *)property_element)[0] = value;
            } else {
                ((t_sl_uint64 *)property_element)[0] = value;
            }
        }
    }
    return error_level_okay;
}

/*f ef_get
 */
static t_sl_error_level ef_get(t_sl_exec_file_cmd_cb *cmd_cb, void *obj, t_sl_exec_file_object_desc *object_desc, t_sl_exec_file_method *method)
{
    WHERE_I_AM;
    t_ef_object *object = (t_ef_object *)object_desc->handle;
    const char *property  = sl_exec_file_eval_fn_get_argument_string( cmd_cb->file_data, cmd_cb->args, 0 );
    t_sl_uint64 value = 0;
    t_ef_property *ef_properties = object->properties;
    for (int i=0; ef_properties[i].name; i++) {
        if (!strcmp(ef_properties[i].name, property)) {
            void *property_element = ((char *)object->contents)+ef_properties[i].offset;
            if (ef_properties[i].ef_type == ef_type_int) {
                value = ((int *)property_element)[0];
            } else {
                value = ((t_sl_uint64 *)property_element)[0];
            }
        }
    }
    return sl_exec_file_eval_fn_set_result( cmd_cb->file_data, value )?error_level_okay:error_level_fatal;
}

/*a Exec file functions
 */
/*f object_message_handler
 */
static t_sl_error_level object_message_handler( t_sl_exec_file_object_cb *obj_cb )
{
    t_ef_object *ef_obj = (t_ef_object *)(obj_cb->object_desc->handle);

    if (!strcmp(obj_cb->data.message.message,"get"))
    {
        ((void **)obj_cb->data.message.client_handle)[0] = ef_obj->contents;
        return error_level_okay;
    }
    return error_level_serious;
}

/*f ef_object_create
 */
extern void *ef_object_create( t_sl_exec_file_data *file_data, const char *name, void *owner, void *contents, t_ef_property *properties, t_sl_exec_file_method *additional_methods )
{
    t_sl_exec_file_object_desc object_desc;

    int i;
    int num_methods;
    for (i=0; ef_object_methods[i].method; i++);
    num_methods = i;
    for (i=0; additional_methods[i].method; i++);
    num_methods += i;

    t_ef_object *ef_obj = (t_ef_object *)malloc( sizeof(t_ef_object) + (num_methods)*sizeof(t_sl_exec_file_method) );
    if (ef_obj)
    {
        memset( ef_obj, 0, sizeof(t_ef_object) );
        for (i=0; ef_object_methods[i].method; i++)
            ef_obj->methods[i] = ef_object_methods[i];
        for (; additional_methods->method; i++, additional_methods++)
            ef_obj->methods[i] = additional_methods[0];
        ef_obj->methods[i] = additional_methods[0];
        ef_obj->name = sl_str_alloc_copy( name );
        ef_obj->owner = owner;
        ef_obj->contents = contents;
        ef_obj->properties = properties;

        memset(&object_desc,0,sizeof(object_desc));
        object_desc.version = sl_ef_object_version_checkpoint_restore;
        object_desc.name = ef_obj->name;
        object_desc.handle = (void *)ef_obj;
        object_desc.methods = ef_obj->methods;
        object_desc.message_handler = object_message_handler;
        sl_exec_file_add_object_instance( file_data, &object_desc );
    }
    return ef_obj;
}

/*f ef_object_contents
 */
extern void *ef_object_contents(void *obj) {
    return ((t_ef_object *)obj)->contents;
}

/*f ef_object_owner
 */
extern void *ef_object_owner(void *obj) {
    return ((t_ef_object *)obj)->owner;
}
