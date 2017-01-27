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
 * @file   bbc_display_vnc.cpp
 * @brief  BBC VNC display application code
 *
 * Code to provide a simple VNC server using the BBC SHM frame buffer
 * and keyboard interaction, and using vnc_rfb as the server code to
 * do the hard work on the VNC server side. Connects to the
 * bbc_display CDL C model, which allocates the shared memryo BBC SHM
 * frame buffer and keyboard setup; that module ties it in with the
 * simulation.
 */

/*a Includes */
#include "vnc_rfb.h"
#include "fb.h"
#include "bbc_shm.h"
#include "bbc_display.h"

/*a Types */
/**
 * Keyboard mapping entry, giving the VNC RFB key number and the
 * column and row to which it maps on a BBC micro keyboard
 */
typedef struct t_kbd_map {
    /** VNC RFB key value of the mapping */
    int key;
    /** BBC micro keyboard column of the key */
    int column;
    /** BBC micro keyboard row of the key */
    int row;
} t_kbd_map;

/*a Static variables */
/*v vnc_bbc_kbd_map */
/**
 * Map from VNC keyboard codes to column/row of a BBC micro keyboard matrix
 */
static t_kbd_map vnc_bbc_kbd_map[] = {
    {0xffe1, 0, 0}, // shift
    {0xffe3, 1, 0}, // control

    {'Q', 0, 1},
    {'3', 1, 1}, // BBC 3#
    {'#', 1, 1},
    {'4', 2, 1}, // BBC 4$
    {'$', 2, 1},
    {'5', 3, 1}, // BBC 5%
    {'%', 3, 1},
    {0xffc1, 4, 1}, // f4
    {'8', 5, 1}, // BBC 8*
    {'*', 5, 1},
    {0xffc4, 6, 1}, // f7
    {'-', 7, 1}, // =-
    {'_', 7, 1}, // =-
    {'~', 8, 1}, // ~^
    //' ', 9, 1, // left

    {0xffc7, 0, 2}, // f10==f0
    {'W', 1, 2},
    {'E', 2, 2},
    {'T', 3, 2},
    {'7', 4, 2}, // BBC 7'
    {'&', 4, 2},
    {'I', 5, 2},
    {'9', 6, 2}, // BBC 9)
    {'(', 6, 2},
    {'0', 7, 2}, // BBC 0)
    {')', 7, 2},
    {'_', 8, 2},
    //{'', 8, 2}, // BBC _pounds
    //{'3', 9, 2}, // down

    {'1', 0, 3},
    {'!', 0, 3},
    {'2', 1, 3},
    {'@', 1, 3},
    {'D', 2, 3},
    {'R', 3, 3},
    {'6', 4, 3}, // BBC 6&
    {'^', 4, 3},
    {'U', 5, 3},
    {'O', 6, 3},
    {'P', 7, 3},
    {'[', 8, 3},
    {'{', 8, 3},
    {0xff52, 9, 3}, // UP

    //{'Q', 0, 4}, Caps lock
    {'A', 1, 4},
    {'X', 2, 4},
    {'F', 3, 4},
    {'Y', 4, 4},
    {'J', 5, 4},
    {'K', 6, 4},
    //{'@', 7, 4}, // BBC @
    {'\'', 8, 4}, // BBC :*
    {'"', 8, 4}, // BBC :*
    {0xff0d, 9, 4}, // ret

    //{'Q', 0, 5}, Shift lock
    {'S', 1, 5},
    {'C', 2, 5},
    {'G', 3, 5},
    {'H', 4, 5},
    {'N', 5, 5},
    {'L', 6, 5},
    {';', 7, 5}, // BBC +;
    {':', 7, 5},
    {']', 8, 5},
    {'}', 8, 5},
    {0xff08, 9, 5}, //Delete

    {'\t', 0, 6},
    {'Z', 1, 6},
    {' ', 2, 6},
    {'V', 3, 6},
    {'B', 4, 6},
    {'M', 5, 6},
    {'<', 6, 6},
    {',', 6, 6},
    {'>', 7, 6},
    {'.', 7, 6},
    {'?', 8, 6},
    {'/', 8, 6},
    //{'3', 9, 6}, // copy

    {0xff1b, 0, 7}, // escape
    {0xffbe, 1, 7}, // f1
    {0xffbf, 2, 7}, // f2
    {0xffc0, 3, 7}, // f3
    {0xffc2, 4, 7}, // f5
    {0xffc3, 5, 7}, // f6
    {0xffc5, 6, 7}, // f8
    {0xffc6, 7, 7}, // f9
    {'\\', 8, 7},
    {'|', 8, 7},
    //{'3', 9, 7}, // right

    {-1, -1, -1,},
};

