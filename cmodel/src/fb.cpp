/** Copyright (C) 2004-2017,  Gavin J Stark.  All rights reserved.
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
 * @file   fb.cpp
 * @brief  Frame buffer code
 *
 * Code for creating and drawing within a simple frame buffer,
 * originally written for the Embisi GIP project.
 *
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

/*a Defines */
#define FB_BOUNDLX(rfb,x) {if ((x)<0)(x)=0;}
#define FB_BOUNDRX(rfb,x) {if ((x)>(rfb)->width) (x)=(rfb)->width;}
#define FB_BOUNDBY(rfb,y) {if ((y)<0)(y)=0;}
#define FB_BOUNDTY(rfb,y) {if ((y)>(rfb)->height) (y)=(rfb)->height;}
#define FONT_HASH (0)
#define FONT_WIDTH_TABLE (4)
#define FONT_HEIGHT_TABLE (4+16)
#define FONT_ASCENT_TABLE (4+16+16)
#define FONT_SHIFT_CHAR (4+16+16+16+0)
#define FONT_FIRST_CHAR (4+16+16+16+1)
#define FONT_LAST_CHAR (4+16+16+16+2)
#define FONT_GROUP_DATA (4+16+16+16+4)
#define FONT_DATA_BIT(f,b,p) (((f)[(b)+((p)>>3)]>>((p)&7))&1)
#define MIN(a,b) ( ((a)<(b))?(a):(b) )
#define MAX(a,b) ( ((a)>(b))?(a):(b) )
#define FB_SET_PIXEL(fb,o,p) {(fb)[o]=p;}
#define FB_ROW(y) ((y)>>8)
#define FB_COL(x) ((x)>>8)

/*a Rectangle support functions
 */
extern int fb_any_rect_valid( t_fb *fb, t_fb_rectangle *rects, int max)
{
    for (int i=0; i<max; i++)
        if (rects[i].valid)
            return 1;
    return 0;
}

/*f fb_clear_rects
  Clear the rectangle list
 */
extern void fb_clear_rects( t_fb *fb, t_fb_rectangle *rects, int max )
{
    for (int i=0; i<max; i++)
        rects[i].valid=0;
}

/*f fb_add_to_rects
  Add to a rectangles list, using pixel coordinates.
  If this rectangle overlaps with another, then remove that one and add one that is the union of them both
  If the list is full, then merge this with the first one (should probably be the one that makes the total area smallest)
 */
extern void fb_add_to_rects( t_fb *fb, t_fb_rectangle *rects, int max, int lx, int by, int rx, int ty )
{
    int i;

    /*b Bound the rectangle, and return if it is zero size
     */
    FB_BOUNDLX( fb, lx );
    FB_BOUNDRX( fb, rx );
    FB_BOUNDBY( fb, by );
    FB_BOUNDTY( fb, ty );
    if ((lx>=rx) || (by>=ty))
    {
        return;
    }

    /*b Find an overlap if one exists, and add the union, then return
     */
    for (i=0; i<max; i++)
    {
        if (rects[i].valid)
        {
            if (fb_rectangle_overlaps_r_c( &(rects[i]), lx, by, rx, ty ))
            {
                rects[i].valid = 0;
                fb_add_to_rects( fb, rects, max, MIN(rects[i].lx,lx), MIN(rects[i].by,by), MAX(rects[i].rx,rx), MAX(rects[i].ty,ty) );
                return;
            }
        }
    }

    /*b No overlap; find an empty slot if one exists, and add it there
     */
    for (i=0; i<max; i++)
    {
        if (!rects[i].valid)
        {
            rects[i].valid = 1;
            rects[i].lx = lx;
            rects[i].by = by;
            rects[i].rx = rx;
            rects[i].ty = ty;
            return;
        }
    }

    /*b No overlap, no slots available - merge with first rectangle
     */
    rects[0].lx = MIN(rects[0].lx,lx);
    rects[0].by = MIN(rects[0].by,by);
    rects[0].rx = MAX(rects[0].rx,rx);
    rects[0].ty = MAX(rects[0].ty,ty);
}

/*a External FB functions
 */
/*f fb_init
 */
extern t_fb *fb_init( int width, int height, int bpp )
{
    t_fb *fb;
    int i;

    if (bpp!=8)
        return NULL;

    fb = (t_fb *)malloc(sizeof(t_fb)+width*height*bpp/8);

    fb->bpp = bpp;
    fb->width = width;
    fb->height = height;
    for (i=0; i<FB_MAX_RECT; i++)
    {
        fb->rects_invalid[i].valid = 0;
    }
    fb->color = 0;
    fb->font_list = NULL;
    fb->font = NULL;
    fb->fb = ((unsigned char *)fb) + sizeof(t_fb);
    return fb;
}

