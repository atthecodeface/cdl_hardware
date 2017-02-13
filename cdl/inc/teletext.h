/*t t_teletext_vertical_interpolation */
typedef enum[2] {
    tvi_all_scanlines  "For twenty scanline output characters",
    tvi_even_scanlines "Only output scanlines 0, 2, 4, ... 18 - for even interlace fields, or for 10-scanline displays",
    tvi_odd_scanlines  "For twenty scanline output characters, but only outputing scanlines 1, 3, 5, ... 19 - for odd interlace fields",
} t_teletext_vertical_interpolation;

/*t t_teletext_timings */
typedef struct {
    bit restart_frame          "Asserted if restarting the frame (resets all teletext character state)";
    bit end_of_scanline        "Asserted if end of scanline";
    bit first_scanline_of_row  "Asserted if first scanline of row; not required if module's internal timing is trusted";
    bit smoothe                "Asserted if interpolation is desired";
    t_teletext_vertical_interpolation interpolate_vertical   "Asserted if vertical interpolation is desired";
} t_teletext_timings;

/*t t_teletext_character */
typedef struct {
    bit    valid;
    bit[7] character;
} t_teletext_character;

/*t t_teletext_rom_access */
typedef struct {
    bit    select;
    bit[7] address;
} t_teletext_rom_access;

/*t t_teletext_pixels */
typedef struct {
    bit valid         "Asserted to indicate that the red, green and blue are valid; asserted three ticks after a valid character in";
    bit[12] red;
    bit[12] green;
    bit[12] blue;
    bit last_scanline "Asserted with a pixel to indicate it is on the last scanline of the row";
} t_teletext_pixels;

/*a Modules */
/*m teletext */
extern module teletext( clock clk     "Character clock",
                        input bit reset_n,
                        input t_teletext_character    character  "Parallel character data in, with valid signal",
                        input t_teletext_timings      timings    "Timings for the scanline, row, etc",
                        output t_teletext_rom_access  rom_access "Teletext ROM access",
                        input bit[45]                 rom_data   "Teletext ROM data, valid in cycle after rom_access",
                        output t_teletext_pixels pixels       "Output pixels, two clock ticks delayed from clk in"
    )
{
    timing to   rising clock clk character, timings;
    timing from rising clock clk rom_access;
    timing to   rising clock clk rom_data;
    timing from rising clock clk pixels;
}
