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
 * @file   vnc_rfb.cpp
 * @brief  VNC RFB class supporting simple VNC server applications
 *
 * Code to support a simple VNC server that can have the display data
 * provided from a simple frame buffer, for example. This is used in
 * the bbc_display_vnc to provide a VNC server onto a BBC
 * microcomputer simulation or FPGA implementation using shared
 * memory.
 *
 * The VNC RFB protocol is a lightweight protocol for providing remote
 * visual and keyboard interaction between a client and a server.
 * 
 * The server contains the source display and accepts keyboard/mouse
 * input.  The c_vnc_rfb class provides for a simple server.
 * 
 * The basic interaction is that a client demands 'give me this
 * rectangle now', and the server supplies the rectangle.  The server
 * may not be able to supply the whole rectangle in a single message,
 * so it needs to remember which portion of the client request it has
 * served.
 * 
 * The client may also say 'give me any updates to any region of this
 * rectangle'.  In this case the server supplies any region of the
 * rectangle that changes; it may also supply more of the rectangle
 * that it has not yet supplied to the client based on an original
 * 'give now' request.
 * 
 * It is therefore wise for the server to have a 'rectangle that has
 * been demanded that has not been given yet', plus a set of
 * rectangles of the frame buffer that have been modified that need to
 * be sent if an update is requested.
 * 
 * The operations that are required are then:
 * 
 * 1. If no client is connected and frame buffer is updated, ignore
 * updates.
 * 
 * 2. If client is connected and client demands a rectangle, then that
 * rectangle is set to be the set of rectangles to send, rectangle is
 * set to be the region of interest for the client, and a 'reply
 * expected' is set.
 * 
 * 3. If the client is connected and asks for updates to a rectangle,
 * then that rectangle is set to be the region of interest for the
 * client, and a 'reply expected' is set.
 * 
 * 4. If 'reply expected' is set and the rectangles to send set is not
 * empty, then a portion (or all) of the first rectangle in the set is
 * sent to the client and removed from the set, and 'reply expected'
 * is cleared.
 * 
 * 5. If a rectangle of the frame buffer is updated (committed), and
 * the client is connected, then the rectangle is overlapped with the
 * region of interest for the client. If the overlap is null the
 * commit is ignored, otherwise the commit is added to the set of
 * rectangles to send.
 * 
 * The operation once a VNC RFB client is connected is to receive any
 * message the VNC RFB client, and handle those - possibly (given this
 * is TCP) there may just be partial messages received, so buffer
 * ahead and interpret messages from the buffer.
 *
 * Once all received messages have been interpret (this may be mouse,
 * key, or update request messages) the code may have one (or more)
 * rectangles of its framebuffer to send. Once a rectangle is started
 * to be sent, then incremental update requests from the VNC RFB
 * client don't effect the area to be sent. Rectangle data is only
 * sent if an update request message has been received since the last
 * rectangle was sent. It seems that some VNC RFB clients (if not all)
 * will send may update requests at high rate, so a rectangle should
 * not be returned for each update request. Once the 'rectangle in
 * progress of being sent' has been sent, further invalidated
 * rectangles can be set to be sent if an update request is received.
 *
 * Outline
 *
 *  Might get SetPixelFormat message back.
 *  
 *  receive_message( card8 0, padding 3, pixel format );
 * 
 *  Will get SetEncodings message back.
 *  
 *  receive_message( card8 2, padding 1, card16 number of encodings, card32[] encodings );
 *  encodings are in preference order:
 *      0 raw
 *      1 copy rectangle
 *      2 RRE
 *      4 compact RRE
 *      5 hextile;
 *  raw is always allowed from server, though;
 *     
 *  Will get FramebufferUpdateRequest
 *  
 *  receive_message( card8 3, card8 incremental (1->can use copyrect), card16 xpos, card16 ypos, card16 width, card16 height );
 * 
 *  May get keymessages/pointer/cut text message
 *  
 *  receive_message( card8 4, card8 down-flag, card16 padding, card32 key );
 *  receive_message( card8 5, card8 buttonmask, card16 xpos, card16 ypos );
 *  receive_message( card8 6, card8[3] padding, card32 length, char[] );
 * 
 *  Can send client update messages
 *  
 *  send_message( card8 0, card8 padding, card16 num_rectangles,
 *                card16 xpos, card16 ypos, card16 width, card16 height, card32 encoding, data );
 *  raw is pixel data left-to-right, top-to-bottom;
 *  copy rect is card16 xsrc, card16 ysrc;
 *  rre is card32 num sub rects, card8bpp background pixel value,
 *      (card8bpp value, card16 xpos, card16 ypos, card16 width, card16 height )*;
 * corre is card32 num sub rects, card8bpp background pixel value,
 *      (card8bpp value, card8 xpos, card8 ypos, card8 width, card8 height )*;
 *  hextile is (card8 mask, [card8bpp[256] raw pix] | ([card8bpp bg], [card8bpp fg], [card8 num subrects],
 *              ([card8bpp color], card8 xandy, card8 widthandheight)*))*
 *      where mask is 1->raw, 2->bg, 4->fg, 8->subrects given, 16->subrects colored;
 * 
 *  Can ring bell
 *  
 *  send_message( card8 2 );
 *  send_message( card8 3, card8[3] padding, card32 length, char[] );
 */

