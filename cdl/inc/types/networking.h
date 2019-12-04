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
 * @file   networking.h
 * @brief  Types for networking that cross protocol types
 *
 */

/*a Includes */

/*a Types */
/*t t_packet_stat_type */
typedef enum [3] {
    packet_stat_type_okay           "Packet received okay",
    packet_stat_type_short          "Packet too short to be received",
    packet_stat_type_long           "Packet too long to be received",
    packet_stat_type_data_error     "Data had error during packet",
    packet_stat_type_carrier        "Carrier lost during packet / outside packet",
    packet_stat_type_underrun       "Data not ready when required",
} t_packet_stat_type;

/*t t_packet_stat */
typedef struct {
    bit                 valid        "Asserted if packet stat is valid; if deasserted, the rest of the fields should be ignored";
    t_packet_stat_type  stat_type    "Type of stat - valid packet, packet too short, packet too long, errored packet, carrier lost, etc";
    bit[16]             byte_count   "Size of a packet if the packet is not in error";
    bit                 is_broadcast "Asserted if the packet had a broadcast address";
    bit                 is_multicast "Asserted if the packet had a multicast address";
} t_packet_stat;
