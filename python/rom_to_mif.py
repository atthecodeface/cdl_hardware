#!/usr/bin/env python
def convert_rom(rom_filename):
    in_file  = open("roms/"+rom_filename)
    out_file =  open("roms/"+rom_filename+".mif", "w")
    address = 0
    r = "%04x: "%address    
    while True:
        ch = in_file.read(1)
        if len(ch)==0: break
        r += "%02x "%ord(ch)
        address = address+1
        if (address%32)==0:
            print >>out_file, r
            r = "%04x: "%address    
            pass
        pass
    in_file.close()
    out_file.close()
    pass
for rom_filename in ("basic2.rom", "dfs.rom", "os12.rom"):
    convert_rom(rom_filename)
    pass
