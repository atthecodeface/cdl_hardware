import unittest, importlib, sys, os
tests = [#"base6502",
         "leds",
         "teletext",
         "csrs",
         "apb",
         "utils",
         "clarvi",
         "input_devices",
         "de1_cl",
         #"bbc_submodules",
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
