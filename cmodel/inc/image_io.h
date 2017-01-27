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
 * @file   image_io.h
 * @brief  Image input/output library header file
 *
 * Header file for simple image input and output, supporting PNG and
 * JPEG (using libpng and libjpeg). This supports both an image class,
 * and functions for just reading and writing image data.
 *
 */

/*a Wrapper */
#ifndef __INC_IMAGE_IO
#define __INC_IMAGE_IO

/*a Types */
/*t c_image_io */
/**
 * This class supports reading and writing images as either PNG or
 * JPEG files.
 */
class c_image_io
{
    /** Private data is allocated by the class instance at
     * construction, if required; its contents are opaque **/
    struct prvt_data *prvt;
    int read_init(FILE *f);
    int read_set_rgb8(void);
    int read_alloc(void);
    int read_image(void);
    void read_finalize(void);
    int write_init(FILE *f);
    int write_image(void);
    int write_finalize(void);
    void free_image_data(void);

public:
    c_image_io(void);
    ~c_image_io(void);
    int jpeg_read(FILE *f);
    int png_read(FILE *f);
    int png_write(FILE *f);
 
    /** Pointer to the image data **/
    unsigned char *image_data;
    /** Width of the image in pixels **/
    unsigned int width;    
    /** Height of the image in pixels **/
    unsigned int height;
    /** Number of bytes per pixel **/
    int byte_width;
    /** Number of bits per pixel **/
    int bit_depth;
    /** Unclear what this is **/
    int color_type;

    /** If set, then 'image_data' will be free'd when the class instance is destroyed **/
    int free_image_data_on_destruction;
};

/*a External functions */
extern int image_write_rgba(const char *filename, const unsigned char *image_data, int width, int height);
extern unsigned char *image_read_rgba(const char *filename, int *width, int *height);

/*a Wrapper */
#endif

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
