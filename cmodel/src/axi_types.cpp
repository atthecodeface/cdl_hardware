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
#include "axi.h"
#include "ef_object.h"
#include "sl_exec_file.h"
#include <stddef.h>
#include "axi_types.h"

/*a Statics
 */
/*v ef_req_obj_properties - Properties of an AXI request
 */
static t_ef_property ef_req_obj_properties[] =
{
    {"valid",   1, ef_type_int,    offsetof(t_axi_request, valid )},
    {"id",      1, ef_type_int,    offsetof(t_axi_request, id)},
    {"addr",   64, ef_type_int64,  offsetof(t_axi_request, addr)},
    {"len",     8, ef_type_int,    offsetof(t_axi_request, len)},
    {"size",    3, ef_type_int,    offsetof(t_axi_request, size)},
    {"burst",   2, ef_type_int,    offsetof(t_axi_request, burst)},
    {"lock",    1, ef_type_int,    offsetof(t_axi_request, lock)},
    {"cache",   1, ef_type_int,    offsetof(t_axi_request, cache)},
    {"prot",    1, ef_type_int,    offsetof(t_axi_request, prot)},
    {"qos",     1, ef_type_int,    offsetof(t_axi_request, qos)},
    {"region",  1, ef_type_int,    offsetof(t_axi_request, region)},
    {"user",    1, ef_type_int,    offsetof(t_axi_request, user)},
    {NULL, 0, ef_type_int,  0}
};

/*v ef_write_data_obj_properties - Properties of AXI write data
 */
static t_ef_property ef_write_data_obj_properties[] =
{
    {"valid", 1, ef_type_int,  offsetof(t_axi_write_data, valid)},
    {"id", 1, ef_type_int,     offsetof(t_axi_write_data, id)},
    {"data", 1, ef_type_int64, offsetof(t_axi_write_data, data)},
    {"strb", 1, ef_type_int,   offsetof(t_axi_write_data, strb)},
    {"last", 1, ef_type_int,   offsetof(t_axi_write_data, last)},
    {"user", 1, ef_type_int,   offsetof(t_axi_write_data, user)},
    {NULL, 0, ef_type_int,  0}
};

/*v ef_write_response_obj_properties - Properties of AXI write response
 */
static t_ef_property ef_write_response_obj_properties[] =
{
    {"valid", 1, ef_type_int, offsetof(t_axi_write_response, valid)},
    {"id", 1, ef_type_int,    offsetof(t_axi_write_response, id)},
    {"resp", 1, ef_type_int,  offsetof(t_axi_write_response, resp)},
    {"user", 1, ef_type_int,  offsetof(t_axi_write_response, user)},
    {NULL, 0, ef_type_int,  0}
};

/*v ef_read_response_obj_properties - Properties of AXI read response
 */
static t_ef_property ef_read_response_obj_properties[] =
{
    {"valid", 1, ef_type_int,  offsetof(t_axi_read_response, valid)},
    {"id", 1, ef_type_int,     offsetof(t_axi_read_response, id)},
    {"data", 1, ef_type_int64, offsetof(t_axi_read_response, data)},
    {"resp", 1, ef_type_int,   offsetof(t_axi_read_response, resp)},
    {"last", 1, ef_type_int,   offsetof(t_axi_read_response, last)},
    {"user", 1, ef_type_int,   offsetof(t_axi_read_response, user)},
    {NULL, 0, ef_type_int,  0}
};

/*v ef_axi4s_obj_properties - Properties of an AXI request
 */
static t_ef_property ef_axi4s_obj_properties[] =
{
    {"data",   64, ef_type_int64,  offsetof(t_axi4s, data)},
    {"strb",   64, ef_type_int64,  offsetof(t_axi4s, strb)},
    {"keep",   64, ef_type_int64,  offsetof(t_axi4s, keep)},
    {"user",   64, ef_type_int64,  offsetof(t_axi4s, user)},
    {"last",   1,  ef_type_int,    offsetof(t_axi4s, last)},
    {"id",     64, ef_type_int64,  offsetof(t_axi4s, id)},
    {"dest",   64, ef_type_int64,  offsetof(t_axi4s, dest)},
    {NULL, 0, ef_type_int,  0}
};

/*a Exec file functions
 */
/*f ef_axi_req_create
 */
extern void *ef_axi_req_create( t_sl_exec_file_data *file_data, const char *name, void *owner, t_axi_request *axi_req, t_sl_exec_file_method *additional_methods )
{
    return (void *)ef_object_create(file_data, name, owner, (void *)axi_req, ef_req_obj_properties, additional_methods );
}

