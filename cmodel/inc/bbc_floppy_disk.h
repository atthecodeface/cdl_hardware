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
 * @file   bbc_floppy_disk.h
 * @brief  BBC floppy disk model for use with bbc_floppy.cpp
 *
 * Header file for BBC floppy disk model.
 *
 */

/*a Wrapper */
#ifndef __INC_BBC_FLOPPY_DISK
#define __INC_BBC_FLOPPY_DISK

/*a Types */
/*t c_bbc_floppy_disk */
/**
 * This class was used to model a floppy disk before the floppy sram
 * drive model was created.
 */
class c_bbc_floppy_disk {
public:
    c_bbc_floppy_disk(void);
    ~c_bbc_floppy_disk(void);
    int sector_bytes(int track, int sector);
    void empty_disk(void);
    int load_disk(const char *disk_filename, int disk_type, int write_protect);
    int format_disk(int max_tracks, int max_sectors_per_track, int bytes_per_track);
    int format_track(int track, struct t_track_data *track_data);
    void validate_track_sector(int *track, int *sector);
    int get_sector_id(int track, int sector, t_bbc_floppy_sector_id *sector_id);
    void write_sector_id(int track, int sector, t_bbc_floppy_sector_id *sector_id); /* Write the id of the current sector id to the data provided */
    unsigned char *get_track_data(int track);
    unsigned char *get_sector_data(int track, int sector);
    int write_data(int track, int sector, const unsigned char *sector_data, int offset, int byte_count);
    int read_data(int track, int sector, unsigned char *sector_data, int offset, int byte_count);
    void step_track(int step_up);
    void next_sector(void);

    int verbose;
    int ready; // if 0, then the rest is invalid
    int write_protected;
    int max_tracks;
    int max_sectors_per_track;
    int number_of_tracks;
    int current_track;
    int current_sector;
    int sector_data_offset;
    struct t_track_data *tracks;
    unsigned char *disk_data;
};

/*a Wrapper */
#endif

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
