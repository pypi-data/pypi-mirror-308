from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FtpcCls:
	"""Ftpc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ftpc", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:FTPC:LESignaling \n
		Snippet: value: int = driver.configure.connection.audio.ftpc.get_le_signaling() \n
		Specifies the flash time peripheral to central for LE audio. \n
			:return: flush_time_pc: numeric Range: 1 to 255
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:FTPC:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, flush_time_pc: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:FTPC:LESignaling \n
		Snippet: driver.configure.connection.audio.ftpc.set_le_signaling(flush_time_pc = 1) \n
		Specifies the flash time peripheral to central for LE audio. \n
			:param flush_time_pc: numeric Range: 1 to 255
		"""
		param = Conversions.decimal_value_to_str(flush_time_pc)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:FTPC:LESignaling {param}')
