from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OminimumCls:
	"""Ominimum commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ominimum", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:OMINimum:LESignaling \n
		Snippet: value: int = driver.configure.connection.audio.ominimum.get_le_signaling() \n
		Specifies the minimum offset for LE audio. \n
			:return: offset_minimum: numeric Range: 0 us to 50E+3 us, Unit: us
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:OMINimum:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, offset_minimum: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:OMINimum:LESignaling \n
		Snippet: driver.configure.connection.audio.ominimum.set_le_signaling(offset_minimum = 1) \n
		Specifies the minimum offset for LE audio. \n
			:param offset_minimum: numeric Range: 0 us to 50E+3 us, Unit: us
		"""
		param = Conversions.decimal_value_to_str(offset_minimum)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:OMINimum:LESignaling {param}')
