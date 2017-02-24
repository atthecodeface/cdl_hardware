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

  The APB modules are predominantly simple APB peripherals; timer,
  GPIO. There is also the *apb_processor* which is a module that can
  replay APB transactions (reads and writes) from a ROM, and execute
  simple ALU operations and loop depending on values in an
  accumulator; this module permits somewhat flexible APB transactions
  to be performed in hardware without a microcontroller (such as to
  initialize a PLL or DDR controller, where APB transactions may
  depend on lock, skew, etc).

* boards

  The boards directory contains subdirectories for various FPGA or
  other boards, into which various designs have been built. At present
  this is mainly the Terasic Cyclone V DE1 board, with the Cambridge
  University Computer Laboratory I/O daughterboard.

* cpus

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

* network

* serial

* storage

* utils

* video

## Documentation progress

Currently documented: apb, csrs, input_devices, utils, led

In progress: video

To do: storage, microcomputers, cpus, serial
