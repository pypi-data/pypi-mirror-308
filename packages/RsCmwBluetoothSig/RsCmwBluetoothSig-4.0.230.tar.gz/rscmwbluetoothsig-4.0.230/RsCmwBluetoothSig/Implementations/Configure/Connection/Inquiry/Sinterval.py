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
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:SINTerval:LESignaling \n
		Snippet: value: int = driver.configure.connection.inquiry.sinterval.get_le_signaling() \n
		Specifies the Inquiry Scan Interval between two consecutive inquiry scans. The interval in ms is calculated as the
		specified value multiplied by 0.625 ms. \n
			:return: inq_scan_int: numeric Range: 4 to 16.384E+3
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:SINTerval:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, inq_scan_int: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:SINTerval:LESignaling \n
		Snippet: driver.configure.connection.inquiry.sinterval.set_le_signaling(inq_scan_int = 1) \n
		Specifies the Inquiry Scan Interval between two consecutive inquiry scans. The interval in ms is calculated as the
		specified value multiplied by 0.625 ms. \n
			:param inq_scan_int: numeric Range: 4 to 16.384E+3
		"""
		param = Conversions.decimal_value_to_str(inq_scan_int)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:INQuiry:SINTerval:LESignaling {param}')
