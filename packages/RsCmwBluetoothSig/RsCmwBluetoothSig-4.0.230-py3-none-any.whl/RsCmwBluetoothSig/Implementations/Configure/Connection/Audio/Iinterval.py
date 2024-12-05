from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IintervalCls:
	"""Iinterval commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iinterval", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:IINTerval:LESignaling \n
		Snippet: value: int = driver.configure.connection.audio.iinterval.get_le_signaling() \n
		Sets the ISO-interval for LE audio. ISO-interval in ms is calculated as the specified value multiplied by 1.25 ms. \n
			:return: iso_interval: numeric Range: 4 to 3200, Unit: ms
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:IINTerval:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, iso_interval: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:IINTerval:LESignaling \n
		Snippet: driver.configure.connection.audio.iinterval.set_le_signaling(iso_interval = 1) \n
		Sets the ISO-interval for LE audio. ISO-interval in ms is calculated as the specified value multiplied by 1.25 ms. \n
			:param iso_interval: numeric Range: 4 to 3200, Unit: ms
		"""
		param = Conversions.decimal_value_to_str(iso_interval)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:AUDio:IINTerval:LESignaling {param}')
