from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SintervalCls:
	"""Sinterval commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sinterval", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SINTerval:LESignaling \n
		Snippet: value: int = driver.configure.connection.audio.sinterval.get_le_signaling() \n
		Specifies the subinterval for LE audio. \n
			:return: sub_interval: numeric Range: maximum subevent length to 4E+6 us, Unit: us
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SINTerval:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, sub_interval: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SINTerval:LESignaling \n
		Snippet: driver.configure.connection.audio.sinterval.set_le_signaling(sub_interval = 1) \n
		Specifies the subinterval for LE audio. \n
			:param sub_interval: numeric Range: maximum subevent length to 4E+6 us, Unit: us
		"""
		param = Conversions.decimal_value_to_str(sub_interval)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:SINTerval:LESignaling {param}')
