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
 * @file   bbc_floppy_disk.cpp
 * @brief  BBC floppy disk class methods
 *
 * Code for the BBC floppy disk class, which is used by
 * bbc_floppy.cpp; this is no longer used in the simulation, as
 * instead a CDL model 'bbc_floppy_sram' maps the FDC floppy interface
 * to an SRAM interface.
 *
 * The code here creates an arbitrary floppy disk, which can have any
 * number of tracks, a different number of sectors per track, and
 * individual sectors may be of different length. All that is really
 * needed is a fixed format disk with 256 byte sectors, ten sectors
 * per track, and from 40 to 85 tracks (possibly double-sided).
 */
/*a Includes */
#include "be_model_includes.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "bbc_floppy.h"
#include "bbc_floppy_disk.h"

/*a Types for floppy disk */
/*t t_sector_data */
/**
 * These are initially configured by 'format_disk'; contents are written in 'format_track'
 */
typedef struct t_sector_data {
    t_bbc_floppy_sector_id sector_id; // Written by 'format_disk' - not a malloc'ed buffer
    int data_offset; // Written by 'format_track' - offset from start of track data to the data for the sector
} t_sector_data;

/*t t_track_data */
/**
 *  These are initially configured by 'format_disk'; contents are written in 'format_track'
 */
typedef struct t_track_data {
    int number_sectors;          // Written by 'format_disk'
    int track_data_offset;       // Written by 'format_disk' - Offset in to 'disk_data' of data for track
    t_sector_data *sector_datas; // Written by 'format_disk' - not a malloc'ed buffer
} t_track_data;

/*a Statics */
static int sector_byte_length[8]={128,256,512,1024,2048,4096,8192,16384};

/*a Methods for c_bbc_floppy_disk */
/*f c_bbc_floppy_disk::c_bbc_floppy_disk */
c_bbc_floppy_disk::c_bbc_floppy_disk(void)
{
    verbose = 1;
    ready = 0;
    write_protected = 0;
    number_of_tracks = 0;
    tracks = NULL;
    disk_data = NULL;
    sector_data_offset = 0;
}

/*f c_bbc_floppy_disk::~c_bbc_floppy_disk */
c_bbc_floppy_disk::~c_bbc_floppy_disk()
{
    empty_disk();
}

/*f c_bbc_floppy_disk::sector_bytes */
int c_bbc_floppy_disk::sector_bytes(int track, int sector)
{
    return sector_byte_length[tracks[track].sector_datas[sector].sector_id.sector_length&3];
}

/*f c_bbc_floppy_disk::empty_disk */
void
c_bbc_floppy_disk::empty_disk(void)
{
    if (verbose) {
        fprintf(stderr, "Empty disk\n");
    }
    if (!ready) return;
    if (tracks) {
        free(tracks);
        tracks = NULL;
    }
    if (disk_data) {
        free(disk_data);
        disk_data = NULL;
    }
    ready = 0;
}

/*f c_bbc_floppy_disk::format_disk */
int c_bbc_floppy_disk::format_disk(int max_tracks, int max_sectors_per_track, int bytes_per_track)
{
    t_sector_data *sectors;
    int track_data_size = sizeof(t_track_data)*max_tracks;
    int data_size       = track_data_size + max_tracks*max_sectors_per_track*sizeof(t_sector_data);

    if (verbose) {
        fprintf(stderr, "Formatting disk with tracks %d sectors %d bytes per TRACK %d\n",
                max_tracks,
                max_sectors_per_track,
                bytes_per_track);
    }
    tracks = (t_track_data *)malloc(data_size);
    this->max_tracks = max_tracks;
    this->max_sectors_per_track = max_sectors_per_track;
    if (!tracks) return -1;
    disk_data = (unsigned char *)malloc(max_tracks*bytes_per_track);
    current_track = 0;
    if (!disk_data) {
        free(tracks);
        tracks = NULL;
        return -1;
    }

    memset(tracks,0,data_size);

    sectors = (t_sector_data *)&tracks[max_tracks];
    for (int t=0; t<max_tracks; t++) {
        tracks[t].sector_datas      = sectors + t*max_sectors_per_track;
        tracks[t].track_data_offset = t*bytes_per_track;
    }
    ready = 1;
    return 0;
}

