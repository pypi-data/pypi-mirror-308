from enum import Enum
# noinspection PyPep8Naming
from .Internal.RepeatedCapability import VALUE_DEFAULT as DefaultRepCap
# noinspection PyPep8Naming
from .Internal.RepeatedCapability import VALUE_EMPTY as EmptyRepCap
# noinspection PyPep8Naming
from .Internal.RepeatedCapability import VALUE_SKIP_HEADER as SkipHeaderRepCap


# noinspection SpellCheckingInspection
class Instance(Enum):
	"""Global Repeated capability Instance"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Inst1 = 1
	Inst2 = 2
	Inst3 = 3
	Inst4 = 4


# noinspection SpellCheckingInspection
class CommSettings(Enum):
	"""Repeated capability CommSettings"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Hw1 = 1
	Hw2 = 2
	Hw3 = 3
	Hw4 = 4


# noinspection SpellCheckingInspection
class HardwareIntf(Enum):
	"""Repeated capability HardwareIntf"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Intf1 = 1
	Intf2 = 2
	Intf3 = 3
	Intf4 = 4


# noinspection SpellCheckingInspection
class UsbSettings(Enum):
	"""Repeated capability UsbSettings"""
	Empty = EmptyRepCap
	Default = DefaultRepCap
	
	Sett1 = 1
	Sett2 = 2
	Sett3 = 3
	Sett4 = 4