/*a Includes */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/select.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <errno.h>

#include "fb.h"
#include "vnc_rfb.h"

/*a Defines */
#define BYTE_OF_CARD(c,b) ( ((c)>>(b*8))&0xff )
#define NAME ("simple_vnc_server")
#define BYTES_PER_PIXEL (1)
#define MIN(a,b) ( ((a)<(b))?(a):(b) )
#define MAX(a,b) ( ((a)>(b))?(a):(b) )

/*a Types */
/*t card32 */
typedef int card32;

/*a VNC message handling */
/*f c_vnc_rfb::vnc_msg_init */
/**
 * Initialize a message structure from a buffer pointer for use with
 * reading and writing
 */
void
c_vnc_rfb::vnc_msg_init(struct t_vnc_rfb_msg *vnc_msg, char *buffer, int length )
{
    vnc_msg->buffer = (unsigned char *)buffer;
    vnc_msg->length = length;
    vnc_msg->offset = 0;
}

/*f c_vnc_rfb::rx_msg_read_card8 */
/**
 * Extract the next single 8-bit cardinal from the RX message
 */
unsigned int
c_vnc_rfb::rx_msg_read_card8(void)
{
    return rx_msg.buffer[rx_msg.offset++];
}

/*f c_vnc_rfb::rx_msg_read_card16 */
/**
 * Extract the next single 16-bit cardinal from the RX message
 */
unsigned int
c_vnc_rfb::rx_msg_read_card16(void)
{
    unsigned int result;
    result = rx_msg.buffer[rx_msg.offset++]<<8;
    result |= rx_msg.buffer[rx_msg.offset++];
    return result;
}

/*f c_vnc_rfb::rx_msg_read_card32 */
/**
 * Extract the next single 32-bit cardinal from the RX message
 */
unsigned int
c_vnc_rfb::rx_msg_read_card32(void)
{
    unsigned int result;
    result = rx_msg.buffer[rx_msg.offset++]<<24;
    result |= rx_msg.buffer[rx_msg.offset++]<<16;
    result |= rx_msg.buffer[rx_msg.offset++]<<8;
    result |= rx_msg.buffer[rx_msg.offset++];
    return result;
}

/*f c_vnc_rfb::tx_msg_add_card8 */
/**
 * Append a single 8-bit cardinal to the TX message
 */
void
c_vnc_rfb::tx_msg_add_card8(int card)
{
    tx_msg.buffer[tx_msg.offset++] = card;
}

/*f c_vnc_rfb::tx_msg_add_card16 */
/**
 * Append a single 16-bit cardinal to the TX message
 */
void
c_vnc_rfb::tx_msg_add_card16(int card)
{
    tx_msg.buffer[tx_msg.offset++] = BYTE_OF_CARD( card, 1 );
    tx_msg.buffer[tx_msg.offset++] = BYTE_OF_CARD( card, 0 );
}

/*f c_vnc_rfb::tx_msg_add_card32 */
/**
 * Append a single 32-bit cardinal to the TX message
 */
void
c_vnc_rfb::tx_msg_add_card32(int card)
{
    tx_msg.buffer[tx_msg.offset++] = BYTE_OF_CARD( card, 3 );
    tx_msg.buffer[tx_msg.offset++] = BYTE_OF_CARD( card, 2 );
    tx_msg.buffer[tx_msg.offset++] = BYTE_OF_CARD( card, 1 );
    tx_msg.buffer[tx_msg.offset++] = BYTE_OF_CARD( card, 0 );
}

/*f c_vnc_rfb::tx_msg_add_le16 */
/**
 * Append a single 16-bit cardinal to the TX message, little-endian
 * Used for little-endian 16bpp pixel data
 */
void
c_vnc_rfb::tx_msg_add_le16(int card)
{
    tx_msg.buffer[tx_msg.offset++] = BYTE_OF_CARD( card, 0 );
    tx_msg.buffer[tx_msg.offset++] = BYTE_OF_CARD( card, 1 );
}

/*f c_vnc_rfb::tx_msg_add_le32 */
/**
 * Append a single 32-bit cardinal to the TX message, little-endian
 * Used for little-endian 32bpp pixel data
 */
