from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MppcCls:
	"""Mppc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mppc", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:MPPC:LESignaling \n
		Snippet: value: int = driver.configure.connection.audio.mppc.get_le_signaling() \n
		Specifies the maximum PDU peripheral to central for LE audio. \n
			:return: max_pdupc: numeric Range: 0 to 251
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:MPPC:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, max_pdupc: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:MPPC:LESignaling \n
		Snippet: driver.configure.connection.audio.mppc.set_le_signaling(max_pdupc = 1) \n
		Specifies the maximum PDU peripheral to central for LE audio. \n
			:param max_pdupc: numeric Range: 0 to 251
		"""
		param = Conversions.decimal_value_to_str(max_pdupc)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:MPPC:LESignaling {param}')
