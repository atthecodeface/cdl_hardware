#!/usr/bin/env python
# VGA  640x480 @ 60Hz: 25.175MHz clk 640+16+ 96+48 = 800  480+10+2+33 = 525
# VGA  800x600 @ 60Hz: 40MHz clk     800+40+128+88 =1076  600+ 1+4+23 = 628
class timing:
    front_porch = None
    strobe_width = None
    back_porch = None
    display_size = None
    active_high = False
    pass
    def __init__(self, front_porch, strobe_width, back_porch, display_size, active_high):
        self.front_porch = front_porch
        self.strobe_width  = strobe_width
        self.back_porch  = back_porch
        self.display_size = display_size
        self.active_high = active_high
        self.total = front_porch + strobe_width + back_porch + display_size
        pass
    def porch_csr(self):
        fp = self.front_porch
        bp = self.back_porch + self.strobe_width
        return (fp<<16) | (bp<<0)
    def strobe_csr(self):
        pol = 0
        if self.active_high: pol = 1
        return (pol<<15) | self.strobe_width
    def display_csr(self):
        return self.display_size
    
class config(object): # New style so it has __subclasses__
    name = None
    pixel_clock = None
    horizontal = None
    vertical = None
    freq = None
    def __init__(self):
        self.name = self.__class__.__name__
        horiz_freq = self.pixel_clock / self.horizontal.total * 1000. # in kHz
        vert_freq  = horiz_freq       / self.vertical.total * 1000. # in Hz
        freq_err = abs(vert_freq - self.freq)
        if (freq_err / self.freq) > 0.01:
            raise Exception("%s: More than 1%% error in vertical frame rate (evaluated %s, specifed as %s)"%(self.name, str(vert_freq), str(self.freq)))
        pass
    def framebuffer_timing(self):
        csrs = {}
        csrs["display_size"] = self.horizontal.display_csr() | ( self.vertical.display_csr()<<16)
        csrs["strobes"]      = self.horizontal.strobe_csr()  | ( self.vertical.strobe_csr()<<16)
        csrs["h_porch"]      = self.horizontal.porch_csr()
        csrs["v_porch"]      = self.vertical.porch_csr()
        return csrs
    pass

#class lcd_480x272p60:
#    pixel_clock = 25.175

class vga_640x480p60(config):
    pixel_clock = 25.175
    horizontal = timing(16, 96, 48, 640, False)
    vertical   = timing(10,  2, 33, 480, False)
    freq = 60.

class lcd_800x480p60(config):
    pixel_clock = 40.000
    horizontal = timing(210, 20, 26, 800, False)
    vertical   = timing( 23,  1, 21, 480, False)
    freq = 72.

class svga_800x600p60(config):
    pixel_clock = 40.000
    horizontal = timing(40, 128, 88, 800, True)
    vertical   = timing( 1,   4, 23, 600, True)
    freq = 60.

class hd_1280x720p60(config): # 1280p
    pixel_clock = 74.240
    horizontal = timing(110, 40, 220, 1280, True)
    vertical   = timing(  5,  5,  20,  720, True)
    freq = 60.

class hd_1920x1080p60(config): # "2k"
    pixel_clock = 148.5
    horizontal = timing( 88, 44, 148, 1920, True)
    vertical   = timing(  4,  5,  36, 1080, True)
    freq = 60.

configs = {}
for c in config.__subclasses__():
    c = c()
    configs[c.name] = c
    pass

csrs = configs["vga_640x480p60"].framebuffer_timing()
csrs = configs["hd_1920x1080p60"].framebuffer_timing()
#csrs = configs["svga_800x600p60"].framebuffer_timing()
#print csrs
for (cn,cv) in csrs.iteritems():
    print "%s:%08x"%(cn,cv)
    pass
