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
 * @file   axi_types.h
 * @brief  Header file for AXI exec_file types
 *
 */

/*a Wrapper */
#ifndef __INC_AXI_TYPES
#define __INC_AXI_TYPES

#include "axi.h"
#include "sl_exec_file.h"

template <typename T>
class c_axi_queue {
private:
    struct t_axi_queue_elt {
        struct t_axi_queue_elt *next;
        int option;
        T data;
    };
    struct t_axi_queue_elt *head;
    struct t_axi_queue_elt *tail;
    int max_size;
    int count;

public:
    c_axi_queue(int max_size);
    ~c_axi_queue();
    inline int is_empty(void) {return count==0;}
    inline int is_full(void)  {return count==max_size;}
    int enqueue(T *elt, int option); // return 0 on failure
    int dequeue(T *elt, int *option); // return NULL on failure
};

extern void *ef_axi_req_create( t_sl_exec_file_data *file_data, const char *name, void *owner, t_axi_request *axi_req, t_sl_exec_file_method *additional_methods );
extern void *ef_axi_write_data_create( t_sl_exec_file_data *file_data, const char *name, void *owner, t_axi_write_data *axi_req, t_sl_exec_file_method *additional_methods );
extern void *ef_axi_write_response_create( t_sl_exec_file_data *file_data, const char *name, void *owner, t_axi_write_response *axi_req, t_sl_exec_file_method *additional_methods );
extern void *ef_axi_read_response_create( t_sl_exec_file_data *file_data, const char *name, void *owner, t_axi_read_response *axi_req, t_sl_exec_file_method *additional_methods );
extern void *ef_axi4s_create( t_sl_exec_file_data *file_data, const char *name, void *owner, t_axi4s *axi_req, t_sl_exec_file_method *additional_methods );

extern void                 *ef_owner_of_objf(t_sl_exec_file_object_desc *object_desc);
extern t_axi_request        *ef_axi_request_of_objf(t_sl_exec_file_object_desc *object_desc);
extern t_axi_write_data     *ef_axi_write_data_of_objf(t_sl_exec_file_object_desc *object_desc);
extern t_axi_write_response *ef_axi_write_response_of_objf(t_sl_exec_file_object_desc *object_desc);
extern t_axi_read_response  *ef_axi_read_response_of_objf(t_sl_exec_file_object_desc *object_desc);
extern t_axi4s              *ef_axi4s_of_objf(t_sl_exec_file_object_desc *object_desc);

/*a Wrapper */
#endif