void
c_vnc_rfb::tx_msg_add_le32(int card)
{
    tx_msg.buffer[tx_msg.offset++] = BYTE_OF_CARD( card, 0 );
    tx_msg.buffer[tx_msg.offset++] = BYTE_OF_CARD( card, 1 );
    tx_msg.buffer[tx_msg.offset++] = BYTE_OF_CARD( card, 2 );
    tx_msg.buffer[tx_msg.offset++] = BYTE_OF_CARD( card, 3 );
}

/*f c_vnc_rfb::tx_msg_add_padding */
/**
 * Append a quantity of zero padding to the TX message
 */
void
c_vnc_rfb::tx_msg_add_padding(int padding)
{
    int i;
    for (i=0; i<padding; i++) {
        tx_msg.buffer[tx_msg.offset++] = 0;
    }
}

/*f c_vnc_rfb::tx_msg_add_buffer */
/**
 * Append a buffer string to the TX message
 */
void
c_vnc_rfb::tx_msg_add_buffer(const void *data, int length)
{
    int i;
    for (i=0; i<length; i++) {
        tx_msg.buffer[tx_msg.offset++] = ((unsigned char *)data)[i];
    }
}

/*f c_vnc_rfb::tx_msg_add_pixel */
/**
 * Append a pixel from the framebuffer at (x,y) to the TX message
 */
void
c_vnc_rfb::tx_msg_add_pixel(int x, int y)
{
    unsigned int p, r, g, b;
    p = FB_GET_PIXEL(fb->fb,x+y*fb->width);
    r = FB_RED_VALUE(fb,p);
    g = FB_GREEN_VALUE(fb,p);
    b = FB_BLUE_VALUE(fb,p);
    p = ((r>>reddownshift)<<redshift) |
        ((g>>greendownshift)<<greenshift) |
        ((b>>bluedownshift)<<blueshift) ;
    if (bpp_on_wire==32) {
        if (bigendian) {
            tx_msg_add_card32(p);
        } else {
            tx_msg_add_le32(p);
        }
    } else if (bpp_on_wire==16) {
        if (bigendian) {
            tx_msg_add_card16(p);
        } else {
            tx_msg_add_le16(p);
        }
    } else if (bpp_on_wire==8) {
        tx_msg_add_card8(p);
    }
}

/*a Socket handling */
/*f socket_listen */
/**
 * Create, bind and listen on a socket
 *
 * @param port    Port number to open on any of the IP addresses of the host
 *
 * @returns -1 for failure, 0 for success
 *
 */
static int
socket_listen(int port)
{
    struct sockaddr_in socket_inet_addr;
    int skt;
    int i;
    
    /*b Create socket */
    socket_inet_addr.sin_family = AF_INET;
    socket_inet_addr.sin_port = htons( port );
    socket_inet_addr.sin_addr.s_addr = htonl( INADDR_ANY );
    skt = socket( PF_INET, SOCK_STREAM, 0 );
    if (skt<0)
        return -1;

    /*b Bind socket */
    i = 1;
    setsockopt( skt, SOL_SOCKET, SO_REUSEADDR, (void *)&i, 4 );
    i = bind( skt, (struct sockaddr *)&socket_inet_addr, sizeof(socket_inet_addr ));
    if (i)
        return -1;

    /*b Listen on socket */
    i = listen(skt, 1);
    if (i)
        return -1;
    return skt;
}

/*f socket_accept */
/**
 * Accept a client socket from a 'public' socket that is listening
 *
 * @param skt       'Public' socket that is listening, that returns readable in its FD_SET
 *
 * @returns -1 for failure, client socket number for success
 *
 */
static int
socket_accept(int skt)
{
    struct sockaddr_in client_address;
    int accept_skt;
    socklen_t i;
    
    /*b Accept socket */
    i = sizeof(client_address);
    accept_skt = accept( skt, (struct sockaddr *)&client_address, &i ); // returns -1 for error
    //printf("accept returns %d\n", accept_skt );
    return accept_skt;
}

/*f socket_send_bl */
/**
 * Send a buffer of a specified length to a socket, without blocking
 *
 * @param skt       Socket to send data to
 * @param buffer    Start of buffer to send
 * @param length    Length of buffer to send
 *
 * @returns 0 for success, 1 otherwise
 *
 */
static int
socket_send_bl(int skt, const char *buffer, int length)
{
    int i;
    //for (int j=0; j<length && j<20; j++) fprintf(stderr, "%02x ", buffer[j] );
    i = send(skt, buffer, length, MSG_DONTWAIT);
    //fprintf(stderr, "Write returns %d of %d\n", i, length );
    return (i!=length);
}
/*f socket_send */
/**
 * Send a null-terminated buffer to a socket, without blocking
 *
 * @param skt       Socket to send data to
 * @param buffer    Start of buffer to send
 *
 * @returns 0 for success, 1 otherwise
 *
 */
