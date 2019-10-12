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
 * @file   input_devices.h
 * @brief  Input device header file for CDL modules
 *
 * Header file for the types and CDL modules for input devices
 *
 */

/*a Key codes
The PS2 codes are:

Extended:
//Prt Scr     E012E07C 
//Pause/Break E11477E1F014E077 

Alt (right) E011
Ctrl        E014
Windows (right) E027
Menus       E02F 
KP/         E04A 
KPEnter     E05A 
End         E069 
Left Arrow  E06B 
Home        E06C 
Insert      E070 
Delete      E071 
Down Arrow  E072 
Right Arrow E074 
Up Arrow    E075 
Page Down   E07A 
Page Up     E07D 
Windows     E01F

01 F9
03 F5
04 F3
05 F1
06 F2
07 F12
09 F10
0A F8
0B F6
0C F4
0D Tab
0E `
11 Alt (left)
12 Shift
14 Ctrl
15 Q
16 1
1A Z
1B S
1C A
1D W
1E 2
21 C
22 X
23 D
24 E
25 4
26 3
29 Spacebar
2A V
2B F
2C T
2D R
2E 5
31 N
32 B
33 H
34 G
35 Y
36 6
3A M
3B J
3C U
3D 7
3E 8
41 ,
42 K
43 I
44 O
45 0
46 9
49 .
4A /
4B L
4C ;
4D P
4E -
52 '
54 [
55 =
58 Caps Lock
59 RtShift
5A Enter
5B ]
5D \
66 Backspace
69 KP1
6B KP4
6C KP7
70 KP0
71 KP.
72 KP2
73 KP5
74 KP6
75 KP8
76 ESC
77 Num Lock
78 F11
79 KP+
7A KP3
7B KP-
7C KP*
7D KP9
7E Scroll Lock
83 F7

 */

/*a Types */
/*t t_ps2_pins */
typedef struct {
    bit data;
    bit clk;
} t_ps2_pins;

/*t t_ps2_rx_data */
typedef struct {
    bit    valid;
    bit[8] data;
    bit    parity_error;
    bit    protocol_error;
    bit    timeout;
} t_ps2_rx_data;

/*t t_ps2_key_state */
typedef struct {
    bit valid;
    bit extended;
    bit release;
    bit[8] key_number;
} t_ps2_key_state;