/*f c_bbc_floppy_disk::format_track */
int c_bbc_floppy_disk::format_track(int track, t_track_data *track_data)
{
    int sector_data_offset;
    if (track>=0) {
        current_track = track;
    }
    if (current_track>=max_tracks) {
        current_track = max_tracks-1;
    }
    if (verbose) {
        fprintf(stderr, "Formatting track %d sectors %d\n",
                track,
                track_data->number_sectors);
    }
    if (track_data->number_sectors > max_sectors_per_track) {
        return -1;
    }
    current_sector = 0;
    sector_data_offset = 0;
    tracks[current_track].number_sectors = track_data->number_sectors;
    for (int s=0; s<track_data->number_sectors; s++) {
        tracks[current_track].sector_datas[s].data_offset = sector_data_offset;
        tracks[current_track].sector_datas[s].sector_id = track_data->sector_datas[s].sector_id;
        sector_data_offset += sector_byte_length[track_data->sector_datas[s].sector_id.sector_length];
    }
    return 0;
}

/*f c_bbc_floppy_disk::validate_track_sector */
void c_bbc_floppy_disk::validate_track_sector(int *track, int *sector)
{
    if (track) {
        if (*track<0) { *track=current_track; }
        if (*track>=max_tracks) {*track=max_tracks-1;}
    }
    if (sector) {
        if (*sector<0) { *sector=current_sector; }
        if (*sector>=tracks[*track].number_sectors) { *sector=0; }
    }
}

/*f c_bbc_floppy_disk::step_track */
void c_bbc_floppy_disk::step_track(int step_up)
{
    validate_track_sector(&current_track, NULL);
    current_track += step_up;
    if (current_track<0) { current_track=0; }
    validate_track_sector(&current_track, &current_sector);
    if (verbose) { fprintf(stderr, "Stepped to track %d of %d\n", current_track, max_tracks); }
}

/*f c_bbc_floppy_disk::get_track_data */
unsigned char *c_bbc_floppy_disk::get_track_data(int track)
{
    if (!disk_data) return NULL;
    if (!tracks) return NULL;
    validate_track_sector(&track, NULL);
    return disk_data + tracks[track].track_data_offset;
}

/*f c_bbc_floppy_disk::get_sector_data */
unsigned char *c_bbc_floppy_disk::get_sector_data(int track, int sector)
{
    validate_track_sector(&track, &sector);
    if (!disk_data) return NULL;
    if (!tracks) return NULL;
    return disk_data + tracks[track].track_data_offset + tracks[track].sector_datas[sector].data_offset;
}

/*f c_bbc_floppy_disk::next_sector */
void c_bbc_floppy_disk::next_sector(void)
{
    validate_track_sector(&current_track, &current_sector);
    current_sector += 1;
    if (current_sector<0) { current_sector += tracks[current_track].number_sectors; }
    validate_track_sector(&current_track, &current_sector);
    sector_data_offset = 0;
}

/*f c_bbc_floppy_disk::write_sector_id */
void c_bbc_floppy_disk::write_sector_id(int track, int sector, t_bbc_floppy_sector_id *sector_id)
{
    validate_track_sector(&track, &sector);
    if (verbose) { fprintf(stderr, "Write sector id %d.%d\n", track, sector); }
    tracks[track].sector_datas[sector].sector_id = *sector_id;
    sector_data_offset = 0;
}

/*f c_bbc_floppy_disk::get_sector_id */
int c_bbc_floppy_disk::get_sector_id(int track, int sector, t_bbc_floppy_sector_id *sector_id)
{
    validate_track_sector(&track, &sector);
    if (verbose) { fprintf(stderr, "Get sector id %d.%d\n", track, sector); }
    *sector_id = tracks[track].sector_datas[sector].sector_id;
    sector_data_offset = 0;
    return 0;
}

