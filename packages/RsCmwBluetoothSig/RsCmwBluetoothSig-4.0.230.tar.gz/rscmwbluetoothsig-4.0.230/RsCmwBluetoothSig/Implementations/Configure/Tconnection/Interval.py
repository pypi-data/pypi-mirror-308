from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IntervalCls:
	"""Interval commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("interval", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:INTerval:LESignaling \n
		Snippet: value: int = driver.configure.tconnection.interval.get_le_signaling() \n
		Sets the time interval between the two consecutive connection events for LE UTP test mode. The interval in ms is
		calculated as the specified value multiplied by 1.25 ms. \n
			:return: connection_interval: numeric Range: 6 to 3200
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:INTerval:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, connection_interval: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:INTerval:LESignaling \n
		Snippet: driver.configure.tconnection.interval.set_le_signaling(connection_interval = 1) \n
		Sets the time interval between the two consecutive connection events for LE UTP test mode. The interval in ms is
		calculated as the specified value multiplied by 1.25 ms. \n
			:param connection_interval: numeric Range: 6 to 3200
		"""
		param = Conversions.decimal_value_to_str(connection_interval)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:TCONnection:INTerval:LESignaling {param}')
