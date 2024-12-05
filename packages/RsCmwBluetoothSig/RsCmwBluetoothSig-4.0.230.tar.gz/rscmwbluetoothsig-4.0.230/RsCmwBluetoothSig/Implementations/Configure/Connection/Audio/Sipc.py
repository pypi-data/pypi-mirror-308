from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SipcCls:
	"""Sipc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sipc", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SIPC:LESignaling \n
		Snippet: value: int = driver.configure.connection.audio.sipc.get_le_signaling() \n
		Specifies the SDU interval peripheral to central for LE audio. \n
			:return: sdu_interval_pc: numeric Range: 255 us to 1.048575E+6 us
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SIPC:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, sdu_interval_pc: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SIPC:LESignaling \n
		Snippet: driver.configure.connection.audio.sipc.set_le_signaling(sdu_interval_pc = 1) \n
		Specifies the SDU interval peripheral to central for LE audio. \n
			:param sdu_interval_pc: numeric Range: 255 us to 1.048575E+6 us
		"""
		param = Conversions.decimal_value_to_str(sdu_interval_pc)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SIPC:LESignaling {param}')