/*f fb_exit
 */
extern void fb_exit( t_fb *fb )
{
    t_fb_font *font, *next_font;
    for (font=fb->font_list;font;font=next_font)
    {
        next_font = font->next_in_list;
        free(font);
    }
    free(fb);
}

/*a Font and color handling
 */
/*f fb_add_font
  Add a new font to our list
 */
extern int fb_add_font( t_fb *fb, unsigned char *font_data )
{
    t_fb_font *font;
    font = (t_fb_font *)malloc(sizeof(t_fb_font));
    if (!font)
        return 0;
    font->data = font_data;
    font->next_in_list = fb->font_list;
    fb->font_list = font;
    return 1;
}

/*f fb_set_color( color )
  Set color
 */
extern int fb_set_color( t_fb *fb, int color )
{
    fb->color = color;
    return color;
}

/*f fb_set_color_rgb( r, g, b )
  Set color from r/g/b, return color
 */
extern int fb_set_color_rgb( t_fb *fb, int r, int g, int b )
{
    fb->color = ( (((r>>5)&7)) | 
                  (((g>>5)&7)<<3) |             
                  (((b>>6)&3)<<6) );
    return fb->color;
}

/*f fb_set_font( font data ptr )
 */
extern unsigned char *fb_set_font( t_fb *fb, unsigned char *font_data )
{
    fb->font = font_data;
    return fb->font;
}

/*f fb_set_font_fn( font name )
 */
extern unsigned char *fb_set_font_fn( t_fb *fb, const char *font_name )
{
    t_fb_font *font;
    unsigned char hash[5];
    int i, j;

    for (i=0; i<4; i++) hash[i] = 0;
    for (i=0; font_name[i]; i++)
    {
        for (j=4; j>0; j--) hash[j]=hash[j-1];
        hash[0] = ((hash[4]>>3)&0x1f) ^ ((hash[4]&0x07)<<5) ^ font_name[i];
    }
    for (font=fb->font_list; font; font=font->next_in_list)
    {
        if (((int *)hash)[0]==((int *)font->data)[0])
        {
            fb->font = font->data;
            return fb->font;
        }
    }
    return NULL;
}

/*a Graphics FB functions
 */
/*f fb_clear
 */
extern void fb_clear( t_fb *fb )
{
    int i, color;
    color = fb->color;

    for (i=0; i<fb->width*fb->height; i++)
    {
        FB_SET_PIXEL(fb->fb,i,color);
    }
    fb_add_to_rects( fb, fb->rects_invalid, FB_MAX_RECT, 0, 0, fb->width, fb->height );
}

/*f fb_rectangle
 */
extern void fb_rectangle( t_fb *fb, int x, int y, int w, int h )
{
    int i, j;
    int color;
    color = fb->color;

    w = FB_COL(x+w);
    h = FB_ROW(y+h);
    x = FB_COL(x);
    y = FB_ROW(y);
    FB_BOUNDLX( fb, x );
    FB_BOUNDRX( fb, w );
    FB_BOUNDBY( fb, y );
    FB_BOUNDTY( fb, h );
    for (j=y; j<h; j++)
    {
        for (i=x; i<w; i++)
        {
            FB_SET_PIXEL( fb->fb,i+j*fb->width, color);
        }
    }
    fb_add_to_rects( fb, fb->rects_invalid, FB_MAX_RECT, x, y, w, h );
}

/*f fb_rectangle
 */
