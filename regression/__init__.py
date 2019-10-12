import unittest, importlib, sys, os
tests = [#"base6502",
         "leds",
         "teletext",
         "csrs",
         "apb",
         "axi",
         "de1_cl_hps",
         "vcu108",
         "utils",
         "riscv_minimal",
         "riscv_coproc",
         "crypt_kasumi",
         #"picoriscv",
         "input_devices",
         "de1_cl",
         "bbc_submodules",
         "jtag",
         # clarvi
         ]
if "BBC" in os.environ.keys():
    tests = ["bbc",
             ]

self = sys.modules[__name__]
suite = unittest.TestSuite()
for t in tests:
    mod_t = importlib.import_module(".."+t, "regression.blah")
    suite.addTest(unittest.TestLoader().loadTestsFromModule(mod_t))
    pass
