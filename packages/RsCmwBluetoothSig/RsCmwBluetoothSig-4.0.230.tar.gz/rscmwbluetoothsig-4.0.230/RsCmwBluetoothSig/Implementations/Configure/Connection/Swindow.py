from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SwindowCls:
	"""Swindow commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("swindow", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SWINdow:LESignaling \n
		Snippet: value: int = driver.configure.connection.swindow.get_le_signaling() \n
		Specifies the interval between two consecutive page scans. The interval in ms is calculated as the specified value
		multiplied by 0.625 ms. \n
			:return: conn_scan_win: numeric Range: 4 to 16.384E+3
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SWINdow:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, conn_scan_win: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SWINdow:LESignaling \n
		Snippet: driver.configure.connection.swindow.set_le_signaling(conn_scan_win = 1) \n
		Specifies the interval between two consecutive page scans. The interval in ms is calculated as the specified value
		multiplied by 0.625 ms. \n
			:param conn_scan_win: numeric Range: 4 to 16.384E+3
		"""
		param = Conversions.decimal_value_to_str(conn_scan_win)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SWINdow:LESignaling {param}')
