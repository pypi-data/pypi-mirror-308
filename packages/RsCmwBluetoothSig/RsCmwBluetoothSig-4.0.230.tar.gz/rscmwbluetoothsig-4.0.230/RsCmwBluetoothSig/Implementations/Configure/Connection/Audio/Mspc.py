from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MspcCls:
	"""Mspc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mspc", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:MSPC:LESignaling \n
		Snippet: value: int = driver.configure.connection.audio.mspc.get_le_signaling() \n
		Specifies the max SDU peripheral to central for LE audio. \n
			:return: max_sdupc: numeric Range: 0 to 4095
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:MSPC:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, max_sdupc: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:MSPC:LESignaling \n
		Snippet: driver.configure.connection.audio.mspc.set_le_signaling(max_sdupc = 1) \n
		Specifies the max SDU peripheral to central for LE audio. \n
			:param max_sdupc: numeric Range: 0 to 4095
		"""
		param = Conversions.decimal_value_to_str(max_sdupc)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:MSPC:LESignaling {param}')
