from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LowEnergyCls:
	"""LowEnergy commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lowEnergy", core, parent)

	def get_le_1_m(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:ITENd:LENergy:LE1M \n
		Snippet: value: bool = driver.configure.rxQuality.itend.lowEnergy.get_le_1_m() \n
		Specifies, whether the R&S CMW ignores the DUT's response to end of direction finding tests. \n
			:return: ignore_test_end: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:ITENd:LENergy:LE1M?')
		return Conversions.str_to_bool(response)

	def set_le_1_m(self, ignore_test_end: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:ITENd:LENergy:LE1M \n
		Snippet: driver.configure.rxQuality.itend.lowEnergy.set_le_1_m(ignore_test_end = False) \n
		Specifies, whether the R&S CMW ignores the DUT's response to end of direction finding tests. \n
			:param ignore_test_end: OFF | ON
		"""
		param = Conversions.bool_to_str(ignore_test_end)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:ITENd:LENergy:LE1M {param}')

	def get_le_2_m(self) -> bool:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:ITENd:LENergy:LE2M \n
		Snippet: value: bool = driver.configure.rxQuality.itend.lowEnergy.get_le_2_m() \n
		Specifies, whether the R&S CMW ignores the DUT's response to end of direction finding tests. \n
			:return: ignore_test_end: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:ITENd:LENergy:LE2M?')
		return Conversions.str_to_bool(response)

	def set_le_2_m(self, ignore_test_end: bool) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:ITENd:LENergy:LE2M \n
		Snippet: driver.configure.rxQuality.itend.lowEnergy.set_le_2_m(ignore_test_end = False) \n
		Specifies, whether the R&S CMW ignores the DUT's response to end of direction finding tests. \n
			:param ignore_test_end: OFF | ON
		"""
		param = Conversions.bool_to_str(ignore_test_end)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:RXQuality:ITENd:LENergy:LE2M {param}')
