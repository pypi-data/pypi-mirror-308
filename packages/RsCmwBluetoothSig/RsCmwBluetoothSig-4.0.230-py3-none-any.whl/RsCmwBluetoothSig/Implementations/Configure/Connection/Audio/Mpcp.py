from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MpcpCls:
	"""Mpcp commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mpcp", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:MPCP:LESignaling \n
		Snippet: value: int = driver.configure.connection.audio.mpcp.get_le_signaling() \n
		Specifies the maximum PDU central to peripheral for LE audio. \n
			:return: max_pducp: numeric Range: 0 to 251
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:MPCP:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, max_pducp: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:MPCP:LESignaling \n
		Snippet: driver.configure.connection.audio.mpcp.set_le_signaling(max_pducp = 1) \n
		Specifies the maximum PDU central to peripheral for LE audio. \n
			:param max_pducp: numeric Range: 0 to 251
		"""
		param = Conversions.decimal_value_to_str(max_pducp)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:MPCP:LESignaling {param}')
