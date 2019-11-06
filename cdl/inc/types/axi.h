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
 * @brief  Types for the AXI bus
 *
 * Header file for the types for an AXI bus, but no modules
 *
 */

/*a Types */
/*t t_axi_burst */
typedef enum[2] // 2 bits
{
    axi_burst_fixed    = 0,
    axi_burst_incr     = 1,
    axi_burst_wrap     = 2,
    axi_burst_reserved = 3,
} t_axi_burst;

/*t t_axi_size */
typedef enum[3] // 3 bits
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

/*t t_axi_resp */
typedef enum[2] // 2 bits
{
    axi_resp_okay   = 0,
    axi_resp_exokay = 1,
    axi_resp_slverr = 2,
    axi_resp_decerr = 3,
} t_axi_resp;

/*t t_axi_request */
typedef struct {
    bit valid;
    bit[12] id;
    bit[32] addr;
    bit[4] len;
    t_axi_size size;
    t_axi_burst burst;
    bit[2] lock;
    bit[4] cache;
    bit[3] prot;
    bit[4] qos;
    bit[4] region;
    bit[4] user;
} t_axi_request;

/*t t_axi_write_data */
typedef struct {
    bit valid;
    bit[12] id;
    bit[32] data;
    bit[4] strb;
    bit last;
    bit[4] user;
} t_axi_write_data;

/*t t_axi_write_response */
typedef struct {
    bit valid;
    bit[12] id;
    t_axi_resp resp;
    bit[4] user;
} t_axi_write_response;

/*t t_axi_read_response */
/**
 * This structure is used to store read response
 */
typedef struct {
    bit valid;
    bit[12] id;
    bit[32] data;
    t_axi_resp resp;
    bit last;
    bit[4] user;
} t_axi_read_response;

/*t t_axi4s_user */
typedef enum[8] {
    axi4s_user_rx_complete = 8h0, // 16-bit packet length in user[16;8]
    axi4s_user_timestamp   = 8h1, // 24-bit nsec timestamp in user[24;8]
    axi4s_user_rx_error    = 8h2, // 16-bit erro reason in user[16;8]
    axi4s_user_undefined = 8hff
} t_axi4s_user;

/*t t_axi4s32_content */
typedef struct {
    bit     last;
    bit[64] id;
    bit[64] dest;
    bit[64] user  "May be byte-specific - in which case 16 bits per byte - or transfer-wide";
    bit[4]  strb  "Optional if every transfer is full 32-bits (default is high)";
    bit[4]  keep  "Optional if every transfer is packed (default is high)";
    bit[32] data;
} t_axi4s32_content;

/*t t_axi4s32 */
typedef struct {
    bit valid;
    t_axi4s32_content t;
} t_axi4s32;
