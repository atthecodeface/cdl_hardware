typedef struct {
    bit valid;
    bit last;
    bit[8] red;
    bit[8] green;
    bit[8] blue;
} t_led_ws2812_data;

typedef struct {
    bit ready          "Active high signal indicating if LED data is required; ignore if the data is currently valid";
    bit first          "If requesting LED data, then the first LED of the stream should be provided; indicates led_number is 0";
    bit[8] led_number  "Number of LED data required, in case an array is used by the client";
} t_led_ws2812_request;

extern module led_ws2812_chain( clock clk                   "system clock - not the pin clock",
                                input bit    reset_n  "async reset",
                                input bit[8] divider_400ns  "clock divider value to provide for generating a pulse every 400ns based on clk",
                                output t_led_ws2812_request led_request  "LED data request",
                                input t_led_ws2812_data     led_data     "LED data, for the requested led",
                                output bit led_data_pin                  "Data in pin for LED chain"
    )
{
    timing to   rising clock clk  divider_400ns, led_data;
    timing from rising clock clk  led_request, led_data_pin;
}