static int
socket_send(int skt, const char *buffer)
{
    return socket_send_bl(skt, buffer, strlen(buffer) );
}

/*f socket_receive */
/**
 * Receive data from a socket into a buffer of a certain length
 *
 * @param skt       Socket to receive data from
 * @param buffer    Start of buffer to receive into
 * @param length    Length of buffer (to not be overrun)
 *
 * @returns -1 for error (socket closed, for example), else number of bytes received (possibly 0)
 *
 */
static int
socket_receive(int skt, char *buffer, int length)
{
    int i;
    i = recv( skt, buffer, length, 0 );
    //printf("Read returns %d\n", i );
    return i;
}

/*a VNC RFB protocol handling support functions
 */
/*f c_vnc_rfb::tx_msg_send */
void
c_vnc_rfb::tx_msg_send(void)
{
    socket_send_bl(client_socket, (char *)tx_msg.buffer, tx_msg.offset);
}

/*f c_vnc_rfb::handle_set_pixel_format
  Message should be card8 0, 3 card8 padding, then char[16] pixel format; expect length>=20, therefore
 */
int
c_vnc_rfb::handle_set_pixel_format(void)
{
    if (rx_msg.length<20) { return 0; }
    if (verbose) fprintf(stderr,"vnc_rfb_handle_set_pixel_format:Got message %d long\n", rx_msg.length);
    if (verbose) fprintf(stderr,"vnc_rfb_handle_set_pixel_format:Check header\n" );
    if (rx_msg_read_card8()!=0) { return -1; }
    rx_msg_read_card8();
    rx_msg_read_card8();
    rx_msg_read_card8();
    bpp_on_wire = rx_msg_read_card8();
    depth = rx_msg_read_card8();
    bigendian = rx_msg_read_card8();
    truecolor = rx_msg_read_card8();
    redmax = rx_msg_read_card16();
    greenmax = rx_msg_read_card16();
    bluemax = rx_msg_read_card16();
    redshift = rx_msg_read_card8();
    greenshift = rx_msg_read_card8();
    blueshift = rx_msg_read_card8();
    reddownshift = 0;
    greendownshift = 0;
    bluedownshift = 0;
    if (verbose) {
        fprintf(stderr, "vnc_rfb_handle_set_pixel_format:bpp %d depth %d bigendian %d truecolor %d redmax %04x greenmax %04x bluemax %04x redshift %d greenshift %d blueshift %d\n",
                bpp_on_wire,
                depth,
                bigendian,
                truecolor,
                redmax,
                greenmax,
                bluemax,
                redshift,
                greenshift,
                blueshift );
    }
    return 20;
}

/*f vnc_rfb_handle_set_encodings
  Message should be card8 2, padding 1, card16 number of encodings, card32[] encodings; expect at least length 4, then check number of encodings
 */
int
c_vnc_rfb::handle_set_encodings(void)
{
    int i, n;

    if (rx_msg.length<4) { return 0; }

    if (verbose) fprintf(stderr,"vnc_rfb_handle_set_encodings:Got message %d long\n", rx_msg.length);
    if (verbose) fprintf(stderr,"vnc_rfb_handle_set_encodings:Check header\n" );
    if (rx_msg_read_card8()!=2) { return -1; }
    rx_msg_read_card8();
    n = rx_msg_read_card16();
    if (rx_msg.length<n*4+4) { return 0; }
    allowed_encodings = 1;
    for (i=0; i<n; i++) {
        allowed_encodings |= 1<<rx_msg_read_card32();
    }
    if (verbose) fprintf(stderr,"vnc_rfb_handle_set_encodings:Allowed encodings now %08x\n", allowed_encodings );
    return n*4+4;
}

/*f vnc_rfb_handle_frame_buffer_update_request
  This message is sent regularly, and if 'incremental' is clear then the specified rectangle should be sent, else only changes should be sent.
  Message should be card8 3, card8 incremental (1->can use copyrect), card16 xpos, card16 ypos, card16 width, card16 height; expect at least 10, therefore
 */
