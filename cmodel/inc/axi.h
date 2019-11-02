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
 * @file   axi.h
 * @brief  AXI header file
 *
 */

/*a Wrapper */
#ifndef __INC_AXI
#define __INC_AXI

/*a Types */
/*t t_axi_burst */
typedef enum // 2 bits
{
    axi_burst_fixed    = 0,
    axi_burst_incr     = 1,
    axi_burst_wrap     = 2,
    axi_burst_reserved = 3,
} t_axi_burst;

/*t t_axi_size */
typedef enum // 3 bits
{
    axi_size_1    = 0,
    axi_size_2    = 1,
    axi_size_4    = 2,
    axi_size_8    = 3,
    axi_size_16   = 4,
    axi_size_32   = 5,
    axi_size_64   = 6,
    axi_size_128  = 7,
} t_axi_size;

/*t t_axi_request */
/**
 * This structure is used to store read and write requests (ar/aw)
 */
typedef struct {
    int valid;
    int id;
    t_sl_uint64 addr;
    int len;
    int size;
    int burst;
    int lock;
    int cache;
    int prot;
    int qos;
    int region;
    int user;
} t_axi_request;

/*t t_axi_write_data */
/**
 * This structure is used to store write data
 */
typedef struct {
    int valid;
    int id;
    t_sl_uint64 data;
    int strb;
    int last;
    int user;
} t_axi_write_data;

/*t t_axi_write_response */
/**
 * This structure is used to store write responses
 */
typedef struct {
    int valid;
    int id;
    int resp;
    int user;
} t_axi_write_response;

/*t t_axi_read_response */
/**
 * This structure is used to store read response
 */
typedef struct {
    int valid;
    int id;
    t_sl_uint64 data;
    int resp;
    int last;
    int user;
} t_axi_read_response;

/*t t_axi4s32 */
typedef struct {
    t_sl_uint64 data;
    t_sl_uint64 strb;
    t_sl_uint64 keep;
    t_sl_uint64 last;
    t_sl_uint64 user;
    t_sl_uint64 id;
    t_sl_uint64 dest;
} t_axi4s;

/*a Wrapper */
#endif
