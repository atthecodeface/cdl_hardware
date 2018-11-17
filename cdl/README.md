# CDL modules

This repository contains a number of open source CDL modules (either
Apache or BSD licensed) that may be freely reused in any project.

## Purpose

The purpose of this repository is to provide freely available modules
for both teaching and implementation; the repository includes
regression suites for most of the designs, which permits some
confidence in the solidity of the design.

A second purpose of the repository is to provide for a corpus of open
source hardware modules written in CDL, to enable a new version of CDL
to be designed; this new version will include use of a hardware IR
(intermediate representation) language that permits targeting and
optimization for a number of backends (simulation, verification, FPGA,
silicon, emulation, and so on).

## Module structure

The modules are grouped into separate directories based on function.

* apb

  The APB modules are predominantly simple APB peripherals; timers,
  GPIO, and other fixed purpose I/O. There is also the *apb_processor*
  which is a module that can replay APB transactions (reads and
  writes) from a ROM, and execute simple ALU operations and loop
  depending on values in an accumulator; this module permits somewhat
  flexible APB transactions to be performed in hardware without a
  microcontroller (such as to initialize a PLL or DDR controller,
  where APB transactions may depend on lock, skew, etc).

* boards

  The boards directory contains subdirectories for various FPGA or
  other boards, into which various designs have been built. At present
  this is mainly the Terasic Cyclone V DE1 board, with the Cambridge
  University Computer Laboratory I/O daughterboard.

* cpu

  The cpu directory contains a 6502 implementation and numerous RISC-V
  implementations.

  The RISC-V implementations are based around a variety of execution
  pipelines of varying lengths, with replaceable instruction
  decoders. This permits a breadth of embedded RISC-V implementations
  to be created, supporting a range of RV32 ISA sets (such as RV32E,
  RV32IMAC, etc). The pipelines are customizable with user instruction
  encodings as well.

* csrs

  The CSR modules (control/status register) map the APB bus to a
  pipelined request/response bus to fit in to an FPGA (or silicon)
  without having to use multicycle paths or slow timing in any
  way. The modules include one that maps APB to the CSR interface; a
  CSR interface back to APB; and a CSR interface to simple
  single-cycle read/write accesses.

* input_devices

  At present the input_devices modules consist solely of PS2-keyboard
  related modules: a PS2 host (to which a keyboard may be connected);
  and a PS2 keyboard decoder (which maps PS2 keyboard codes to key
  up/down events for an 8-bit keycode).

* led

  This directory contains useful modules for driving LEDs: LED
  7-segment display, from hex digits; a Neopixel (WS2812) driver for
  any length of Neopixel chain.

* microcomputers

  At present the 'BBC microcomputer' is the only microcomputer design;
  this is an implementation of the BBC microcomputer model B, with
  video, ROMs, and floppy disk controller, that runs at 50MHz on a the
  Cyclone V.

  A 'Picoriscv' implementation is at a conceptual level; it is not
  clear if this is worth moving forward with outside of the RISC-V CPU
  directory, at present.

* network

  At present, empty

* serial

* storage

  The storage modules currently consist of only a model of the Intel
  8271 floppy disk controller; this was the initial floppy disk
  controller for the BBC microcomputer. Instead of supporting a
  physical disk drive, the FDC8271 module uses an SRAM to supply track
  format and sector information, as well as disk data.

* utils

  The utils directory contains some generic utility modules. Firstly
  there is a generic module to support multiplexing two
  request/acknowledge buses on to a single request/acknowledge
  bus. This has to be compiled using CDL options to specify the actual
  request/acknowledge type bus required for a module - this is the CDL
  1.4 method for parametrizing types. This module is used in two @a
  dprintf multiplexer modules also in the utils directory.

  The dprintf module is an sprintf-like module: it is used for debug
  printing. The module is supplied with a request - a format string to
  display with arguments, and an address - and it generates a stream
  of output bytes (with addresses) that are the output of the
  formatting. The module supports 7-bit characters (suitable for
  teletext), and hexadecimal and decimal formatted numbers (with field
  size).

  The utils also includes a hysteresis_switch module. This module
  takes an input and generates a filtered output using hysteresis; it
  may be used, for example, to debounce an input switch.

* video

  The video modules relate to video output, currently. There are two
  framebuffer modules - one uses a bitmap framebuffer, and the other a
  teletext framebuffer (where the SRAM contains characters and control
  codes). These use a framebuffer_timing module, that generates the
  timing for a video output (vsync, hsync, display area enable, and so
  on).

  To provide the teletext decoding there is a teletext decoder module;
  this is used also by the Mullard SAA5050 implementation, used by the
  BBC microcomputer.

  There is also a Motorola 6845 CRTC controller module, which was a
  character video timing generator, that was used for all the display
  modes in the BBC microcomputer.


## Documentation progress

Currently documented: apb, csrs, input_devices, utils, led

To do: storage, microcomputers, cpus, serial
