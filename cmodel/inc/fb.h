/** Copyright (C) 2003-2017,  Gavin J Stark.  All rights reserved.
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
 * @file   fb.h
 * @brief  Frame buffer header file
 *
 * Header file for simple frame buffer code, such as for bitmap fonts
 * and managing rectangular areas.
 *
 * This code was originally written for a simple VNC server for the
 * Embisi 'gip' project.
 *
 */

/*a Wrapper */
#ifndef __INC_FB
#define __INC_FB

/*a Defines */
#define FB_MAX_RECT (4)
#define fb_rectangle_overlaps_r_c(r,lx,by,rx,ty) (((r)->lx<(rx))&&((r)->rx>=(lx))&&((r)->by<=(ty))&&((r)->ty>=(by)))
#define fb_rectangle_overlaps_r_r(r,r_b) (((r)->lx<(r_b)->rx)&&((r)->rx>=(r_b)->lx)&&((r)->by<=(r_b)->ty)&&((r)->ty>=(r_b)->by))
#define FB_GET_PIXEL(fb,o) ((fb)[o])
#define FB_RED_VALUE(fb,p) (((p)&0x7)<<5)
#define FB_GREEN_VALUE(fb,p) (((p)&0x38)<<2)
#define FB_BLUE_VALUE(fb,p) (((p)&0xc0)<<0)

/*a Types */
/*t t_fb_rectangle */
/**
 * A simple validated rectangle with inclusive pixel coordinates.
 *
 * If valid is zero, then the remaining entries are undefined.
 */
typedef struct t_fb_rectangle
{
    int valid;
    int lx;
    int by;
    int rx;
    int ty;
} t_fb_rectangle;

/*t t_fb_font */
/**
 * A simple font list structure
 */
typedef struct t_fb_font
{
    struct t_fb_font *next_in_list;
    unsigned char *data;
} t_fb_font;

/*t t_fb */
/**
 * A framebuffer descriptor with width, height, and invalidated regions.
 *
 * The data for the framebuffer is available through the 'fb' element.
 */
typedef struct t_fb
{
    int width; // width in pixels
    int height; // height in pixels
    int bpp; // bits-per-pixel; currently must be 8
    int color; // foreground color, set through functions calls below
    t_fb_rectangle rects_invalid[FB_MAX_RECT]; // List of rectangles that are invalid as they have been written to
    t_fb_font *font_list; // List of fonts
    unsigned char *font; // Font to get characters from for text; this is an array of unsigned chars that is unpicked internally
    unsigned char *fb;
} t_fb;

/*a External functions */
extern void fb_clear_rects( t_fb *fb, t_fb_rectangle *rects, int max );
extern void fb_add_to_rects( t_fb *fb, t_fb_rectangle *rects, int max, int lx, int by, int rx, int ty );
extern int fb_any_rect_valid( t_fb *fb, t_fb_rectangle *rects, int max);
extern t_fb *fb_init( int width, int height, int bpp );
extern void fb_exit( t_fb *fb );
extern int fb_add_font( t_fb *fb, unsigned char *font_data ); // add a new font
extern int fb_set_color( t_fb *fb, int color ); // returns color
extern int fb_set_color_rgb( t_fb *fb, int r, int g, int b ); // returns color for future calls
extern unsigned char *fb_set_font( t_fb *fb, unsigned char *font_data ); // select a font
extern unsigned char *fb_set_font_fn( t_fb *fb, const char *font_data ); // select a font from a name, return ptr
extern void fb_clear( t_fb *fb ); // clear all to color
extern void fb_rectangle( t_fb *fb,int x, int y, int w, int h ); // draw rectangle
extern void fb_put_char( t_fb *fb, int x, int y, int c ); // put a character from the current font, bottom left at (x,y)
extern void fb_put_string( t_fb *fb, int x, int y, char *string ); // put a string of characters from the current font, bottom left at (x,y)
extern void fb_copy_rectangle( t_fb *fb, int x, int y, unsigned char *src, int src_w, int src_h, t_fb_rectangle *r, int vertical_flip ); // copy rectangle

/*a Wrapper */
#endif

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
