from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OmaximumCls:
	"""Omaximum commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("omaximum", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:OMAXimum:LESignaling \n
		Snippet: value: int = driver.configure.connection.audio.omaximum.get_le_signaling() \n
		Specifies the maximum offset for LE audio. \n
			:return: offset_maximum: numeric Range: 0 us to 50E+3 us, Unit: us
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:OMAXimum:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, offset_maximum: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:OMAXimum:LESignaling \n
		Snippet: driver.configure.connection.audio.omaximum.set_le_signaling(offset_maximum = 1) \n
		Specifies the maximum offset for LE audio. \n
			:param offset_maximum: numeric Range: 0 us to 50E+3 us, Unit: us
		"""
		param = Conversions.decimal_value_to_str(offset_maximum)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:OMAXimum:LESignaling {param}')
