from mibuild.generic_platform import *
from mibuild.crg import SimpleCRG
from mibuild.xilinx_ise import XilinxISEPlatform
from mibuild.programmer import XC3SProg

_io = [
        ("user_led", 0, Pins("P11"), IOStandard("LVCMOS33")),
        ("user_led", 1, Pins("N9"), IOStandard("LVCMOS33")),
        ("user_led", 2, Pins("M9"), IOStandard("LVCMOS33")),
        ("user_led", 3, Pins("P9"), IOStandard("LVCMOS33")),
        ("user_led", 4, Pins("T8"), IOStandard("LVCMOS33")),
        ("user_led", 5, Pins("N8"), IOStandard("LVCMOS33")),
        ("user_led", 6, Pins("P8"), IOStandard("LVCMOS33")),
        ("user_led", 7, Pins("P7"), IOStandard("LVCMOS33")),
        
	("clk32", 0, Pins("K3"), IOStandard("LVCMOS33")),
        ("clk50", 0, Pins("J4"), IOStandard("LVCMOS33")),

	("spiflash", 0,
		Subsignal("cs_n", Pins("T3")),
		Subsignal("clk", Pins("R11")),
		Subsignal("mosi", Pins("T10")),
		Subsignal("miso", Pins("P10"))
	)
]

_connectors = [
        ("A", "E7 C8 D8 E8 D9 A10 B10 C10 E10 F9 F10 D11"),
        ("B", "E11 D14 D12 E12 E13 F13 F12 F14 G12 H14 J14"),
        ("C", "J13 J12 K14 L14 L13 M14 M13 N14 M12 N12 P12 M11"),
        ("D", "D6 C6 E6 C5"),
        ("E", "D5 A4 G5 A3 B3 A2 B2 C3 C2 D3 D1 E3"),
        ("F", "E2 E1 E4 F4 F5 G3 F3 G1 H3 H1 H2 J1")
]

class Platform(XilinxISEPlatform):
	def __init__(self):
		XilinxISEPlatform.__init__(self, "xc6slx9-3-ftg256", _io,
			lambda p: SimpleCRG(p, "clk50", None), _connectors)

	def create_programmer(self):
		return XC3SProg("minispartan6", "bscan_spi_minispartan6.bit")

	def do_finalize(self, fragment):
		try:
			self.add_period_constraint(self.lookup_request("50"), 50)
		except ConstraintError:
			pass
