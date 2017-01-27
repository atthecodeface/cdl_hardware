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
 * @file   bbc_shm.h
 * @brief  BBC shared memory class for use by shared memory users
 *
 * Header file for BBC shared memory class; this class is used by
 * shared memory applications such as the display viewer C model for
 * BBC simulations, and for the VNC server that allows VNC clients to
 * interact with the simulation.
 *
 */

/*a Wrapper */
#ifndef __INC_BBC_SHM
#define __INC_BBC_SHM

/*a Includes */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h> 
#include <stddef.h> 
#include <sys/types.h> 
#include <sys/stat.h> 
#include <fcntl.h>
#include <unistd.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <inttypes.h>

#ifndef SHM_HUGETLB
#define SHM_HUGETLB 0
#endif

/*t c_bbc_shm */
/**
 * Class for creating and accessing a shared memory for use in
 * simulation and interaction with simulation.
 *
 * The 'server' creates a new instance with a specified data size, e.g.:
 *
 *  shm = new c_bbc_shm("/tmp/bbc_shm.lock", 0xbbc, data_size);
 *
 * and other 'clients' use a data_size of 0.
 *
 * The returned class instance has a 'data' property that points to
 * the shared memory.
 * 
 */
class c_bbc_shm {
private:
    int  shm_alloc(int byte_size);
    void close(void);
    /** Private shared memory lock filename **/
    const char *shm_lock_filename;
    /** Private shared memory key **/
    int        shm_key;
    /** Private shared memory lock file, opened in shm_alloc, closed
     * in close **/
    FILE       *shm_lock_file;
    /** Private shared memory id **/
    int        shm_id;
public:
    c_bbc_shm(const char *lock_filename, int key, int byte_size);
    ~c_bbc_shm();
    /** Pointer to shared memory data **/
    void       *data;
    /** Size of allocated data **/
    int        byte_size;
};

/*a Wrapper */
#endif

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