/*
        0      1      2      3      4      5      6      7      8      9   
    7  Esc    F1     F2     F3     F5     F6     F8     F9     \|     Rght   
    6  Tab     Z     Spc     V      B      M     <,     >.     ?/     Copy                              
    5  ShLk    S      C      G      H      N      L     +;     }]     Del                              
    4  CpLk    A      X      F      Y      J      K      @     :      Ret                            
    3   1      2      D      R      6      U      O      P     [{     Up                         
    2  F0      W      E      T      7      I      9      0     _      Down                         
    1   Q      3      4      5     F4      8     F7     =-     ~^     Left                         
    0  Shft   Ctrl   DIP7   DIP7   DIP7   DIP7   DIP7   DIP7   DIP7   DIP7                                                                            
*/
/*a Static functions */
/*f key_pressed */
/**
 * This is a callback function invoked by the polling of a VNC RFB,
 * called when a key press/release is given to the VNC RFB server
 *
 * The shared memory structure (fbk) keys down is updated, after
 * looking up @key in the @vnc_bbc_kbd_map
 *
 * @param vnc   VNC RFB class instance invoking the callback
 * @param down  If non-zero, the key is being pressed; if zero, the key is being released
 * @param key   VNC RFB key code of the key being pressed or released
 */
static void
key_pressed(c_vnc_rfb *vnc, int down, int key)
{
    t_framebuffer_and_keys *fbk;
    fbk = (t_framebuffer_and_keys *)vnc->handle;
    if (key==0xffc9) {fbk->fbk->reset_pressed = down;}
    if (key>='a' && key<='z') {key-=32;}
    // fbk->fbk is the shared memory
    for (int i=0; vnc_bbc_kbd_map[i].key!=-1; i++) {
        if (vnc_bbc_kbd_map[i].key == key) {
            int c, r;
            c = vnc_bbc_kbd_map[i].column;
            r = vnc_bbc_kbd_map[i].row;
            t_sl_uint64 k, kv;
            kv = 1ULL<<((c&7)*8+r);
            k = fbk->fbk->keys_down.cols_0_to_7;
            if (c>=8) { k = fbk->fbk->keys_down.cols_8_to_9; }
            if (down)  k |= kv;
            if (!down) k &= ~kv;
            if (c>=8) { fbk->fbk->keys_down.cols_8_to_9 = k; }
            else      { fbk->fbk->keys_down.cols_0_to_7 = k; }
            break;
        }
    }
    fprintf(stderr,"Keys %04x %d %016llx %016llx\n",key, down, fbk->fbk->keys_down.cols_0_to_7, fbk->fbk->keys_down.cols_8_to_9);
}

/*a External functions */
/*f main */
/**
 * Main program entry point
 *
 * Connects to the BBC shared memory (using c_bbc_shm), which
 * presumably has been created by a simulation of FPGA emulation
 *
 * Opens a VNC RFB server, whose display frame buffer will be copied
 * from the shared memory display.
 *
 * Polls for the VNC RFB server, and on idle for 50ms (20Hz) copies
 * data from the shared memory display to the VNC RFB frame buffer,
 * and commits it; hence VNC RFB clients will get an updated display
 * from the simulation/emulation.
 *
 * @param argc  Number of arguments
 * @param argv  Arguments to invocation
 */
extern int
main(int argc, char **argv) {
    c_vnc_rfb *vnc;
    t_fb *fb;
    class c_bbc_shm *bbc_fb;
    t_framebuffer_and_keys fbk;

    const char *shm_lock_filename="/tmp/bbc_shm.lock";
    const int shm_key = 0xbbc;
    bbc_fb = new c_bbc_shm(shm_lock_filename, shm_key, 0);
    if (!bbc_fb->data) {
        fprintf(stderr,"Failed to open shared memory\n");
        return 4;
    }
    fbk = *(t_framebuffer_and_keys *)bbc_fb->data;
    fbk.fbk = (t_framebuffer_and_keys *)bbc_fb->data;

    printf("Frame buffer %p: %d,%d\n",fbk.fbk,fbk.width, fbk.height);
    fb = fb_init(fbk.width, fbk.height, 8);
    vnc = new c_vnc_rfb(6980, fb);
    vnc->key_fn = key_pressed;
    vnc->handle = (void *)&fbk;
    while (1) {
        if (!vnc->poll(50)) {
            t_fb_rectangle r;
            r.lx=0;
            r.by=0;
            r.rx=fbk.width;
            r.ty=fbk.height;
            fb_copy_rectangle(fb, 0,0, (unsigned char *)(fbk.fbk->fb_data),fbk.width,fbk.height, &r, 1 );
            vnc->commit();
        }
    }
}

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
