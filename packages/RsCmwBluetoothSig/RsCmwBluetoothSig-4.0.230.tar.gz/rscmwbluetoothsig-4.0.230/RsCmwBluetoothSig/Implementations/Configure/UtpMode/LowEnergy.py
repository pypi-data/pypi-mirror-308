from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def get_pcode(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:UTPMode:LENergy:PCODe \n
		Snippet: value: int = driver.configure.utpMode.lowEnergy.get_pcode() \n
		No command help available \n
			:return: test_mode_pin: No help available
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:UTPMode:LENergy:PCODe?')
		return Conversions.str_to_int(response)

	def set_pcode(self, test_mode_pin: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:UTPMode:LENergy:PCODe \n
		Snippet: driver.configure.utpMode.lowEnergy.set_pcode(test_mode_pin = 1) \n
		No command help available \n
			:param test_mode_pin: No help available
		"""
		param = Conversions.decimal_value_to_str(test_mode_pin)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:UTPMode:LENergy:PCODe {param}')

	def get_value(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:UTPMode:LENergy \n
		Snippet: value: bool = driver.configure.utpMode.lowEnergy.get_value() \n
		Enables or disables LE UTP test mode at the R&S CMW. \n
			:return: enable_test_mode: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:UTPMode:LENergy?')
		return Conversions.str_to_bool(response)

	def set_value(self, enable_test_mode: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:UTPMode:LENergy \n
		Snippet: driver.configure.utpMode.lowEnergy.set_value(enable_test_mode = False) \n
		Enables or disables LE UTP test mode at the R&S CMW. \n
			:param enable_test_mode: OFF | ON
		"""
		param = Conversions.bool_to_str(enable_test_mode)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:UTPMode:LENergy {param}')