/*f ef_axi_write_data_create
 */
extern void *ef_axi_write_data_create( t_sl_exec_file_data *file_data, const char *name, void *owner, t_axi_write_data *axi_write_data, t_sl_exec_file_method *additional_methods )
{
    return (void *)ef_object_create(file_data, name, owner, (void *)axi_write_data, ef_write_data_obj_properties, additional_methods );
}

/*f ef_axi_write_response_create
 */
extern void *ef_axi_write_response_create( t_sl_exec_file_data *file_data, const char *name, void *owner, t_axi_write_response *axi_write_response, t_sl_exec_file_method *additional_methods )
{
    return (void *)ef_object_create(file_data, name, owner, (void *)axi_write_response, ef_write_response_obj_properties, additional_methods );
}

/*f ef_axi_read_response_create
 */
extern void *ef_axi_read_response_create( t_sl_exec_file_data *file_data, const char *name, void *owner, t_axi_read_response *axi_read_response, t_sl_exec_file_method *additional_methods )
{
    return (void *)ef_object_create(file_data, name, owner, (void *)axi_read_response, ef_read_response_obj_properties, additional_methods );
}

/*f ef_axi4s_create
 */
extern void *ef_axi4s_create( t_sl_exec_file_data *file_data, const char *name, void *owner, t_axi4s *axi4s, t_sl_exec_file_method *additional_methods )
{
    return (void *)ef_object_create(file_data, name, owner, (void *)axi4s, ef_axi4s_obj_properties, additional_methods );
}

/*f ef_owner_of_objf */
extern void *ef_owner_of_objf(t_sl_exec_file_object_desc *object_desc)
{
    return ef_object_owner(object_desc->handle);
}

/*f ef_axi_request_of_objf */
extern t_axi_request *ef_axi_request_of_objf(t_sl_exec_file_object_desc *object_desc)
{
    return (t_axi_request *)ef_object_contents(object_desc->handle);
}

/*f ef_axi_write_data_of_objf */
extern t_axi_write_data *ef_axi_write_data_of_objf(t_sl_exec_file_object_desc *object_desc)
{
    return (t_axi_write_data *)ef_object_contents(object_desc->handle);
}

/*f ef_axi_write_response_of_objf */
extern t_axi_write_response *ef_axi_write_response_of_objf(t_sl_exec_file_object_desc *object_desc)
{
    return (t_axi_write_response *)ef_object_contents(object_desc->handle);
}

/*f ef_axi_read_response_of_objf */
extern t_axi_read_response *ef_axi_read_response_of_objf(t_sl_exec_file_object_desc *object_desc)
{
    return (t_axi_read_response *)ef_object_contents(object_desc->handle);
}

/*f ef_axi4s_of_objf */
extern t_axi4s *ef_axi4s_of_objf(t_sl_exec_file_object_desc *object_desc)
{
    return (t_axi4s *)ef_object_contents(object_desc->handle);
}

/*f c_axi_queue<t> constructor */
template <typename T>
c_axi_queue<T>::c_axi_queue(int max_size)
{
    this->max_size = max_size;
    count = 0;
    head = NULL;
    tail = NULL;
}

/*f c_axi_queue<t> destructor */
template <typename T>
c_axi_queue<T>::~c_axi_queue()
{
}

/*f c_axi_queue<t> enqueue */
template <typename T>
int c_axi_queue<T>::enqueue(T *elt, int option)
{
    struct t_axi_queue_elt *ptr = (struct t_axi_queue_elt *)malloc(sizeof(t_axi_queue_elt));
    ptr->next = NULL;
    ptr->data = *elt;
    ptr->option = option;
    if (is_full()) return 0;
    if (tail) {
        tail->next = ptr;
    } else {
        head = ptr;
    }
    tail = ptr;
    count++;
    return 1;
}

/*f c_axi_queue<t> dequeue */
template <typename T>
int c_axi_queue<T>::dequeue(T *elt, int *option)
{
    if (is_empty()) return 0;
    struct t_axi_queue_elt *ptr = head;
    head = head->next;
    count--;
    if (!head) tail=NULL;
    *elt = ptr->data;
    if (option) {*option = ptr->option;};
    free(ptr);
    return 1;
}

/*f c_axi_queue instantiations */
template class c_axi_queue<t_axi4s>;
template class c_axi_queue<t_axi_request>;
template class c_axi_queue<t_axi_write_data>;
template class c_axi_queue<t_axi_write_response>;
template class c_axi_queue<t_axi_read_response>;
