from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SicpCls:
	"""Sicp commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sicp", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SICP:LESignaling \n
		Snippet: value: int = driver.configure.connection.audio.sicp.get_le_signaling() \n
		Specifies the SDU interval central to peripheral for LE audio. \n
			:return: sdu_interval_cp: numeric Range: 255 us to 1.048575E+6 us, Unit: us
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SICP:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, sdu_interval_cp: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SICP:LESignaling \n
		Snippet: driver.configure.connection.audio.sicp.set_le_signaling(sdu_interval_cp = 1) \n
		Specifies the SDU interval central to peripheral for LE audio. \n
			:param sdu_interval_cp: numeric Range: 255 us to 1.048575E+6 us, Unit: us
		"""
		param = Conversions.decimal_value_to_str(sdu_interval_cp)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SICP:LESignaling {param}')
