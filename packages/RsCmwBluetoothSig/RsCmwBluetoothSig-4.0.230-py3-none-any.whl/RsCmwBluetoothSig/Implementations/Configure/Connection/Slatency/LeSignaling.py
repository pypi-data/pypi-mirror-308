from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LeSignalingCls:
	"""LeSignaling commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("leSignaling", core, parent)

	def get_cperipheral(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SLATency:LESignaling:CPERipheral \n
		Snippet: value: int = driver.configure.connection.slatency.leSignaling.get_cperipheral() \n
		Specify the response latency of peripheral device for connection tests, central ..:CCENtral and peripheral ..:CPERipheral
		R&S CMW LE role. \n
			:return: slave_latency: numeric Range: 0 to 499, Unit: The number of consecutive connection events
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SLATency:LESignaling:CPERipheral?')
		return Conversions.str_to_int(response)

	def set_cperipheral(self, slave_latency: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SLATency:LESignaling:CPERipheral \n
		Snippet: driver.configure.connection.slatency.leSignaling.set_cperipheral(slave_latency = 1) \n
		Specify the response latency of peripheral device for connection tests, central ..:CCENtral and peripheral ..:CPERipheral
		R&S CMW LE role. \n
			:param slave_latency: numeric Range: 0 to 499, Unit: The number of consecutive connection events
		"""
		param = Conversions.decimal_value_to_str(slave_latency)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SLATency:LESignaling:CPERipheral {param}')

	def get_ccentral(self) -> int:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SLATency:LESignaling[:CCENtral] \n
		Snippet: value: int = driver.configure.connection.slatency.leSignaling.get_ccentral() \n
		Specify the response latency of peripheral device for connection tests, central ..:CCENtral and peripheral ..:CPERipheral
		R&S CMW LE role. \n
			:return: slave_latency: numeric Range: 0 to 499, Unit: The number of consecutive connection events
		"""
		response = self._core.io.query_str('CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SLATency:LESignaling:CCENtral?')
		return Conversions.str_to_int(response)

	def set_ccentral(self, slave_latency: int) -> None:
		"""SCPI: CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SLATency:LESignaling[:CCENtral] \n
		Snippet: driver.configure.connection.slatency.leSignaling.set_ccentral(slave_latency = 1) \n
		Specify the response latency of peripheral device for connection tests, central ..:CCENtral and peripheral ..:CPERipheral
		R&S CMW LE role. \n
			:param slave_latency: numeric Range: 0 to 499, Unit: The number of consecutive connection events
		"""
		param = Conversions.decimal_value_to_str(slave_latency)
		self._core.io.write(f'CONFigure:BLUetooth:SIGNaling<Instance>:CONNection:SLATency:LESignaling:CCENtral {param}')