/*f c_bbc_floppy_disk::write_data */
int c_bbc_floppy_disk::write_data(int track, int sector, const unsigned char *sector_data, int offset, int byte_count)
{
    unsigned char *disk_sector_data;
    validate_track_sector(&track, &sector);
    if (offset<0) {offset = sector_data_offset;}
    if ((offset<0) || (offset+byte_count>sector_bytes(track,sector))) return -2;
    disk_sector_data = get_sector_data(track, sector);
    if (verbose) { fprintf(stderr, "Write data %d.%d : %p\n", track, sector, disk_sector_data); }
    if (!disk_sector_data) return -1;
    sector_data_offset = offset+byte_count;
    memcpy(disk_sector_data, sector_data, byte_count);
    return 0;
}

/*f c_bbc_floppy_disk::read_data */
int c_bbc_floppy_disk::read_data(int track, int sector, unsigned char *sector_data, int offset, int byte_count)
{
    unsigned char *disk_sector_data;
    validate_track_sector(&track, &sector);
    if (offset<0) {offset = sector_data_offset;}
    if ((offset<0) || (offset+byte_count>sector_bytes(track,sector))) return -2;
    disk_sector_data = get_sector_data(track, sector);
    if (!disk_sector_data) return -1;
    sector_data_offset = offset+byte_count;
    if (verbose>5) { fprintf(stderr, "Read data %d.%d %d : %p\n", track, sector, offset, disk_sector_data+offset); }
    memcpy(sector_data, disk_sector_data+offset, byte_count);
    return 0;
}

/*f c_bbc_floppy_disk::load_disk */
// BBC default type of disk is 100kB for SS SD, 40 tracks, i.e. 2.5kB per track
// That is 10 sectors of 256B
int c_bbc_floppy_disk::load_disk(const char *filename, int disk_type, int write_protect)
{
    FILE *f;
    int file_size;
    int num_tracks;
    int sectors_per_track;
    int bytes_per_sector;
    unsigned char sector_data[2048];
    t_track_data track_data;
    t_sector_data sector_datas[32];

    if (verbose) {
        fprintf(stderr, "Loading disk with filename '%s'\n",
                filename);
    }
    empty_disk();
    write_protected = write_protect;
    f = fopen(filename,"r");
    if (!f) {
        fprintf(stderr, "Failed to open disk file '%s'\n", filename);
        return -1;
    }
    fseek(f, 0, SEEK_END);
    file_size = ftell(f);
    fseek(f, 0, SEEK_SET);
    bytes_per_sector = 256;
    sectors_per_track = 10;
    num_tracks = 40;
    if (disk_type<1) {
        bytes_per_sector = 256;
        sectors_per_track = 10;
        num_tracks = (file_size/(bytes_per_sector*sectors_per_track))+1;
    }
    fprintf(stderr,"Formatting to %d/%d/%d/%d\n",file_size, num_tracks, sectors_per_track, bytes_per_sector);
    track_data.number_sectors = sectors_per_track;
    track_data.sector_datas = sector_datas;
    if (format_disk(num_tracks, sectors_per_track, bytes_per_sector*sectors_per_track)) {
        empty_disk();
        return -3;
    }
    for (int t=0; t<num_tracks; t++) {
        if (verbose) { fprintf(stderr,"Load disk track %d\n",t); }
        for (int s=0; s<sectors_per_track; s++) {
            sector_datas[s].sector_id.track = t;
            sector_datas[s].sector_id.head = 0;
            sector_datas[s].sector_id.sector_number = s;
            sector_datas[s].sector_id.sector_length = 1; // 256 :-)
            sector_datas[s].sector_id.bad_crc = 0;
            sector_datas[s].sector_id.bad_data_crc = 0;
            sector_datas[s].sector_id.deleted_data = 0;
        }
        format_track(t, &track_data); // should move to sector id 0
        for (int s=0; s<sectors_per_track; s++) {
            if (fread( sector_data, bytes_per_sector, 1, f)!=1) {
                break; // Can have a partial last track
            }
            write_sector_id(-1, s, &sector_datas[s].sector_id);
            write_data(-1, -1, sector_data, 0, bytes_per_sector);
            next_sector();
        }
    }
    fclose(f);
    return 0;
}

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/
