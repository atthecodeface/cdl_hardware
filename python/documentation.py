#!/usr/bin/env python
#a Documentation
"""
 :   0      1      2      3      4      5      6      7      8      9      a      b      c      d      e      f
0:  BRK   ORAIX   DIE   ASOIX   SKB   ORAZ   ASLZ   ASOZ    PHP   ORA#   ASLA   ANC#    RDW   ORAM   ASLM   ASOM      
1:  BPL   ORAIY   DIE   ASOIY   SKB   ORAZX  ASLZX  ASOZX   CLC   ORAMY   NOP   ASOMY   RDW   ORAMX  ASLMX  ASOMX
2:  JSR   ANDIX   DIE   RLAIX  BITZ   ANDZ   ROLZ   RLAZ    PLP   AND#   ROLA   ANC#    BITM  ANDM   ROLM   RLAM      
3:  BMI   ANDIY   DIE   RLAIY   SKB   ANDZX  ROLZX  RLAZX   SEC   ANDMY   NOP   RLAMY   RDW   ANDMX  ROLMX  RLAMX      
4:  RTI   EORIX   DIE   LSEIX   SKB   EORZ   LSRZ   LSEZ    PHA   EOR#   LSRA   ALR#    JMP   EORM   LSRM   LSEM      
5:  BVC   EORIY   DIE   LSEIY   SKB   EORZX  LSRZX  LSEZX   CLI   EORMY   NOP   LSEMY   RDW   EORMX  LSRMX  LSEMX      
6:  RTS   ADCIX   DIE   RRAIX   SKB   ADCZ   RORZ   RRAZ    PLA   ADC#   RORA   ARR#    JMPI  ADCM   RORM   RRAM      
7:  BVS   ADCIY   DIE   RRAIY   SKB   ADCZX  RORZX  RRAZX   SEI   ADCMY   NOP   RRAMY   RDW   ADCMX  RORMX  RRAMX      
8:  SKB   STAIX   SKB   SAXIX  STYZ   STAZ   STXZ   SAXZ    DEY    SKB    TXA   XAA#    STYM  STAM   STXM   SAXM      
9:  BCC   STAIY   DIE   AXAIY  STYZX  STAZX  STXZY  SAXZY   TYA   STAMY   TXS                 STAMX         AXAMY          
a: LDY#   LDAIX  LDX#   LAXIX  LDYZ   LDAZ   LDXZ   LAXZ    TAY   LDA#    TAX   OAL#    LDYM  LDAM   LDXM   LAXM      
b:  BCS   LDAIY   DIE   LAXIY  LDYZX  LDAZX  LDXZY  LAXZX   CLV   LDAMY   TSX   LASMY   LDYMX LDAMX  LDXMY  LAXMY
c: CPY#   CMPIX   SKB   DCMIX  CPYZ   CMPZ   DECZ   DCMZ    INY   CMP#    DEX   ASX#    CPYM  CMPM   DECM   DCMM      
d:  BNE   CMPIY   DIE   DCMIY   SKB   CMPZX  DECZX  DCMZX   CLD   CMPMY   NOP   DCMMY   RDW   CMPMX  DECMX  DCMMX
e: CPX#   SBCIX   SKB   INSIX  CPXZ   SBCZ   INCZ   INSZ    INX   SBC#    NOP   S?BC#   CPXM  SBCM   INCM   INSM      
f:  BEQ   SBCIY   DIE   INSIY   SKB   SBCZX  INCZX  INSZX   SED   SBCMY   NOP   INSMY   RDW   SBCMX  INCMX  INSMX


Reordered
 :   0      4      8      c      1      5      9      d      2      6      a      e      3      7      b      f
0:  BRK    SKB    PHP    RDW   ORAIX  ORAZ   ORA#   ORAM    DIE   ASLZ   ASLA   ASLM   ASOIX  ASOZ   ANC#   ASOM      
1:  BPL    SKB    CLC    RDW   ORAIY  ORAZX  ORAMY  ORAMX   DIE   ASLZX   NOP   ASLMX  ASOIY  ASOZX  ASOMY  ASOMX
2:  JSR   BITZ    PLP    BITM  ANDIX  ANDZ   AND#   ANDM    DIE   ROLZ   ROLA   ROLM   RLAIX  RLAZ   ANC#   RLAM      
3:  BMI    SKB    SEC    RDW   ANDIY  ANDZX  ANDMY  ANDMX   DIE   ROLZX   NOP   ROLMX  RLAIY  RLAZX  RLAMY  RLAMX      
4:  RTI    SKB    PHA    JMP   EORIX  EORZ   EOR#   EORM    DIE   LSRZ   LSRA   LSRM   LSEIX  LSEZ   ALR#   LSEM      
5:  BVC    SKB    CLI    RDW   EORIY  EORZX  EORMY  EORMX   DIE   LSRZX   NOP   LSRMX  LSEIY  LSEZX  LSEMY  LSEMX      
6:  RTS    SKB    PLA    JMPI  ADCIX  ADCZ   ADC#   ADCM    DIE   RORZ   RORA   RORM   RRAIX  RRAZ   ARR#   RRAM      
7:  BVS    SKB    SEI    RDW   ADCIY  ADCZX  ADCMY  ADCMX   DIE   RORZX   NOP   RORMX  RRAIY  RRAZX  RRAMY  RRAMX      
8:  SKB   STYZ    DEY    STYM  STAIX  STAZ    SKB   STAM    SKB   STXZ    TXA   STXM   SAXIX  SAXZ   XAA#   SAXM      
9:  BCC   STYZX   TYA          STAIY  STAZX  STAMY  STAMX   DIE   STXZY   TXS          AXAIY  SAXZY         AXAMY          
a: LDY#   LDYZ    TAY    LDYM  LDAIX  LDAZ L LDA#   LDAM   LDX#   LDXZ    TAX   LDXM   LAXIX  LAXZ   OAL#   LAXM      
b:  BCS   LDYZX   CLV    LDYMX LDAIY  LDAZX  LDAMY  LDAMX   DIE   LDXZY   TSX   LDXMY  LAXIY  LAXZX  LASMY  LAXMY
c: CPY#   CPYZ    INY    CPYM  CMPIX  CMPZ   CMP#   CMPM    SKB   DECZ    DEX   DECM   DCMIX  DCMZ   ASX#   DCMM      
d:  BNE    SKB    CLD    RDW   CMPIY  CMPZX  CMPMY  CMPMX   DIE   DECZX   NOP   DECMX  DCMIY  DCMZX  DCMMY  DCMMX
e: CPX#   CPXZ    INX    CPXM  SBCIX  SBCZ   SBC#   SBCM    SKB   INCZ    NOP   INCM   INSIX  INSZ   S?BC#  INSM      
f:  BEQ    SKB    SED    RDW   SBCIY  SBCZX  SBCMY  SBCMX   DIE   INCZX   NOP   INCMX  INSIY  INSZX  INSMY  INSMX

Addressing modes
 :   0      4      8      c      1      5      9      d      2      6      a      e      3      7      b      f
0:  BRK    SKB    PHP    RDW   ALU.IX ALU.Z  ALU.#  ALU.M   DIE   SHF.Z  SHF.A  SHF.M  SHA.IX SHA,Z  SHA.#  SHA.M
1:  BCC    SKB    CLC    RDW   ALU.IY ALU.ZI ALU.MI ALU.MI  DIE   SHF.ZI  NOP   SHF.MI SHA.IY SHA.ZI SHA.MI SHA.MI
2:  JSR   BITZ    PLP    BITM  ALU.IX ALU.Z  ALU.#  ALU.M   DIE   SHF.Z  SHF.A  SHF.M  SHA.IX SHA,Z  SHA.#  SHA.M
3:  BCC    SKB    SEC    RDW   ALU.IY ALU.ZI ALU.MI ALU.MI  DIE   SHF.ZI  NOP   SHF.MI SHA.IY SHA.ZI SHA.MI SHA.MI
4:  RTI    SKB    PHA    JMP   ALU.IX ALU.Z  ALU.#  ALU.M   DIE   SHF.Z  SHF.A  SHF.M  SHA.IX SHA,Z  SHA.#  SHA.M
5:  BCC    SKB    CLI    RDW   ALU.IY ALU.ZI ALU.MI ALU.MI  DIE   SHF.ZI  NOP   SHF.MI SHA.IY SHA.ZI SHA.MI SHA.MI
6:  RTS    SKB    PLA    JMPI  ALU.IX ALU.Z  ALU.#  ALU.M   DIE   SHF.Z  SHF.A  SHF.M  SHA.IX SHA,Z  SHA.#  SHA.M
7:  BCC    SKB    SEI    RDW   ALU.IY ALU.ZI ALU.MI ALU.MI  DIE   SHF.ZI  NOP   SHF.MI SHA.IY SHA.ZI SHA.MI SHA.MI
8:  SKB   ST_.Z   DEY   ST_.M  ST_.IX ST_.Z  SKB    ST_.M   SKB   ST.Z    TXA   ST_.M  ST_.IX ST_.Z  XAA#   ST_.M
9:  BCC   ST_.ZI  TYA          ST_.IY ST_.ZI ST_.MI ST_.MI  DIE   ST.ZI   TXS          AXAIY  ST.ZI         AXAMY          
a: LD_.#  LD_.Z   TAY   LD_.M  LD_.IX LD_.Z  LD_.#  LD_.M  LD_.#  LD_.Z   TAX   LDXM   LD_.IX LD_.Z   OAL#  LD_.M      
b:  BCC   LD_.ZI  CLV   LD_.MI LD_.IY LD_.ZI LD_.MI LD_.MI  DIE   LD_.ZI  TSX   LDXMY  LD_.IY LD_.ZI LD_.MI  LD_.MI
c: CMP.#  CMP.Z   INY    CPYM  CMP.IX CMP.Z  CMP.#  CMP.M   SKB   DECZ    DEX   DECM   DCMIX  DCMZ   ASX#   DCMM      
d:  BCC    SKB    CLD    RDW   CMP.IY CMP.ZI CMP.MI CMP.MI  DIE   DECZX   NOP   DECMX  DCMIY  DCMZX  DCMMY  DCMMX
e: CMP.#  CMP.Z   INX    CPXM  SBC.IX SBC.Z  SBC.#  SBC.M   SKB   INCZ    NOP   INCM   INSIX  INSZ   S?BC#  INSM      
f:  BCC    SKB    SED    RDW   SBC.IY SBC.ZI SBC.MI SBC.MI  DIE   INCZX   NOP   INCMX  INSIY  INSZX  INSMY  INSMX

1xx00000 => .#  (8ace.0)
1xx00010 => .#  (8ace.2)
xxx000x1 => .IX (even.13)
xxx001xx => .Z  (even.4567)
xxx010x1 => .#  (even.9b)
xxx011xx => .M  (even.cdef except JMP, JMPI)
xxx10000 => .B  (odd.0)
xxx100x1 => .IY (odd.13)
xxx101xx => .ZI (odd.4567)
xxx110x1 => .MI (odd.9b)
xxx110x0 => .A  (odd.8a)
xxx111xx => .MI (odd.cdef)


Types (particularly for memory-related instructions)
 :   0      4      8      c      1      5      9      d      2      6      a      e      3      7      b      f
0:   -      -      -      -      R      R      R      R      -      RW     -      RW     RW     RW     -      RW
1:   -      -      -      -      R      R      R      R      -      RW     -      RW     RW     RW     RW     RW
2:   -      -      -      -      R      R      R      R      -      RW     -      RW     RW     RW     -      RW
3:   -      -      -      -      R      R      R      R      -      RW     -      RW     RW     RW     RW     RW
4:   -      -      -      -      R      R      R      R      -      RW     -      RW     RW     RW     -      RW
5:   -      -      -      -      R      R      R      R      -      RW     -      RW     RW     RW     RW     RW
6:   -      -      -      -      R      R      R      R      -      RW     -      RW     RW     RW     -      RW
7:   -      -      -      -      R      R      R      R      -      RW     -      RW     RW     RW     RW     RW
8:   -      W      -      W      W      W      W      W      -       W     -      W      W      W      -      W
9:   -      W      -      -      W      W      W      W      -       W     -      -      W      W      ?      W
a:   -      R      -      R      R      R      R      R      -       R     -      R      R      R      -      R
b:   -      R      -      R      R      R      R      R      -       R     -      R      R      R      R      R
c:   -      R      -      R      R      R      R      R      -      RW     -      RW     RW     RW     -      RW
d:   -      -      -      -      R      R      R      R      -      RW     -      RW     RW     RW     RW     RW
e:   -      R      -      R      R      R      R      R      -      RW     -      RW     RW     RW     -      RW
f:   -      -      -      -      R      R      R      R      -      RW     -      RW     RW     RW     RW     RW

!100x.xxxx read memory if not 89.xxxx
 100x.xxxx write memory if 89.xxxx
 0xxx.xx1x write memory if 0-7.2367abef
 110x.xx1x write memory if cd.2367abef

Source driven by (AXYS) (during ALU)
 :   0      4      8      c      1      5      9      d      2      6      a      e      3      7      b      f
0:  PSR     -     PSR     -      A      A      A      A      -      -      A      -      A      A      A      A
1:   -      -      0      -      A      A      A      A      -      -      -      -      A      A      A      A
2:   -      A      -      A      A      A      A      A      -      -      A      -      A      A      A      A
3:   -      -      1      -      A      A      A      A      -      -      -      -      A      A      A      A
4:   -      -      A      -      A      A      A      A      -      -      A      -      A      A      A      A
5:   -      -      0      -      A      A      A      A      -      -      -      -      A      A      A      A
6:   -      -      -      -      A      A      A      A      -      -      A      -      A      A      A      A
7:   -      -      1      -      A      A      A      A      -      -      -      -      A      A      A      A
8:   -      Y      Y      Y      A      A      -      A      -      X      X      X      AX     AX     X      AX
9:   -      Y      Y             A      A      A      A      -      X      X      X      AX     AX     AX     AX
a:   -      -      A      -      -      -      -      -      -      -      A      -      -      -      A      -       
b:   -      -      0      -      -      -      -      -      -      -      S      -      -      -      S      -  
c:   Y      Y      Y      Y      A      A      A      A      -      -      X      -      A      A     AX      A
d:   -      -      0      -      A      A      A      A      -      -      -      -      A      A      A      A
e:   X      X      X      X      A      A      A      A      -      -      -      -      A      A      A      A
f:   -      -      1      -      A      A      A      A      -      -      -      -      A      A      A      A

Source
xxxxxx01 => A   (any.159d)
0xxxxxxx => A   (01234567.x)
100xxx11 => A   (89.37bf)
1010xxxx => A   (a.x)
1xxxxx11 => A   (cdef.37bf)
100xxx1x => X   (89.2367abef)
1100101x => X   (c.ab)
111xxx00 => X   (ef.048c)
100xxx00 => Y   (89.048c)
1011xxxx => S   (b.x)
110xxx00 => Y   (cd.048c)

Source written to (AXYS) (during ALU: . implies no ALU)
 :   0      4      8      c      1      5      9      d      2      6      a      e      3      7      b      f
0:   -      -      -      -      AF     AF     AF     AF     -      F      AF     F      AF     AF     AF     AF
1:   .      -      F      -      AF     AF     AF     AF     -      F      -      F      AF     AF     AF     AF
2:   -      F     PSR     F      AF     AF     AF     AF     -      F      AF     F      AF     AF     AF     AF
3:   .      -      F      -      AF     AF     AF     AF     -      F      -      F      AF     AF     AF     AF
4:  PSR     -      -      -      AF     AF     AF     AF     -      F      AF     F      AF     AF     AF     AF
5:   .      -      F      -      AF     AF     AF     AF     -      F      -      F      AF     AF     AF     AF
6:   -      -      AF     -      AF     AF     AF     AF     -      F      AF     F      AF     AF     AF     AF
7:   .      -      F      -      AF     AF     AF     AF     -      F      -      F      AF     AF     AF     AF
8:   ?      .      YF     .      .      .      ?      .      -      .      AF     .      .      .      AF     .
9:   .      .      AF     ?      .      .      .      .      -      .      SF     .      .      .      .      .
a:   YF     YF     YF     YF     AF     AF     AF     AF     XF     XF     XF     XF     AXF    AXF   AXF     AXF       
b:   .      YF     F      YF     AF     AF     AF     AF     -      XF     XF     XF     AXF    AXF   AXSF    AXF  
c:   F      F      YF     F      F      F      F      F      -      F      XF     F      F      F      XF     F
d:   .      ?      F      ?      F      F      F      F      -      F      -      F      F      F      F      F
e:   F      F      XF     F      AF     AF     AF     AF     -      F      !      F      AF     AF     AF     AF
f:   .      ?      F      ?      AF     AF     AF     AF     -      F      -      F      AF     AF     AF     AF

Source
# A   (0-bef.13579bdf, 68, 98, 02468.a, 8.37bf)
# X   (ab.26ae37bf, c.ab, 8.37f)
# Y   (a.048c, b4.c, 88, c8)
# F   (0-7a-f.13579bdf, actually possibly everything that does an ALU complete? which one's dont?)
0xxxxxx1 => A   (01234567.159d37bf)
1x1xxxx1 => A   (abef.159d37bf)
# A   (68, 98, 02468.a, 8.37bf)
# X   (ab.26ae37bf, c.ab, 8.37f)
# Y   (ab.26ae37bf, c.ab, 8.37f)

Not handled yet
 :   0      4      8      c       2      6      a      e      3      7      b      f
0:  BRK    SKB    PHP    RDW     DIE   ASLZ   ASLA   ASLM   ASOIX  ASOZ   ANC#   ASOM      
1:  BPL    SKB    CLC    RDW     DIE   ASLZX   NOP   ASLMX  ASOIY  ASOZX  ASOMY  ASOMX
2:  JSR   BITZ    PLP    BITM    DIE   ROLZ   ROLA   ROLM   RLAIX  RLAZ   ANC#   RLAM      
3:  BMI    SKB    SEC    RDW     DIE   ROLZX   NOP   ROLMX  RLAIY  RLAZX  RLAMY  RLAMX      
4:  RTI    SKB    PHA    JMP     DIE   LSRZ   LSRA   LSRM   LSEIX  LSEZ   ALR#   LSEM      
5:  BVC    SKB    CLI    RDW     DIE   LSRZX   NOP   LSRMX  LSEIY  LSEZX  LSEMY  LSEMX      
6:  RTS    SKB    PLA    JMPI    DIE   RORZ   RORA   RORM   RRAIX  RRAZ   ARR#   RRAM      
7:  BVS    SKB    SEI    RDW     DIE   RORZX   NOP   RORMX  RRAIY  RRAZX  RRAMY  RRAMX      
8:  SKB   STYZ    DEY    STYM    SKB   STXZ    TXA   STXM   SAXIX  SAXZ   XAA#   SAXM      
9:  BCC   STYZX   TYA            DIE   STXZY   TXS          AXAIY  SAXZY         AXAMY          
a: LDY#   LDYZ    TAY    LDYM   LDX#   LDXZ    TAX   LDXM   LAXIX  LAXZ   OAL#   LAXM      
b:  BCS   LDYZX   CLV    LDYMX   DIE   LDXZY   TSX   LDXMY  LAXIY  LAXZX  LASMY  LAXMY
c: CPY#   CPYZ    INY    CPYM    SKB   DECZ    DEX   DECM   DCMIX  DCMZ   ASX#   DCMM      
d:  BNE    SKB    CLD    RDW     DIE   DECZX   NOP   DECMX  DCMIY  DCMZX  DCMMY  DCMMX
e: CPX#   CPXZ    INX    CPXM    SKB   INCZ    NOP   INCM   INSIX  INSZ   S?BC#  INSM      
f:  BEQ    SKB    SED    RDW     DIE   INCZX   NOP   INCMX  INSIY  INSZX  INSMY  INSMX

IDB source (int) - X and Y are used in indexed addressing modes too
 :   0      4      8      c      1      5      9      d      2      6      a      e      3      7      b      f
0:  BRK     -      P      -      A      A      A      A      -      -      -      -      A      A      A      A       
1:   -      -      -      -      A      A      A      A      -      -      -      -      A      A      A      A  
2:  JSR     A      -      A      A      A      A      A      -      -      -      -      A      A      A      A       
3:   -      -      -      -      A      A      A      A      -      -      -      -      A      A      A      A        
4:  RTI     -      A     JMP     A      A      A      A      -      -      -      -      A      A      A      A       
5:   -      -      -      -      A      A      A      A      -      -      -      -      A      A      A      A        
6:  RTS     -      -     JMPI    A      A      A      A      -      -      -      -      A      A      A      A       
7:   -      -      -      -      A      A      A      A      -      -      -      -      A      A      A      A        
8:   -      Y      Y      Y      A      A      -      A      -      X      X      X     A&X    A&X     X     A&X      
9:   -      Y      Y             A      A      A      A      -      X      X            A&X    A&X    A&X    A&X
a:   -      -      -      -      -      -      -      -      -      -      -      -      -      -     A|?     -        
b:   -      -      -      -      -      -      -      -      -      -      -      -      -      -      -      -  
c:   Y      Y      Y      Y      A      A      A      A      -      -      X      A      A      A     A&X     A       
d:   -      -      -      -      A      A      A      A      -      -      -      A      A      A      A      A  
e:   X      X      X      X      A      A      A      A      -      -      -      A      A      A    S?BC#    A       
f:   -      -      -      -      A      A      A      A      -      -      -      A      A      A      A      A  

IDB source (B) - want to lost S, X and Y from here; HM should come from DL (as does imm, M); can this always be DL?
 :   0      4      8      c      1      5      9      d      2      6      a      e      3      7      b      f
0:  BRK     -      P?     -      M      M     Imm     M      -      M      A      M      M      M     Imm     M       
1:   -      -      -      -      M      M      M      M      -      M      -      M      M      M      M      M  
2:  JSR     M      M      M      M      M     Imm     M      -      M      A      M      M      M     Imm     M       
3:   -      -      -      -      M      M      M      M      -      M      -      M      M      M      M      M        
4:  RTI     -      A?    JMP     M      M     Imm     M      -      M      A      M      M      M    A&Imm    M       
5:   -      -      -      -      M      M      M      M      -      M      -      M      M      M      M      M        
6:  RTS     -      M?    JMPI    M      M     Imm     M      -      M      A      M      M      M    A&Imm    M       
7:   -      -      -      -      M      M      M      M      -      M      -      M      M      M      M      M        
8:   -      -      -      -      -      -     Imm     -      -      -      -      0      0      0     Imm     0       
9:   -      -      Y             -      -      -      -      -      -      -     HM     HM      0     HM     HM             
a:   M      M      A      M      M      M     Imm     M     Imm     M      A      M      M      M     Imm     M       
b:   -      M      -      M      M      M      M      M      -      M      S      M      M      M     S&M     M  
c:  Imm     M      M      M      M      M     Imm     M      -      M      X      M      M      M     Imm     M       
d:   -      -      -      -      M      M      M      M      -      M      -      M      M      M      M      M  
e:  Imm     M      M      M      M      M     Imm     M      -      M      -      M      M      M     Imm     M       
f:   -      -      -      -      M      M      M      M      -      M      -      M      M      M      M      M  

ALU dest
 :   0      4      8      c      1      5      9      d      2      6      a      e      3      7      b      f
0:  BRK     -      -      -      A      A      A      A      M      M      A      M     A&M    A&M     A     A&M       
1:   -      -      -      -      A      A      A      A      M      M      M      M     A&M    A&M    A&M    A&M  
2:  JSR     A      P      A      A      A      A      A      M      M      A      M     A&M    A&M     A     A&M       
3:   -      -      -      -      A      A      A      A      M      M      M      M     A&M    A&M    A&M    A&M        
4:  RTI     -      -     JMP     A      A      A      A      M      M      A      M     A&M    A&M     A     A&M       
5:   -      -      -      -      A      A      A      A      M      M      M      M     A&M    A&M    A&M    A&M        
6:  RTS     -      A     JMPI    A      A      A      A      M      M      A      M     A&M    A&M     A     A&M       
7:   -      -      -      -      A      A      A      A      M      M      M      M     A&M    A&M    A&M    A&M        
8:   -      Y      Y      Y      -      -      -      -      -      X      A      X      M      M      X      M       
9:   -      Y      Y             -      -      -      -      -      X     (S)     M      M      M     M(+S)   M
a:   Y      Y      Y      Y      A      A      A      A      X      X      X      X     A&X    A&X     X     A&X        
b:   -      Y      -      Y      -      A      A      A      -      X      X      X     A&X    A&X    A&X    A&X  
c:   -      -      Y      -      -      -      -      -      -      -      X      -      -      -      X      -       
d:   -      -      -      -      -      -      -      -      -      -      -      -      -      -      -      -  
e:   -      -      X      -      A      A      A      A      -      -      -      -      A      A      A      A       
f:   -      -      -      -      A      A      A      A      -      -      -      -      A      A      A      A  

ALU shift/inc/dec
 :   0      4      8      c      1      5      9      d      2      6      a      e      3      7      b      f
0:   -      -      -      -      -      -      -      -      -     ASL    ASL    ASL    ASL    ASL    ASL    ASL    *-perhaps ASL since C=din[7]     
1:   -      -      -      -      -      -      -      -      -     ASL    ASL    ASL    ASL    ASL    ASL    ASL  
2:   -      -      -      -      -      -      -      -      -     ROL    ROL    ROL    ROL    ROL    ROL    ROL       
3:   -      -      -      -      -      -      -      -      -     ROL    ROL    ROL    ROL    ROL    ROL    ROL        
4:   -      -      -      -      -      -      -      -      -     LSR    LSR    LSR    LSR    LSR    LSR    LSR       
5:   -      -      -      -      -      -      -      -      -     LSR    LSR    LSR    LSR    LSR    LSR    LSR        
6:   -      -      -      -      -      -      -      -      -     ROR    ROR    ROR    ROR    ROR    ROR    ROR       
7:   -      -      -      -      -      -      -      -      -     ROR    ROR    ROR    ROR    ROR    ROR    ROR        
8:   -      -      -      -      -      -      -      -      -      -      -      -      -      -      -      -       
9:   -      -      -      -      -      -      -      -      -      -      -      -      -      -      -      -       
a:   -      -      -      -      -      -      -      -      -      -      -      -      -      -      -      -         
b:   -      -      -      -      -      -      -      -      -      -      -      -      -      -      -      -   
c:   -      -      -      -      -      -      -      -      -     DEC    DEC    DEC    DEC    DEC    DEC    DEC     
d:   -      -      -      -      -      -      -      -      -     DEC    DEC    DEC    DEC    DEC    DEC    DEC 
e:   -      -      -      -      -      -      -      -      -     INC    INC    INC    INC    INC    INC    INC      
f:   -      -      -      -      -      -      -      -      -     INC    INC    INC    INC    INC    INC    INC 

ALU op
 :   0      4      8      c      1      5      9      d      2      6      a      e      3      7      b      f
0:   -      -      -      -     ORA    ORA    ORA    ORA     -      -      -      -     ORA    ORA    ANC    ORA       
1:   -      -      -      -     ORA    ORA    ORA    ORA     -      -      -      -     ORA    ORA    ORA    ORA  
2:   -      -      -      -     AND    AND    AND    AND     -      -      -      -     AND    AND    ANC    AND       
3:   -      -      -      -     AND    AND    AND    AND     -      -      -      -     AND    AND    AND    AND        
4:   -      -      -      -     EOR    EOR    EOR    EOR     -      -      -      -     EOR    EOR     -     EOR       
5:   -      -      -      -     EOR    EOR    EOR    EOR     -      -      -      -     EOR    EOR    EOR    EOR        
6:   -      -      -      -     ADC    ADC    ADC    ADC     -      -      -      -     ADC    ADC     -     ADC       
7:   -      -      -      -     ADC    ADC    ADC    ADC     -      -      -      -     ADC    ADC    ADC    ADC        
8:   -      -      -      -      -      -      -      -      -      -      -      -      -      -      -      -       
9:   -      -      -      -      -      -      -      -      -      -      -      -      -      -      -      -   
a:   -      -      -      -      -      -      -      -      -      -      -      -      -      -      -      -         
b:   -      -      -      -      -      -      -      -      -      -      -      -      -      -      -      -   
c:   -      -      -      -     CMP    CMP    CMP    CMP     -      -      -      -     CMP    CMP    CMP    CMP     
d:   -      -      -      -     CMP    CMP    CMP    CMP     -      -      -      -     CMP    CMP    CMP    CMP 
e:   -      -      -      -     SBC    SBC    SBC    SBC     -      -      -      -     SBC    SBC    SBC    SBC      
f:   -      -      -      -     SBC    SBC    SBC    SBC     -      -      -      -     SBC    SBC    SBC    SBC 


ALU ops
 :   0      1      2      3      4      5      6      7      8      9      a      b      c      d      e      f
0:  BRK   ORA     DIE   ASO     SKB   ORA    ASL    ASO     PHP   ORA    ASL    ANC#    RDW   ORA    ASL    ASO       
1:  BPL   ORA     DIE   ASO     SKB   ORA    ASL    ASO     CLC   ORA     NOP   ASOMY   RDW   ORA    ASL    ASO  
2:  JSR   AND     DIE   RLA    BITZ   AND    ROL    RLA     PLP   AND    ROL    ANC#    BITM  AND    ROL    RLA       
3:  BMI   AND     DIE   RLA     SKB   AND    ROL    RLA     SEC   AND     NOP   RLAMY   RDW   AND    ROL    RLA        
4:  RTI   EOR     DIE   LSE     SKB   EOR    LSR    LSE     PHA   EOR    LSR    ALR#    JMP   EOR    LSR    LSE       
5:  BVC   EOR     DIE   LSE     SKB   EOR    LSR    LSE     CLI   EOR     NOP   LSEMY   RDW   EOR    LSR    LSE        
6:  RTS   ADC     DIE   RRA     SKB   ADC    ROR    RRA     PLA   ADC    ROR    ARR#    JMPI  ADC    ROR    RRA       
7:  BVS   ADCIY   DIE   RRA     SKB   ADC    ROR    RRA     SEI   ADC     NOP   RRAMY   RDW   ADC    ROR    RRA        
8:  SKB   STAIX   SKB   SAXIX  STYZ   STAZ   STXZ   SAXZ    DEY    SKB    TXA   XAA#    STYM  STAM   STXM   SAXM      
9:  BCC   STAIY   DIE   AXAIY  STYZX  STAZX  STXZY  SAXZY   TYA   STAMY   TXS                 STAMX         AXAMY          
a: LDY#   LDAIX  LDX#   LAXIX  LDYZ   LDAZ   LDXZ   LAXZ    TAY   LDA#    TAX   OAL#    LDYM  LDAM   LDXM   LAXM      
b:  BCS   LDAIY   DIE   LAXIY  LDYZX  LDAZX  LDXZY  LAXZX   CLV   LDAMY   TSX   LASMY   LDYMX LDAMX  LDXMY  LAXMY
c: CPY#   CMP     SKB   DCM    CPYZ   CMP    DEC    DCM     INY   CMP     DEX   ASX#    CPYM  CMP    DEC    DCM       
d:  BNE   CMP     DIE   DCM     SKB   CMP    DEC    DCM     CLD   CMP     NOP   DCMMY   RDW   CMP    DEC    DCM  
e: CPX#   SBC     SKB   INS    CPXZ   SBC    INC    INS     INX   SBC     NOP   SBC#    CPXM  SBC    INC    INS       
f:  BEQ   SBC     DIE   INS     SKB   SBC    INC    INS     SED   SBC     NOP   INSMY   RDW   SBC    INC    INS  

Addressing modes:

 :   0      1      2      3      4      5      6      7      8      9      a      b      c      d      e      f
0: ?BRK   IX.in  ?DIE   IX.rw  Z .in  Z .in  Z .rw  Z .rw   IMPP   IMM    IMP    IMM    RDW   M .in  M .rw  M. rw      
1:  BCC   IY.in  ?DIE   IY.rw  ZX.in  ZX.in  ZX.rw  ZX.rw   IMP   MY.in   IMP   MY.rw   RDW   MX.in  MX.rw  MX.rw
2: ?JSR   IX.in  ?DIE   IX.rw  Z .in  Z .in  Z .rw  Z .rw   IMPP   IMM    IMP    IMM   M .in  M .in  M .rw  M. rw      
3:  BCC   IY.in  ?DIE   IY.rw  ZX.in  ZX.in  ZX.rw  ZX.rw   IMP   MY.in   IMP   MY.rw   RDW   MX.in  MX.rw  MX.rw      
4:  IMPR  IX.in  ?DIE   IX.rw  Z .in  Z .in  Z .rw  Z .rw   IMPP   IMM    IMP    IMM   M .in  M .in  M .rw  M. rw      
5:  BCC   IY.in  ?DIE   IY.rw  ZX.in  ZX.in  ZX.rw  ZX.rw   IMP   MY.in   IMP   MY.rw   RDW   MX.in  MX.rw  MX.rw      
6:  IMPR  IX.in  ?DIE   IX.rw  Z .in  Z .in  Z .rw  Z .rw   IMPP   IMM    IMP    IMM   ?JMPI  M .in  M .rw  M. rw      
7:  BCC   IY.in  ?DIE   IY.rw  ZX.in  ZX.in  ZX.rw  ZX.rw   IMP   MY.in   IMP   MY.rw   RDW   MX.in  MX.rw  MX.rw      
8: ?SKB   IX.ot  ?SKB   IX.ot  Z .ot  Z .ot  Z .ot  Z .ot   IMP    IMM    IMP    IMM    M .ot M .ot  M .ot  M .ot     
9:  BCC   IY.ot  ?DIE   IX.ot  ZX.ot  ZX.ot  ZY.ot  ZY.ot   IMP   MY.ot   IMP           MX.ot MX.ot  MX.ot  MY.ot          
a:  IMM   IX.in   IMM   IX.in  Z .in  Z .in  Z .in  Z .in   IMP    IMM    IMP    IMM    M .in M .in  M .in  M .in     
b:  BCC   IY.in  ?DIE   IY.in  ZX.in  ZX.in  ZY.in  ZX.in   IMP   MY.in   IMP   MY.in   MX.in MX.in  MY.in  MY.in
c:  IMM   IX.in  ?SKB   IX.rw  Z .in  Z .in  Z .rw  Z .rw   IMP    IMM    IMP    IMM    M .in M .in  M .rw  M. rw      
d:  BCC   IY.in  ?DIE   IY.rw  ZX.in  ZX.in  ZX.rw  ZX.rw   IMP   MY.in   IMP   MY.rw   RDW   MX.in  MX.rw  MX.rw
e:  IMM   IX.in  ?SKB   IX.rw  Z .in  Z .in  Z .rw  Z .rw   IMP    IMM    IMP    IMM    M .in M .in  M .rw  M. rw      
f:  BCC   IY.in  ?DIE   IY.rw  ZX.in  ZX.in  ZX.rw  ZX.rw   IMP   MY.in   IMP   MY.rw   RDW   MX.in  MX.rw  MX.rw


Non-ALU/load/store opcodes...
 :   0      1      2      3      4      5      6      7      8      9      a      b      c      d      e      f
0:  BRK     -      -      -      -      -      -      -     PHP     -      -      -       -     -      -      -       
1:  BPL     -      -      -      -      -      -      -     CLC     -      -      -       -     -      -      -  
2:  JSR     -      -      -      -      -      -      -     PLP     -      -      -       -     -      -      -       
3:  BMI     -      -      -      -      -      -      -     SEC     -      -      -       -     -      -      -        
4:  RTI     -      -      -      -      -      -      -     PHA     -      -      -     JMP     -      -      -       
5:  BVC     -      -      -      -      -      -      -     CLI     -      -      -       -     -      -      -        
6:  RTS     -      -      -      -      -      -      -     PLA     -      -      -     JMPI    -      -      -       
7:  BVS     -      -      -      -      -      -      -     SEI     -      -      -       -     -      -      -        
8:  -       -      -      -      -      -      -      -     DEY     -     TXA     -       -     -      -      -       
9:  BCC     -      -      -      -      -      -      -     TYA     -     TXS     -       -     -      -      -            
a:   -      -      -      -      -      -      -      -     TAY     -     TAX     -       -     -      -      -       
b:  BCS     -      -      -      -      -      -      -     CLV     -     TSX     -       -     -      -      -  
c:   -      -      -      -      -      -      -      -     INY     -     DEX     -       -     -      -      -       
d:  BNE     -      -      -      -      -      -      -     CLD     -      -      -       -     -      -      -  
e:   -      -      -      -      -      -      -      -     INX     -      -      -       -     -      -      -       
f:  BEQ     -      -      -      -      -      -      -     SED     -      -      -       -     -      -      -  

Conditional branch is to PC + offset (sign extended)
=> PCL = PCL + offset
=> PCH = PCH + 0 + carry extended

JSR pushes PC+2
RTS is PC <= pulled PC +1
RTI is PC <= pulled PC...

Other opcodes are then:
BRK, JSR, JMP, JMPI, RTI, RTS
CLC, SEC, CLI, SEI, CLV, CLD, SED
PHP, PHA
PLP, PLA
DEY, INY, DEX, INX
TAY, TYA, TAX, TXA, TSX, TXS

ASO is A OR (op<<1)
RLA is A AND (op<r<1)
LSE is A EOR (op>>1)
RRA is A + (op>r>1)
i.e. shift is done first, and arithmetic/logic is done with accumulator and the shift result
Looking at INS, DCM:
INS is A - (op++). It does increment the memory, but the ALU result is only put in the accumulator
DCM is A - (op--). It does increment the memory, but the ALU result is only put in the accumulator
These instructions DO take an additional cycle - hence they probably have a different addressing mode, effectively

ALR/ARR are A AND (op>>1) and A AND (op>r>1). Immediate only.
ANC is A AND op but with bit 7 going to C as well as N.
These link with XAA, OAL, ASX (and SBC #): XAA is A=X AND op; OAL is X,A=A OR (ee...) AND op; ASX is X=(A&X)-op

SAX is store (A & X) - sort of STX&STA simultaneously - hence both X and A probably drive IDB
LAX is load (A & X)  - sort of LDX&LDA simultaneously
AXA is store (A & X & (high byte of address+1))
LAS is AND memory with stack pointer and store in A, stack pointer, X.

# ASL if 0x/1x x in [2,3, 6,7, a,b, e,f]
# ROL if 2x/3x x in [2,3, 6,7, a,b, e,f]
# LDR if 4x/5x x in [2,3, 6,7, a,b, e,f]
# ROR if 6x/7x x in [2,3, 6,7, a,b, e,f]
# INC if cx/dx x in [2,3, 6,7, a,b, e,f]
# DEC if ex/fx x in [2,3, 6,7, a,b, e,f]
# ORA if 0x/1x x in [1,3 5,7,9,b,d,f]
# AND if 2x/3x x in [1,3 5,7,9,b,d,f]
# EOR if 4x/5x x in [1,3 5,7,9,b,d,f]
# ADC if 6x/7x x in [1,3 5,7,9,b,d,f]
# CMP if cx/dx x in [0,1,3,4,5,7,9,b,c,d,f] (i.e. not 2,6,a,e)
# SBC if ex/fx x in [0,1,3,4,5,7,9,b,c,d,f] (i.e. not 2,6,a,e)

ALU op is ORA, AND, EOR, ADC, LDA, CMP, SBC (ANC, ALR, ARR, XAA, OAL, ASX)

ALU Addressing mode IMM:
0 - read imm, DL <= data
1 - fetch next, dest <= ALU op A/X/Y, DL

Addressing mode Z.in
0 - read, DL <= data
1 - read (0,DL), DL <= data
2 - fetch next, dest <= ALU op A/X/Y, DL

Addressing mode Z.rw
0 - read, DL <= data
1 - read (0,DL), DL <= data
2 - write (0,DL,incorrect), ADL<=DL, DL <= ALU op A/X/Y, DL
3 - write (0,DL,valid)
4 - fetch next

Addressing mode Z.ot
0 - read, DL <= data
2 - write (0,DL,A/X/Y/A&X (wire-and?) valid)
3 - fetch next

ALU Addressing mode ZX.in (also ZY.in)
0 - read, DL <= data
1 - read unknown, DL <= DL+X
2 - read (0,DL), DL <= data
3 - fetch next, A(or X or Y)/PSR <= ALU op A (or X or Y), DL

ALU Addressing mode ZX.rw (also ZY.rw)
0 - read, DL <= data
1 - read unknown, ALU=DL+X, ADL <= ALU
2 - read (0,DL+X), DL <= data
3 - write (0,DL+X,incorrect), ADL<=DL, DL <= ALU op A/X/Y, DL
4 - write (0,DL+X,valid)
5 - fetch next

ALU Addressing mode ZX.ot (also ZY.ot)
0 - read, DL <= data
1 - read unknown, ALU=DL+X, ADL <= ALU
2 - write (0,DL,A/X/Y/A&X (wire-and?) valid)
3 - fetch next

Addressing mode M.in
0 - read, DL <= data
1 - read, ADL<=DL, DL <= data
2 - read (DL,ADL), DL <= data
3 - fetch next, dest <= ALU op A/X/Y, DL

Addressing mode M.ot
0 - read, DL <= data
1 - read, ADL<=DL, DL <= data
2 - write (DL,ADL,A/X/Y/A&X (wire-and?) valid)
3 - fetch next

Addressing mode M.rw
0 - read, DL <= data
1 - read, ADL<=DL, DL <= data
2 - read (DL,ADL), ADH<=DL, DL <= data
3 - write (ADH,ADL,invalid), DL <= ALU op A/X/Y, DL
4 - write (ADH,ADL,DL)
5 - fetch next

Addressing mode MX.in (also MY.in)
0 - read, DL <= data
1 - read, ADL<=DL+X, DL <= data (CC -> skip 2)
2 - read (DL,ADL), DL <= DL+1
3 - read (DL,ADL), DL <= data
4 - fetch next, dest <= ALU op A/X/Y, DL

Addressing mode MX.rw
0 - read, DL <= data
1 - read, ADL<=DL+X, DL <= data (CC -> skip 2)
2 - read (DL,ADL), DL <= DL+1
3 - read (DL,ADL), ADH<=DL, DL <= data
4 - write (ADH,ADL,invalid), DL <= ALU op A/X/Y, DL
5 - write (ADH,ADL,DL)
6 - fetch next

Addressing mode MX.ot (also MY.ot)
0 - read, DL <= data
1 - read, ADL<=DL+X, DL <= data (CC -> skip 2)
2 - read (DL,ADL), DL <= DL+1
3 - write (DL,ADL,A/X/Y/A&X (wire-and?) valid)
4 - fetch next

Addressing mode IX.in
0 - read, DL <= data
1 - read invalid, DL<=DL+X
2 - read (0,DL), DL <= data, ADL <= DL+1
3 - read (0,ADL), DL <= data, ADL <= DL
4 - read (DL,ADL), DL <= data
5 - fetch next, dest <= ALU op A/X/Y, DL

Addressing mode IX.rw (no standard instructions)
0 - read, DL <= data
1 - read invalid, DL<=DL+X
2 - read (0,DL), DL <= data, ADL <= DL+1
3 - read (0,ADL), DL <= data, ADL <= DL
4 - read (DL,ADL), DL <= data
5 - write (ADH,ADL,invalid), DL <= ALU op A/X/Y, DL
6 - write (ADH,ADL,DL)
7 - fetch next

Addressing mode IX.ot
0 - read, DL <= data
1 - read invalid, ADL<=DL+X
2 - read (0,ADL), DL <= data, ADL <= DL+1
3 - read (0,ADL), DL <= data, ADL <= DL
4 - write (DL,ADL,A/X/Y/A&X (wire-and?) valid)
5 - fetch next

Addressing mode IY.in
0 - read, DL <= data
1 - read (0,DL), DL <= data, ADL <= DL+1
2 - read (0,ADL), DL <= data, ADL <= DL+Y, skip 3 if cc
3 - read (DL,ADL), DL <= DL+1
4 - read (DL,ADL), DL <= data
5 - fetch next, dest <= ALU op A/X/Y, DL

Addressing mode IY.rw (no standard instructions)
0 - read, DL <= data
1 - read (0,DL), DL <= data, ADL <= DL+1
2 - read (0,ADL), DL <= data, ADL <= DL+Y, skip 3 if cc
3 - read (DL,ADL), DL <= DL+1
4 - read (DL,ADL), DL <= data
5 - write (ADH,ADL,invalid), DL <= ALU op A/X/Y, DL
6 - write (ADH,ADL,DL)
7 - fetch next

Addressing mode IY.ot
0 - read, DL <= data
1 - read (0,DL), DL <= data, ADL <= DL+1
2 - read (0,ADL), DL <= data, ADL <= DL+Y, skip 3 if cc
3 - read (DL,ADL), DL <= DL+1
4 - write (DL,ADL,A/X/Y/A&X (wire-and?) valid)
5 - fetch next


"""