extern void
fb_copy_rectangle( t_fb *fb, int dst_lx, int dst_by, unsigned char *src, int src_w, int src_h, t_fb_rectangle *r, int vertical_flip )
{
    int src_lx, src_by, src_rx, src_ty;
    int dst_rx, dst_ty;

    src_lx = r->lx;
    src_rx = r->rx;
    src_by = r->by;
    src_ty = r->ty;
    if (src_lx<0)     { dst_lx-=src_lx; src_lx=0; }
    if (src_by<0)     { dst_by-=src_by; src_by=0; }
    if (dst_lx<0)     { src_lx-=dst_lx; dst_lx=0; }
    if (dst_by<0)     { src_by-=dst_by; dst_by=0; }
    if (src_rx>src_w) { src_rx=src_w; }
    if (src_ty>src_h) { src_ty=src_h; }
    dst_rx = dst_lx + src_rx-src_lx;
    dst_ty = dst_by + src_ty-src_by;
    if (dst_rx>fb->width)  { src_rx-=dst_rx-fb->width;  dst_rx=fb->width; }
    if (dst_ty>fb->height) { src_ty-=dst_ty-fb->height; dst_ty=fb->height; }

    int dst_y = dst_by;
    if (vertical_flip) {dst_y=dst_ty-1;}
    for (int src_y=src_by; src_y<src_ty; src_y++) {
        int dst_x = dst_lx;
        for (int src_x=src_lx; src_x<src_rx; src_x++, dst_x++) {
            unsigned int rgb;
            unsigned int p;
            rgb = ((unsigned int *)src)[src_x+src_w*src_y];
            p = ((rgb&0xff)?7:0) | (((rgb>>8)&0xff)?0x38:0) | (((rgb>>16)&0xff)?0xc0:0);
            fb->fb[dst_y*fb->width+dst_x] = p;
        }
        if (vertical_flip) {dst_y--;} else {dst_y++;}
    }
    //fprintf(stderr,"Invalidating rectangle %d,%d %d,%d\n",dst_lx, dst_by, dst_rx-dst_lx, dst_ty-dst_by);
    fb_add_to_rects(fb, fb->rects_invalid, FB_MAX_RECT, dst_lx, dst_by, dst_rx-dst_lx, dst_ty-dst_by);
}

/*f fb_get_char_data
 */
static int fb_get_char_data( t_fb *fb, int c, int *cw, int *ch, int *cl, int *ca, int *bitmap_offset )
{
    int shift, group, group_data, ch_data, bo;

    if (!fb->font)
        return 0;

    if (c>=fb->font[FONT_LAST_CHAR])
        return 0;
    c = c-fb->font[FONT_FIRST_CHAR];
    if (c<0)
        return 0;

    shift = fb->font[FONT_SHIFT_CHAR];
    group = c>>shift;
    c = c&~(group<<shift);

    group_data = FONT_GROUP_DATA+group*(2+(3<<shift));
    ch_data = group_data + 2+3*c;

    bo = fb->font[ group_data ] | (fb->font[ group_data+1 ]<<8); 

    *ch = fb->font[FONT_HEIGHT_TABLE+(fb->font[ch_data]&0xf)];
    *cw = fb->font[FONT_WIDTH_TABLE+((fb->font[ch_data]>>4)&0xf)];
    *ca = fb->font[FONT_ASCENT_TABLE+(fb->font[ch_data+1]&0xf)]-128;
    *cl = fb->font[FONT_ASCENT_TABLE+((fb->font[ch_data+1]>>4)&0xf)]-128;
    *bitmap_offset = bo + fb->font[ ch_data+2 ];

    //printf("Char %d/%d (s %d); %02x %02x %02x: %dx%d a %d l %d offset %04x\n", group, c, shift, fb->font[ch_data], fb->font[ch_data+1], fb->font[ch_data+2], cw, ch, ca-128, cl-128, bitmap_offset );
    return 1;
}

/*f fb_put_char
 */
extern void fb_put_char( t_fb *fb, int x, int y, int c )
{
    int i, j, ch, cw, ca, cl;
    int bitmap_offset;
    int color;

    color = fb->color;
    if (!fb_get_char_data( fb, c, &cw, &ch, &cl, &ca, &bitmap_offset ))
        return;

    x = FB_COL(x)+cl;
    y = FB_ROW(y)+ca;
    for (j=0; j<ch; j++)
    {
        if (y+j<0)
            continue;
        if (y+j>fb->height)
            break;
        for (i=0; i<cw; i++)
        {
            if (x+i<0)
                continue;
            if (x+i>fb->width)
                break;
            //printf("%d:%d:%02x..",j*cw+i,FONT_DATA_BIT(font, bitmap_offset, j*cw+i),fb->font[bitmap_offset]);
            if (FONT_DATA_BIT(fb->font, bitmap_offset, j*cw+i))
            {
                FB_SET_PIXEL( fb->fb,(x+i)+(y+j)*fb->width, color);
            }
        }
    }
    fb_add_to_rects( fb, fb->rects_invalid, FB_MAX_RECT, x, y, x+cw, y+ch );
}

/*f fb_put_string
 */
extern void fb_put_string( t_fb *fb, int x, int y, char *string )
{
    int i, ch, cw, ca, cl, bitmap_offset;

    for (i=0; string[i]; i++)
    {
        if (fb_get_char_data( fb, string[i], &cw, &ch, &cl, &ca, &bitmap_offset ))
        {
            fb_put_char( fb, x, y, string[i] );
            x += 256*(cw+1);
        }
    }
}


/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/

