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
 * @file   bbc_shm.cpp
 * @brief  BBC shared memory class for use by shared memory users
 *
 * Code for class used by shared memory applications such as the
 * display viewer C model for BBC simulations, and for the VNC server
 * that allows VNC clients to interact with the simulation.
 *
 */

/*a Includes */
#include "bbc_shm.h"

/*a Methods */
/*f c_bbc_shm::shm_alloc */
/**
 * Private method to allocate shared memory of a specified size,
 * using the class' SHM file details.
 */
int
c_bbc_shm::shm_alloc(int byte_size)
{
    int shm_flags;
    key_t key;
    struct shmid_ds shmid_ds;

    shm_flags = 0x1ff;
    if (byte_size>0) {
        shm_flags |= IPC_CREAT;
        shm_lock_file = fopen(shm_lock_filename,"w");
        if (!shm_lock_file) {
            fprintf(stderr,"Failed to open shm lock file %s\n", shm_lock_filename);
            return 0;
        }
    }
    key = ftok(shm_lock_filename, shm_key);
    
    shm_id = shmget(key, byte_size, SHM_HUGETLB | shm_flags );
    if (shm_id == -1) {
        fprintf(stderr,"Failed to allocate SHM id\n");
        close();
        return 0;
    }
    if (shmctl(shm_id, IPC_STAT, &shmid_ds) != 0) {
        fprintf(stderr,"Failed to find SHM size\n");
        close();
        return 0;
    }
    byte_size = shmid_ds.shm_segsz;
    data = shmat(shm_id, NULL, 0);
    return byte_size;
}

/*f c_bbc_shm::close */
/**
 * Private method to close the SHM file created by shm_alloc.
 *
 * Being shared memory, this does not deallocate the shared memory;
 * that needs an ipcrm call.
 */
void
c_bbc_shm::close(void) {
    if (data != NULL) {
        shmdt(data);
        data = NULL;
        if (shm_lock_file != NULL) {
            struct shmid_ds shmid_ds;
            shmctl(shm_id, IPC_RMID, &shmid_ds);
        }
    }
    if (shm_lock_file) {
        fclose(shm_lock_file);
        shm_lock_file = NULL;
    }
}

/*f c_bbc_shm::c_bbc_shm */
/**
 * Constructor for shared memory instance, setting properties and
 * allocating the memory - or finding a previous allocation
 *
 */
c_bbc_shm::c_bbc_shm(const char *lock_filename, int key, int byte_size) {
    shm_lock_file = NULL;
    shm_lock_filename = lock_filename;
    shm_key = key;
    data = NULL;
    this->byte_size = shm_alloc(byte_size);
}

/*f c_bbc_shm::~c_bbc_shm */
/**
 * Destructor for shared memory instance, closing it down
 *
 */
c_bbc_shm::~c_bbc_shm(void) {
    if (shm_lock_file) close();
}

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
