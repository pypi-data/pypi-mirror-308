from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TimeoutCls:
	"""Timeout commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("timeout", core, parent)

	def get_le_signaling(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:TOUT:LESignaling \n
		Snippet: value: int = driver.configure.connection.paging.timeout.get_le_signaling() \n
		Specifies the PageTimeout configuration parameter, i.e. the maximum time the local link manager waits for a baseband page
		response from the EUT. \n
			:return: timeout: integer Range: 10 ms to 30E+3 ms, Unit: s
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:TOUT:LESignaling?')
		return Conversions.str_to_int(response)

	def set_le_signaling(self, timeout: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:TOUT:LESignaling \n
		Snippet: driver.configure.connection.paging.timeout.set_le_signaling(timeout = 1) \n
		Specifies the PageTimeout configuration parameter, i.e. the maximum time the local link manager waits for a baseband page
		response from the EUT. \n
			:param timeout: integer Range: 10 ms to 30E+3 ms, Unit: s
		"""
		param = Conversions.decimal_value_to_str(timeout)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:TOUT:LESignaling {param}')

	def get_value(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:TOUT \n
		Snippet: value: int = driver.configure.connection.paging.timeout.get_value() \n
		Sets/gets the Page_Timeout configuration parameter, i.e. the maximum time the local link manager waits for a baseband
		page response from the EUT. \n
			:return: timeout: integer Range: 22 to 65535, Unit: slot (625 us)
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:TOUT?')
		return Conversions.str_to_int(response)

	def set_value(self, timeout: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:TOUT \n
		Snippet: driver.configure.connection.paging.timeout.set_value(timeout = 1) \n
		Sets/gets the Page_Timeout configuration parameter, i.e. the maximum time the local link manager waits for a baseband
		page response from the EUT. \n
			:param timeout: integer Range: 22 to 65535, Unit: slot (625 us)
		"""
		param = Conversions.decimal_value_to_str(timeout)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:PAGing:TOUT {param}')
