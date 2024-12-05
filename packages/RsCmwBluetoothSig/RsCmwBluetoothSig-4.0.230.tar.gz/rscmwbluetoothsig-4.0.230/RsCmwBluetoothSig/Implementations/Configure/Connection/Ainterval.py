from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AintervalCls:
	"""Ainterval commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ainterval", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AINTerval:LESignaling \n
		Snippet: value: int = driver.configure.connection.ainterval.get_le_signaling() \n
		Specifies the interval between two consecutive advertisers for an instrument in peripheral LE role. \n
			:return: adv_int: numeric Range: 32 to 16.384E+3
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AINTerval:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, adv_int: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AINTerval:LESignaling \n
		Snippet: driver.configure.connection.ainterval.set_le_signaling(adv_int = 1) \n
		Specifies the interval between two consecutive advertisers for an instrument in peripheral LE role. \n
			:param adv_int: numeric Range: 32 to 16.384E+3
		"""
		param = Conversions.decimal_value_to_str(adv_int)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AINTerval:LESignaling {param}')
