from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BnpcCls:
	"""Bnpc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bnpc", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BNPC:LESignaling \n
		Snippet: value: int = driver.configure.connection.audio.bnpc.get_le_signaling() \n
		Specifies the burst number peripheral to central for LE audio. \n
			:return: burst_number_pc: numeric Range: 0 to 15
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BNPC:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, burst_number_pc: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BNPC:LESignaling \n
		Snippet: driver.configure.connection.audio.bnpc.set_le_signaling(burst_number_pc = 1) \n
		Specifies the burst number peripheral to central for LE audio. \n
			:param burst_number_pc: numeric Range: 0 to 15
		"""
		param = Conversions.decimal_value_to_str(burst_number_pc)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:BNPC:LESignaling {param}')
