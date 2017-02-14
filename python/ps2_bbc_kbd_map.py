import ps2
import bbc_kbd
import copy

bbc_std_remappings = ( (":", "'"),
                       ("~", "`"),
                       ("_", "="),
                       ("Copy", "Alt (right)"),
                       ("Delete", "Backspace"),
                       ("@", "Home"),
                       )
ps2_double_mappings = ( ("KP0", "0",),
                        ("KP1", "1"),
                        ("KP2", "2"),
                        ("KP3", "3"),
                        ("KP4", "4"),
                        ("KP5", "5"),
                        ("KP6", "6"),
                        ("KP7", "7"),
                        ("KP8", "8"),
                        ("KP9", "9"),
                        ("KP.", "."),
                        ("Delete", "Backspace"),
                        ("Insert", "Alt (right)",),
                        ("KPEnter", "Enter"),
                        ("RtShift", "Shift"),
                        ("Ctrl (right)", "Ctrl" ),
                        #("Windows (left)", ),
                        #("Alt (left)", ),
                        #("Page Down", ),
                        #("KP+", ),
                        #("KP*", ),
                        #("Page Up", ),
                        #("KP-", ),
                        #("KP/", ),
                        #("Windows (right)", ),
                        #("F11", ),
                        #("Home", ),
                        )

# bbc_code_of_key is (bbc symbol => standard symbol)
bbc_code_of_key = bbc_kbd.bbc_code_of_key
for (bbc_sym,std_sym) in bbc_std_remappings:
    bbc_code_of_key[std_sym] = bbc_code_of_key[bbc_sym]
    del bbc_code_of_key[bbc_sym]
    pass

rom_key_map = copy.copy(ps2.ps2_key_map)
remove_list = []
rom_keys  = rom_key_map.keys()
rom_key_codes = {}
# rom_key_codes is (standard symbol => rom address)
# rom_key_map   is (address => standard symbol)
for k in rom_keys:
    sym = rom_key_map[k]
    if k>0xff:
        rom_key_map[0x80+(k&0x7f)] = sym
        rom_key_codes[sym] = 0x80+(k&0x7f)
        del rom_key_map[k]
    elif k>0x7f:
        print "Remapping key '%s' from %d to 0x7f (should be at most one of these)"%(sym,k)
        rom_key_map[0x7f] = sym
        rom_key_codes[sym] = 0x7f
        del rom_key_map[k]
        pass
    else:
        rom_key_codes[sym] = k
        pass
    pass

unmapped_ps2_keys = set()
unmapped_bbc_keys = copy.copy(bbc_code_of_key)
# bbc_of_std_keys is (standard symbol => bbc code)
bbc_of_std_keys = {}
for k in rom_key_map:
    sym = rom_key_map[k]
    if sym not in bbc_code_of_key:
        unmapped_ps2_keys.add( sym )
        pass
    else:
        bbc_code = bbc_code_of_key[sym]
        bbc_of_std_keys[sym] = bbc_code
        if sym in unmapped_bbc_keys:
            del unmapped_bbc_keys[sym]
            pass
        pass
    pass

for (ps2_sym, bbc_sym) in ps2_double_mappings:
    if ps2_sym not in unmapped_ps2_keys:
        print "Attempt to use ps2 symbol '%s' in double mapping, but it is already used"%ps2_sym
        pass
    else:
        unmapped_ps2_keys.remove(ps2_sym)
        if bbc_sym not in bbc_code_of_key:
            raise Exception("Double mapping of ps2 symbol '%s' to unknown BBC symbol '%s'"%(ps2_sym,bbc_sym))
        bbc_of_std_keys[rom_key_map[rom_key_codes[ps2_sym]]] = bbc_code_of_key[bbc_sym]
        pass
    pass
    
if len(unmapped_bbc_keys)>0:
    print "WARNING: Unmapped BBC keys:"
    for sym in unmapped_bbc_keys:
        print sym
        pass
    pass

if True:
    print "INFO: Unused ps2 keys"
    for sym in unmapped_ps2_keys:
        print sym
        pass
    pass

if False:
    print "INFO: BBC of standard keys"
    for sym in bbc_of_std_keys:
        print sym, bbc_of_std_keys[sym]
        pass
    pass

def bit_data(text):
    rows = text.split(" ")
    while len(rows)<9:
        rows.append(".....")
        pass
    rows.reverse()
    data = 0
    for ch in "".join(rows):
        data = data<<1
        if ch=="*": data |= 1
        pass
    return data

# bbc_code_of_key is (bbc symbol => standard symbol)
# bbc_of_std_keys is (standard symbol => bbc code)
# rom_key_codes   is (standard symbol => rom address)
# rom_key_map     is (address => standard symbol)
mif_file = open("roms/ps2_bbc_kbd.mif", "w")
for k in rom_key_map:
    sym = rom_key_map[k]
    if sym in bbc_code_of_key:
        (col, row) = bbc_code_of_key[sym]
        value = col*8+row
        print >>mif_file, "%02x: %02x"%(k, value)
        pass
    #in range(len(font_rom_characters)):
    #ch = font_rom_characters[i]
    #ch_text = font[ch]
    #data = bit_data(ch_text)
    #print "%02x: %016x"%(i,data)
    pass
mif_file.close()