int
c_vnc_rfb::handle_frame_buffer_update_request(void)
{
    int incr, x, y, w, h;

    if (rx_msg.length<10) { return 0; }
    if (verbose) fprintf(stderr,"vnc_rfb_handle_frame_buffer_update_request:Check header\n" );
    if (rx_msg_read_card8()!=3) {
        return -1;
    }
    incr = rx_msg_read_card8();
    x = rx_msg_read_card16();
    y = rx_msg_read_card16();
    w = rx_msg_read_card16();
    h = rx_msg_read_card16();
    y = fb->height-1-y-h;
    if (verbose) fprintf(stderr,"vnc_rfb_handle_frame_buffer_update_request:Incr %d x %d y %d w %d h %d\n", incr, x, y, w, h );
    if (incr) {
        int force_update = 0;
        if (!client_interest.valid) { force_update=1; }
        if ((client_interest.lx!=x) ||
            (client_interest.by!=y) ||
            (client_interest.rx!=x+w) ||
            (client_interest.ty!=y+h)) { force_update=1; }
        client_interest.valid = 1;
        client_interest.lx = x;
        client_interest.by = y;
        client_interest.rx = x+w;
        client_interest.ty = y+h;
        if (0 && force_update) {
            fb_add_to_rects( fb, rects_to_send, MAX_RECT, x, y, x+w, y+h );
        }
    } else {
        client_interest.valid = 0;
        fb_clear_rects( fb, rects_to_send, MAX_RECT );
        fb_add_to_rects( fb, rects_to_send, MAX_RECT, x, y, x+w, y+h );
    }
    rectangle_expected = 1;
    need_to_send = fb_any_rect_valid( fb, rects_to_send, MAX_RECT );
    fprintf(stderr,"u%d",need_to_send);
    return 10;
}

/*f vnc_rfb_handle_callback_requests
  Message should be card8 4, card8 down-flag, card16 padding, card32 key for key message
  Message should be card8 5, card8 buttonmask, card16 xpos, card16 ypos for button message
  Message should be card8 6, 3 card8 padding, card32 length, card[] for cut text message
 */
int
c_vnc_rfb::handle_callback_requests(void)
{
    int reason;
    if (verbose) fprintf(stderr,"vnc_rfb_handle_callback_requests:Got message %d long\n", rx_msg.length);
    reason = rx_msg_read_card8();
    if (reason==4) { 
        int down = rx_msg_read_card8();
        (void) rx_msg_read_card16(); // skip padding
        int key = rx_msg_read_card32();
        if (key_fn) {key_fn(this,down,key);}
        return 8;
    }
    if (reason==5) {
        int buttons = rx_msg_read_card8();
        int x = rx_msg_read_card16();
        int y = rx_msg_read_card16();
        if (mouse_fn) {mouse_fn(this,buttons,x,y);}
        return 6;
    }
    return -1;
}

/*f vnc_rfb_handle_protocol */
int
c_vnc_rfb::handle_protocol(void)
{
    /*b Receive protocol name and send authentication requirement */
    if (rx_msg.length<12) return 0;
    fprintf(stderr,"Client protocol:");
    for (int i=0; i<12; i++) {
        fprintf(stderr, "%c", rx_msg.buffer[i]);
    }
    fprintf(stderr, "\n");

    if (0) { //version==308) {
        tx_msg_add_card8(1); // 1 authentication type
        tx_msg_add_card8(1); // 1 -> no authentication
        tx_msg_send();
        skt_state = vnc_rfb_skt_state_await_client_security_choice;
    } else { // 303
        // 303 does not negotiate security, it dictates
        tx_msg_add_card32(1); // 1 for security type
        tx_msg_send();
        skt_state = vnc_rfb_skt_state_await_client_exclusivity;
    }
    return 12;
}

/*f c_vnc_rfb::handle_security_choice */
int
c_vnc_rfb::handle_security_choice(void)
{
    /*b Security result message - okay (card32 of 0) */
    tx_msg_add_card32(0);
    tx_msg_send();
    skt_state = vnc_rfb_skt_state_await_client_exclusivity;
    return 1;
}

/*f c_vnc_rfb::handle_exclusivity */
int
c_vnc_rfb::handle_exclusivity(void)
{
    /*b Receive ClientInit = exclusivity (0->exclusive, nonzero leave other clients up,
      send server initialisation (pixel format included) message */
    tx_msg_add_card16(fb->width );
    tx_msg_add_card16(fb->height );
    tx_msg_add_card8(32 ); // bpp_on_wire
    tx_msg_add_card8(24 ); // depth
    tx_msg_add_card8(1 ); // bigendian pixel data
    tx_msg_add_card8(1 ) ; // truecolor
    tx_msg_add_card16(0xff ); // redmax = 0xff, 8 bits
    tx_msg_add_card16(0xff ); // greenmax = 0xff, 8 bits
    tx_msg_add_card16(0xff ); // bluemax = 0xff, 8 bits
    tx_msg_add_card8(16 ); // redshift - top 16 bits are red
    tx_msg_add_card8(8 ); // greenshift - next 8 bits are green
    tx_msg_add_card8(0 ); // blueshift - next 0 bits are blue
    tx_msg_add_padding(3 );
    tx_msg_add_card32(strlen(NAME) );
    tx_msg_add_buffer(NAME, strlen(NAME) );
    tx_msg_send();
    skt_state = vnc_rfb_skt_state_running;
    return 1;
}

