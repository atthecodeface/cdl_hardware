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
 * @file   kasumi_types.cdl
 * @brief  Types for the Kasumi acceleration and ciphering
 *
 */

/*a Types */
typedef enum[4] {
    kasumi_op_shift_key,      // Shift in 64 bits of key
    kasumi_op_set_auth_data,  // Set auth data (count and bearer and direction for f8)
    kasumi_op_cipher_stream,  // Cipher stream of specified number of bits using an initial 64-bits value provided; KS0=cipher(V); KSN+1=cipher(V^KSN^N)
    kasumi_op_f8_cipher,      // Take specified number of bits and XOR with cipher stream generated using 64 bits of auth data (V=cipher(authdata) with modified key, then keystream)
    kasumi_op_f9_mac_0,       // Take specified number of (plaintext) bits and 64 bits of auth data (count, fresh) with direction 0 and generate MAC
    kasumi_op_f9_mac_1,       // Take specified number of (plaintext) bits and 64 bits of auth data (count, fresh) with direction 1 and generate MAC
    kasumi_op_f8_f9_encrypt_0,  // Take specified number of bits of plaintext, 64 bits of auth data for f8, different 64 bits of auth data for f9, with direction 0, and produce output data and MAC
    kasumi_op_f8_f9_encrypt_1,  // Take specified number of bits of plaintext, 64 bits of auth data for f8, different 64 bits of auth data for f9, with direction 0, and produce output data and MAC
    kasumi_op_f8_f9_decrypt_0,  // Take specified number of bits of ciphertext, 64 bits of auth data for f8, different 64 bits of auth data for f9, with direction 0, and produce output data and MAC
    kasumi_op_f8_f9_decrypt_1,  // Take specified number of bits of ciphertext, 64 bits of auth data for f8, different 64 bits of auth data for f9, with direction 0, and produce output data and MAC
    kasumi_op_f9,               // Take specified number of bits and assume it is fully describing an authdata + data + direction + padding and generate MAC
} t_kasumi_op;
typedef struct {
    t_kasumi_op op;
    bit[4]      tag    "Tag of the request";
    bit[16]     length "Additional data length";
    bit[64]     data   "Interpreted as length in bits for ciphering";
} t_kasumi_acceleration_request;

/*t t_kasumi_input
 *
 * Input data for Kasumi
 *
 */
typedef struct {
    bit valid;
    bit[64] data;
    bit[64] k0;
    bit[64] k1;
} t_kasumi_input;

/*t t_kasumi_output
 *
 * Output data for Kasumi
 *
 */
typedef struct {
    bit valid;
    bit[64] data;
} t_kasumi_output;

