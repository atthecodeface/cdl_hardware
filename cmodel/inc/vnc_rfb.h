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
 * @file   vnc_rfb.h
 * @brief  VNC RFB header file
 *
 * Header file for remote frame buffer using the VNC RFB protocol; a
 * client of this can provide a frame buffer and notifications of
 * changes to that frame buffer, and a 'c_vnc_rfb' instance will
 * manage communication to a VNC display client as required.
 *
 */

/*a Wrapper */
#ifndef __INC_VNC_RFB
#define __INC_VNC_RFB

/*a Includes */
#include "fb.h"

/*a Defines */
#define RX_BUFFER_SIZE (60*1024)
#define TX_BUFFER_SIZE (32*1024)
#define MAX_RECT 4

/*a Types */
/*t t_vnc_mouse_fn */
/**
 * A callback function that can be invoked when a VNC client moves a mouse
 * or presses/unpresses a button on the mouse
 */
typedef void (*t_vnc_mouse_fn) (class c_vnc_rfb *vnc_rfb, int buttons, int x, int y);

/*t t_vnc_key_fn */
/**
 * A callback function that can be invoked when a VNC client presses
 * or releases a key
 */
typedef void (*t_vnc_key_fn) (class c_vnc_rfb *vnc_rfb, int down, int key);

/*t t_vnc_rfb_msg */
/**
 * Internal structure for a message used in the TCP connection to the VNC client
 *
 * The message starts at 'buffer+offset' and is 'length' chars long
 */
struct t_vnc_rfb_msg {
    unsigned char *buffer;
    int length;
    int offset;
};

/*t t_vnc_rfb_skt_state */
/**
 * State of a VNC client socket, supporting the RFB protocol
 */
typedef enum {
    vnc_rfb_skt_state_not_connected,
    vnc_rfb_skt_state_await_protocol_name,
    vnc_rfb_skt_state_await_client_security_choice,
    vnc_rfb_skt_state_await_client_exclusivity,
    vnc_rfb_skt_state_running
} t_vnc_rfb_skt_state;

/*t c_vnc_rfb */
/**
 * A VNC RFB class permitting a simple application client to have a
 * full-fledged VNC RFB server.
 */
class c_vnc_rfb
{
private:
    int public_socket;
    int client_socket;
    int allowed_encodings;
    int bpp_on_wire;
    int depth;
    int truecolor;
    int bigendian;
    int redmax;
    int greenmax;
    int bluemax;
    int redshift;
    int greenshift;
    int blueshift;
    int reddownshift;
    int greendownshift;
    int bluedownshift;
    t_vnc_rfb_skt_state skt_state;
    int skip_timeout_count;

    int rx_buffer_pos; // position of first character in buffer to be understood
    int rx_buffer_length; // position of last character in buffer
    char rx_buffer[RX_BUFFER_SIZE];

    char tx_buffer[TX_BUFFER_SIZE];
    t_fb_rectangle client_interest; // If the client sends an incremental request, then this will contain it - any updates that overlap this lead to a framebuffer update
    int rectangle_expected; // Set if client has sent a request (incremental or otherwise) and hence the server is the next
    int need_to_send; // Set if rectangle_expected and at least one rects_to_send is valid
    t_fb_rectangle rects_to_send[MAX_RECT]; // FIFO of rectangles to send; cleared first on non-incremental frame buffer update requests, added to on commits and non-incremental frame buffer requests
    t_fb_rectangle rect_being_sent; // Rectangle being sent
    t_fb *fb;

    struct t_vnc_rfb_msg rx_msg;
    struct t_vnc_rfb_msg tx_msg;

    int handle_frame_buffer_update_request(void);
    int handle_set_pixel_format(void);
    int handle_set_encodings(void);
    int handle_callback_requests(void);
    int handle_protocol(void);
    int handle_security_choice(void);
    int handle_exclusivity(void);
    int handle_receive_buffer(void);

    void vnc_msg_init(struct t_vnc_rfb_msg *vnc_msg, char *buffer, int length );
    
    int receive_data(void);
    unsigned int rx_msg_read_card8(void);
    unsigned int rx_msg_read_card16(void);
    unsigned int rx_msg_read_card32(void);

    void tx_msg_add_card8(int card);
    void tx_msg_add_card16(int card);
    void tx_msg_add_card32(int card);
    void tx_msg_add_le16(int card);
    void tx_msg_add_le32(int card);
    void tx_msg_add_padding(int padding);
    void tx_msg_add_buffer(const void *data, int length);
    void tx_msg_add_pixel(int x, int y);
    void tx_msg_send(void);

    void send_first_rectangle(void);

public:
    c_vnc_rfb(int port, t_fb *fb);
    ~c_vnc_rfb();
    int poll(int ms_timeout );
    void commit(void);

    t_vnc_mouse_fn mouse_fn;
    t_vnc_key_fn key_fn;
    void *handle;
    int verbose;
};

/*a Wrapper */
#endif

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