/*f c_vnc_rfb::handle_receive_buffer */
int
c_vnc_rfb::handle_receive_buffer(void)
{
    char *rx_msg_start;
    int rx_msg_length;
    int bytes_consumed;

    /*b Check buffer is basically okay */
    rx_msg_length = rx_buffer_length - rx_buffer_pos;
    rx_msg_start  = rx_buffer + rx_buffer_pos;
    if (rx_msg_length<1) return 0;
    if (verbose) {
        fprintf(stderr, "Rx message buffer:");
        for (int i=0; i<rx_msg_length; i++) {
            fprintf(stderr, "%02x ",((unsigned char *)rx_msg_start)[i]);
        }
        fprintf(stderr, "\n");
    }

    vnc_msg_init(&rx_msg, rx_msg_start, rx_msg_length);
    vnc_msg_init(&tx_msg, tx_buffer, sizeof(tx_buffer) );

    /*b Handle client state machine, and process the start of the buffer (hopefully) */
    switch (skt_state) {
    case vnc_rfb_skt_state_not_connected:
        return -1;
    case vnc_rfb_skt_state_await_protocol_name:
        bytes_consumed = handle_protocol();
        break;
    case vnc_rfb_skt_state_await_client_security_choice:
        bytes_consumed = handle_security_choice();
        break;
    case vnc_rfb_skt_state_await_client_exclusivity:
        bytes_consumed = handle_exclusivity();
        break;
    case vnc_rfb_skt_state_running:
        /*b Receive various messages - frame buffer update request, keys pressed, etc */
        // rectangle_expected = 0;
        switch (rx_msg.buffer[0]) {
        case 0:
            bytes_consumed = handle_set_pixel_format();
            break;
        case 2:
            bytes_consumed = handle_set_encodings();
            break;
        case 3:
            bytes_consumed = handle_frame_buffer_update_request();
            break;
        case 4: // key down
        case 5: // mouse change
        case 6: // cut text
            bytes_consumed = handle_callback_requests();
            break;
        }
        break;
    }
    /*b Consume the bytes */
    if (verbose) { fprintf(stderr, "Consumed %d bytes\n",bytes_consumed); }
    if (bytes_consumed<0) return -1;
    rx_buffer_pos += bytes_consumed;

    /*b Shuffle the buffer back if necessary to allow room for next message too */
    if (rx_buffer_pos>0) {
        rx_buffer_length -= rx_buffer_pos;
        if (rx_buffer_length>0) {
            memmove(rx_buffer, rx_buffer+rx_buffer_pos, rx_buffer_length);
        }
        rx_buffer_pos = 0;
    }

    /*b All done */
    return bytes_consumed;
}

/*f c_vnc_rfb::send_first_rectangle
  Run through rectangles to send, and send as much as possible (from the bottom up) of the first rectangle to send,
  and reduce the rectangle by the amount sent.
 */
void
c_vnc_rfb::send_first_rectangle(void)
{
    int i, j;
    int w, h;
    t_fb_rectangle *rect;

    need_to_send = 0;
    fprintf(stderr,"s");
    if (!rect_being_sent.valid) {
        for (i=0; i<MAX_RECT; i++) {
            rect = &(rects_to_send[i]);
            if (verbose) { fprintf(stderr, "Check rectangle to send %d is valid (%d)\n", i, rect->valid ); }
            if (rect->valid) {
                rect_being_sent = *rect;
                rect_being_sent.ty--; // Chicken of the VNC breaks if this is not here.
                rect->valid = 0;
                break;
            }
        }
    }
    if (!rect_being_sent.valid) {
        return;
    }

    int sending_all;
    rectangle_expected = 0;

    /*b Send rectangle in RAW (for now); at least, send up to BUFFER_SIZE-HDR pixels, and reduce rectangle size appropriately */
    w = rect_being_sent.rx-rect_being_sent.lx;
    h = rect_being_sent.ty-rect_being_sent.by;
    sending_all = 1;
    vnc_msg_init(&tx_msg, tx_buffer, sizeof(tx_buffer) );
    if ((w*h*bpp_on_wire/8)>(tx_msg.length-160)) {
        h = (tx_msg.length-160)/(bpp_on_wire/8)/w;
        sending_all = 0;
    }
    if (h<=0) {
        fprintf(stderr, "vnc_rfb_send_first_rectangle:BUFFER NOT BIG ENOUGH FOR 1 ROW OF RECTANGLE LX %d RX %d!\n", rect_being_sent.lx, rect_being_sent.rx );
        rect_being_sent.valid = 0;
    }
    tx_msg_add_card8(0 ); // Message type 0 - frame buffer update
    tx_msg_add_padding(1 ); // Padding
    tx_msg_add_card16(1 ); // Num rectangles
    tx_msg_add_card16(rect_being_sent.lx ); // Xpos
    tx_msg_add_card16(fb->height-1-rect_being_sent.by-h ); // Ypos
    tx_msg_add_card16(w ); // Width
    tx_msg_add_card16(h ); // Height
    tx_msg_add_card32(0 ); // Raw encoding
    for (i=0; i<h; i++) {
        for (j=0; j<w; j++) {
            tx_msg_add_pixel(j+rect_being_sent.lx, rect_being_sent.by+h-1-i );
        }
    }
    tx_msg_send();
    if (verbose) fprintf(stderr, "vnc_rfb_send_first_rectangle:Sent rectangle (%d,%d) to (%d,%d) (all:%d)\n", rect_being_sent.lx, rect_being_sent.by, rect_being_sent.lx+w, rect_being_sent.by+h, sending_all );
    rect_being_sent.by+=h;
    if (sending_all) {
        rect_being_sent.valid = 0;
    }
}

/*f c_vnc_rfb::receive_data */
int
c_vnc_rfb::receive_data(void)
{
    int i = socket_receive( client_socket, rx_buffer+rx_buffer_length, sizeof(rx_buffer)-rx_buffer_length );
    if (i<=0) return -1;
    rx_buffer_length += i;
    return i;
}

/*a Public VNC RFB methods */
/*f c_vnc_rfb::c_vnc_rfb */
/**
 * Constructor for the c_vnc_rfb class
 *
 * @param port      Public port to listen on for connections to the VNC RFB server
 * @param fb        Framebuffer object with width, height, fb (data) and rects_invalid
 *
 */
c_vnc_rfb::c_vnc_rfb(int port, t_fb *fb)
{
    /*b Clear to default values */
    this->fb = fb;
    public_socket = -1;
    client_socket = -1;
    skt_state = vnc_rfb_skt_state_not_connected;
    allowed_encodings = 0;
    bpp_on_wire = 0;
    depth = 0;
    bigendian = 0;
    truecolor = 0;
    redmax = 0xff;
    greenmax = 0xff;
    bluemax = 0xff;
    redshift = 0;
    greenshift = 0;
    blueshift = 0;
    reddownshift = 0;
    greendownshift = 0;
    bluedownshift = 0;
    need_to_send = 0;
    rectangle_expected = 0;
    client_interest.valid = 0;
    rx_buffer_pos = 0;
    rx_buffer_length = 0;
    fb_clear_rects( fb, rects_to_send, MAX_RECT );
    verbose = 0;
    mouse_fn = NULL;
    key_fn = NULL;
    handle = NULL;

    /*b Listen on public socket */
    public_socket = socket_listen( port );
    if (public_socket<0) {
        fprintf(stderr, "Failed to get public socket %d\n", public_socket);
        return;
    }

    fprintf(stderr, "Public socket %d\n", public_socket);
}

/*f c_vnc_rfb::~c_vnc_rfb */
/**
 * Denstructor for the c_vnc_rfb class
 *
 * Closes any sockets that are open
 *
 */
c_vnc_rfb::~c_vnc_rfb()
{
    if (verbose) fprintf(stderr, "Exiting cleanly\n");
    if (client_socket>=0) {
        if (verbose) fprintf(stderr, "Close client socket %d\n", client_socket);
        close(client_socket);
        client_socket = -1;
    }
    if (public_socket>=0) {
        if (verbose) fprintf(stderr, "Close public socket %d\n", public_socket);
        close(public_socket);
        public_socket = -1;
    }
}

/*f c_vnc_rfb::commit */
/**
 * Commit updates that are in the frame buffers 'rects_invalid' list
 * to be sent to the VNC RFB client, if there is one.
 *
 * Normally the rectangles in the framebuffer will have been marked as
 * invalid with an fb_add_to_rects call to the fb->rects_invalid
 * array.
 *
 * If a VNC RFB client has not registered incremental interest in a
 * rectangle, then the commit is ignored. If one has been registered,
 * then run through all the invalid FB rectangles and overlap those
 * with the client interest rectangle, and add those to the rectangles
 * to send
 */
void
c_vnc_rfb::commit(void)
{
    /*b Test if client has registered an interest - if not, then ignore the commit */
    if (!client_interest.valid) {
        if (verbose) { fprintf(stderr, "Commit of rectangle, but client has not registered interest in any area\n"); }
        return;
    }

    /*b Run through the frame-buffers updated rectangles, overlap with client interest, and
     add the overlapping rectangle to the rectangles to send */
    for (int i=0; i<MAX_RECT; i++) {
        if (fb->rects_invalid[i].valid) {
            fb->rects_invalid[i].valid = 0;
            if (fb_rectangle_overlaps_r_r( &(fb->rects_invalid[i]), &client_interest)) {
                fb_add_to_rects( fb, rects_to_send,
                                 MAX_RECT,
                                 fb->rects_invalid[i].lx,
                                 fb->rects_invalid[i].by,
                                 fb->rects_invalid[i].rx,
                                 fb->rects_invalid[i].ty );
                fprintf(stderr,"c");
                need_to_send = rectangle_expected;
            }
        }
    }
}

/*f c_vnc_rfb::poll*/
/**
 * Poll for a new client, or for messages from a client, or to send if the client socket
 * can transmit and there are rectangles to send.
 *
 * @param  ms_timeout   Number of milliseconds to wait for receive data if nothing needs to be done
 *
 * @return 1 if something was handled, 0 if timed out
 *
 * A regular usage would be to poll with a timeout, and if the timeout
 * occurs (0 returned) then perhaps update the framebuffer and then
 * commit invalid rectangles.
 */
int
c_vnc_rfb::poll(int ms_timeout )
{
    fd_set readfds, writefds, exceptfds;
    struct timeval timeout;
    int i, max;
    int something_done;

    /*b Handle any received data from VNC RFB client */
    while (skt_state != vnc_rfb_skt_state_not_connected) {
        int r=handle_receive_buffer();
        if (r<0) {
            close(client_socket);
            client_socket = -1;
            fprintf(stderr, "Protocol error, dropping client\n");
            break;
        }
        if (r==0) break;
    }

    /*b Prepare to poll for receive data, exceptions, and ability to write (if data is to be sent) */
    FD_ZERO(&readfds);
    FD_ZERO(&writefds);
    FD_ZERO(&exceptfds);

    max = -1;
    if (client_socket<0) {
        skip_timeout_count = 0;
    } else {
        FD_SET( client_socket, &readfds);
        FD_SET( client_socket, &exceptfds);
        max = client_socket;
        if ((skt_state==vnc_rfb_skt_state_running) && (need_to_send)) {
            FD_SET( client_socket, &writefds);
        }
    }
    FD_SET( public_socket, &readfds);
    if (public_socket>max) {
        max = public_socket;
    }

    /*b Poll with timeout - return 0 if timeout occurs */
    //fprintf(stderr,"Rx state %d %d %d %d %d %d\n", client_socket, skt_state, skip_timeout_count, rx_buffer_length, rx_buffer_pos, need_to_send);
    if (skip_timeout_count>0) {
        timeout.tv_sec  = 0;
        timeout.tv_usec = 0;
        skip_timeout_count--;
        i = select(max+1, &readfds, &writefds, &exceptfds, &timeout);
        //if (i<=0) return 1;
    } else {
        timeout.tv_sec = ms_timeout/1000;
        timeout.tv_usec = (ms_timeout%1000)*1000;
        i = select(max+1, &readfds, &writefds, &exceptfds, &timeout);
        if (i<=0) {
            //fprintf(stderr,"timeout or error\n");
            return 0;
        }
    }
    
    //for (int j=0; j<max+1; j++) {
    //fprintf(stderr, "%d: R%d W%d X%d\n", j, FD_ISSET( j, &readfds ), FD_ISSET( j, &writefds ), FD_ISSET( j, &exceptfds ) );
    //}

    /*b Handle public socket interactions */
    something_done = 0;
    if (FD_ISSET( public_socket, &readfds)) {
        if (client_socket>=0) {
            close(client_socket);
            client_socket = -1;
            fprintf(stderr, "New client to replace current client, so closing current client\n");
        }
        // do accept?
        client_socket = socket_accept( public_socket );
        if (client_socket>=0) {
            fprintf(stderr, "Accepting new client\n");
            rx_buffer_pos = 0;
            rx_buffer_length = 0;
            rectangle_expected = 0;
            need_to_send = 0;
            socket_send( client_socket, "RFB 003.003\n" );
        }
        skt_state = vnc_rfb_skt_state_await_protocol_name;
        something_done = 1;
    }

    /*b Handle client socket interactions */
    if (!something_done && (client_socket>=0)) {
        //fprintf(stderr,"Accepting client data or sending\n");
        if (FD_ISSET( client_socket, &readfds)) {
            if (receive_data()<0) {
                close(client_socket);
                client_socket = -1;
                fprintf(stderr, "Client killed socket, so closing\n");
                return 1;
            }
        }
        if (FD_ISSET( client_socket, &writefds)) {
            if (need_to_send) {
                send_first_rectangle();
                something_done = 1;
            }
        }
        if (FD_ISSET( client_socket, &exceptfds)) {
            // close it?
            close(client_socket);
            client_socket = -1;
            client_interest.valid = 0;
            something_done = 1;
            fprintf(stderr, "Exception on client socket, so closing\n");
        }
        //fprintf(stderr,"Rx has %d.%d bytes\n",rx_buffer_length,rx_buffer_pos);
        if (rx_buffer_length!=rx_buffer_pos) {
            //skip_timeout_count = 10;
        }
    }

    /*b All done - return indicating stuff was done */
    return 1;
}

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/

